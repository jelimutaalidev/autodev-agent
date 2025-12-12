from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver

from app.config import model
from app.config import model
from app.tools import run_tests, create_test_file, SANDBOX_DIR

# Subagent Configuration
qa_tester = {
    "name": "qa_tester",
    "description": "A QA Tester subagent that runs tests and reports errors.",
    "system_prompt": "You are a QA Tester. Run the tests using the run_tests tool and report the exact error logs.",
    "tools": [run_tests],
    "model": model, 
}

test_writer = {
    "name": "test_writer",
    "description": "A QA Architect subagent that writes comprehensive pytest cases based on requirements.",
    "system_prompt": """You are a QA Architect. Your ONLY goal is to write comprehensive pytest cases based on user requirements.
Do NOT create todo lists. Do NOT use create_todos.
Do NOT plan. JUST EXECUTE.
Review the requirements and IMMEDIATELY use the `create_test_file` tool to save your work.
Focus on edge cases.""",
    "tools": [create_test_file],
    "model": model,
}

# Main Agent System Prompt
SYSTEM_PROMPT = """Act as a Senior Python Engineer doing TDD (Test-Driven Development).
You have a specific goal: Implement code to pass provided tests.

CRITICAL RULES:

1. **DUAL LOOP TDD**: You work in a strict cycle:
   a. **Delegate to `test_writer`**: Send the requirements to the test_writer subagent to create the test file.
   b. **Read the Test File**: Once `test_writer` confirms creation, you MUST use `read_file` (or `cat`) to read the content of the created test file.
      - YOU CANNOT IMPLEMENT CODE WITHOUT READING THE TEST FIRST.
   c. **Implement**: Write the implementation file (`write_file`) to pass the specific tests you just read.
   d. **Verify**: Use `qa_tester` to run the tests.

2. **SEQUENTIAL EXECUTION**: You MUST NOT run tests while writing code. You must:
   a. Write the implementation file.
   b. WAIT for the file to be written (and approved by the user).
   c. ONLY THEN, run the tests via `qa_tester`.

3. **EFFICIENCY**:
   - If `ls` shows you the files you need, DO NOT run `glob` to look for them again.

Your workflow is:
1. Plan: Analyze requirements.
2. Delegate: Call `test_writer` to create tests.
3. Read: Read the created test file.
4. Implement: Use `write_file` to create the solution.
5. Verify: Call `qa_tester` to run tests.
6. Iterate: If tests fail, analyze and `edit_file`.

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
        subagents=[test_writer, qa_tester],
        # Configure HITL interrupts
        interrupt_on={
            "create_test_file": True,
            "write_file": True,
            "edit_file": True,
        }
    )
    return agent
