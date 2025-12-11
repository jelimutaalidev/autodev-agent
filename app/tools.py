import os
import subprocess
from langchain.tools import tool

# Constants
SANDBOX_DIR = "./my_project_sandbox"
TEST_FILE_PATH = os.path.join(SANDBOX_DIR, "test_calculator.py")

def setup_environment():
    """Sets up the sandbox directory and a dummy failing test file (Hard Mode)."""
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
        print(f"Created sandbox directory: {SANDBOX_DIR}")

    # Create difficult test file with specific edge cases
    test_content = """import pytest

def test_add():
    from calculator import add
    assert add(2, 3) == 5

def test_subtract():
    from calculator import subtract
    assert subtract(10, 5) == 5

def test_divide():
    from calculator import divide
    # Normal case
    assert divide(10, 2) == 5
    
    # Edge case: Division by zero MUST raise ValueError
    # (The agent usually forgets this or raises ZeroDivisionError instead, causing a failure)
    with pytest.raises(ValueError):
        divide(10, 0)
"""
    with open(TEST_FILE_PATH, "w") as f:
        f.write(test_content)
    print(f"Created dummy test file for Hard Mode: {TEST_FILE_PATH}")

@tool
def run_tests() -> str:
    """
    Runs pytest in the sandbox directory and returns the stdout/stderr.
    Useful for checking if code passes unit tests.
    """
    from rich.console import Console
    console = Console()
    
    try:
        console.print("[bold cyan]Running tests...[/bold cyan]")
        
        # Run pytest inside the sandbox directory with Popen for streaming
        process = subprocess.Popen(
            ["pytest"],
            cwd=SANDBOX_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # Merge stderr into stdout
            text=True,
            bufsize=1, # Line buffered
            encoding='utf-8' # Explicit encoding
        )
        
        output_lines = []
        
        # Stream output
        if process.stdout:
            for line in process.stdout:
                # Print live to user terminal
                console.print(line, end="", style="dim")
                output_lines.append(line)
        
        process.wait()
        
        full_output = "".join(output_lines)
        
        if process.returncode == 0:
            return f"Tests Passed:\n{full_output}"
        else:
            return f"Tests Failed:\n{full_output}"
            
    except Exception as e:
        return f"Error running tests: {str(e)}"
