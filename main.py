import sys
import json
from langgraph.types import Command
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.theme import Theme

from app.tools import setup_environment
from app.agent import build_autodev_agent

# Initialize Rich Console with a theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console = Console(theme=custom_theme)

def stream_agent(agent, inputs, config, last_message_count=0):
    """Execution helper that streams steps and prints them nicely."""
    
    final_chunk = None
    
    # We use stream_mode="values" to get the full state after each node
    for chunk in agent.stream(inputs, config=config, stream_mode="values"):
        final_chunk = chunk
        messages = chunk.get("messages", [])
        
        # Check for new messages
        if len(messages) > last_message_count:
            new_msgs = messages[last_message_count:]
            for msg in new_msgs:
                role = msg.type
                content = getattr(msg, 'content', '')
                
                if role == "human":
                     console.print(Panel(content, title="[bold green]HUMAN[/bold green]", border_style="green"))
                elif role == "ai":
                    # Display AI thought/content
                    if content:
                        console.print(Panel(Markdown(content), title="[bold blue]AI[/bold blue]", border_style="blue"))
                    
                    # Display Tool Calls if any
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tc in msg.tool_calls:
                            console.print(Panel(
                                Syntax(json.dumps(tc['args'], indent=2), "json", theme="monokai", word_wrap=True),
                                title=f"[bold yellow]Tool Call: {tc['name']}[/bold yellow]",
                                border_style="yellow"
                            ))
                elif role == "tool":
                    # Display Tool Output
                    # Try to pretty print if it looks like code or long text
                    if len(content) > 500 or "\n" in content:
                         console.print(Panel(Syntax(content, "python", theme="monokai", word_wrap=True), title=f"[bold purple]Tool Output[/bold purple]", border_style="purple"))
                    else:
                         console.print(Panel(content, title=f"[bold purple]Tool Output[/bold purple]", border_style="purple"))
            
            last_message_count = len(messages)
            
    return final_chunk, last_message_count

def main():
    console.print("[bold green]Starting AutoDev Agent (Refactored with Rich UI)...[/bold green]")
    
    # 1. Setup Sandbox
    setup_environment()
    
    # 2. Build Agent
    agent = build_autodev_agent()
    
    # 3. Initial input
    initial_message = "Buatkan fungsi untuk menghitung luas lingkaran"
    config = {"configurable": {"thread_id": "autodev-session-1", "recursion_limit": 50}}
    
    # Initial invocation with streaming
    console.print("\n[bold cyan]Invoking agent...[/bold cyan]")
    
    # Track message count state
    current_msg_count = 0
    
    result, current_msg_count = stream_agent(
        agent,
        {"messages": [{"role": "user", "content": initial_message}]},
        config,
        last_message_count=current_msg_count
    )

    # 4. HITL Loop
    while True:
        # Check if execution was interrupted
        if isinstance(result, dict) and result.get("__interrupt__"):
            interrupts = result["__interrupt__"][0].value
            action_requests = interrupts["action_requests"]
            review_configs = interrupts["review_configs"]
            
            # Map tool name to its config
            config_map = {cfg["action_name"]: cfg for cfg in review_configs}

            decisions = []
            
            # Process each action request
            for action in action_requests:
                action_name = action["name"]
                action_args = action["args"]
                review_config = config_map.get(action_name, {})
                
                console.print("\n" + "="*50, style="warning")
                console.print(f"⚠️ INTERRUPT: Agent wants to call tool '[bold]{action_name}[/bold]'", style="warning")
                console.print(Syntax(json.dumps(action_args, indent=2), "json", theme="monokai"), style="warning")
                console.print(f"Allowed decisions: {review_config.get('allowed_decisions', ['approve', 'reject', 'edit'])}")
                console.print("="*50 + "\n", style="warning")
                
                try:
                    user_input = console.input("[bold white]Action (approve/reject/edit): [/bold white]").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    console.print("\nExiting...", style="danger")
                    sys.exit(0)

                decision = {}
                if user_input == "approve":
                    decision = {"type": "approve"}
                elif user_input == "reject":
                    decision = {"type": "reject"}
                elif user_input == "edit":
                    console.print("Enter new arguments as JSON string (or press Enter to cancel edit and reject):")
                    new_args_str = input()
                    try:
                        if new_args_str:
                            new_args = json.loads(new_args_str)
                            decision = {
                                "type": "edit", 
                                "edited_action": {"name": action_name, "args": new_args}
                            }
                        else:
                            decision = {"type": "reject"}
                    except Exception as e:
                        console.print(f"Invalid JSON: {e}. Rejecting action.", style="danger")
                        decision = {"type": "reject"}
                else:
                    console.print("Unknown input, defaulting to reject.", style="danger")
                    decision = {"type": "reject"}
                
                decisions.append(decision)
            
            # Resume execution with decisions (Streaming)
            console.print("[info]Resuming execution...[/info]")
            result, current_msg_count = stream_agent(
                agent,
                Command(resume={"decisions": decisions}),
                config,
                last_message_count=current_msg_count
            )
        else:
            # If no interrupt, we are done or it's a normal finish
            if isinstance(result, dict) and "messages" in result:
                console.print("\n[bold green]FINISHED.[/bold green]")
            break

if __name__ == "__main__":
    main()
