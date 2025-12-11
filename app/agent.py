from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver

from app.config import model
from app.tools import run_tests, SANDBOX_DIR

# Subagent Configuration
qa_tester = {
    "name": "qa_tester",
    "description": "A QA Tester subagent that runs tests and reports errors.",
    "system_prompt": "You are a QA Tester. Run the tests using the run_tests tool and report the exact error logs.",
    "tools": [run_tests],
    "model": model, 
}

# Main Agent System Prompt
SYSTEM_PROMPT = """Act as a Senior Python Engineer doing TDD (Test-Driven Development).
You have a specific goal: Implement code to pass provided tests.
CRITICAL RULES:

1. **SEQUENTIAL EXECUTION**: You MUST NOT run tests while writing code. You must:
   a. Write the implementation file (write_file).
   b. WAIT for the file to be written (and approved by the user).
   c. ONLY THEN, run the tests (task -> qa_tester).

   Do not try to do step (a) and (c) in the same turn.

2. **EFFICIENCY**:
   - If `ls` shows you the files you need, DO NOT run `glob` to look for them again.
   - Read the test file immediately to understand requirements.

Your workflow is:
1. Explore: Use `ls` to find what tests exist.
2. Plan: Read the test file.
3. Implement: Use `write_file` to create the solution.
4. Verify: Use `task` to call the 'qa_tester' subagent.
5. Iterate: If tests fail, analyze and `edit_file`.

"""

def build_autodev_agent():
    """Constructs and returns the configured Deep Agent."""
    
    # Backend & Checkpointer
    # Virtual mode true for safety, rooted in the sandbox
    backend = FilesystemBackend(root_dir=SANDBOX_DIR, virtual_mode=True)
    checkpointer = MemorySaver()

    agent = create_deep_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        backend=backend,
        checkpointer=checkpointer,
        subagents=[qa_tester],
        # Configure HITL interrupts
        interrupt_on={
            "write_file": True,
            "edit_file": True,
        }
    )
    return agent
