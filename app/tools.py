import os
import subprocess
from langchain.tools import tool

# Constants
SANDBOX_DIR = "./my_project_sandbox"

def setup_environment():
    """Sets up the sandbox directory."""
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
        print(f"Created sandbox directory: {SANDBOX_DIR}")

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

@tool
def create_test_file(filename: str, content: str) -> str:
    """
    Creates a new Python test file in the sandbox directory.
    
    Args:
        filename (str): The name of the file. MUST start with 'test_' and end with '.py'.
        content (str): The content of the test file (pytest code).
        
    Returns:
        str: Status message indicating success or failure, including the full path.
    """
    if not filename.startswith("test_") or not filename.endswith(".py"):
        return f"Error: Filename '{filename}' must start with 'test_' and end with '.py'."
    
    full_path = os.path.join(SANDBOX_DIR, filename)
    
    if os.path.exists(full_path):
        return f"Error: File '{full_path}' already exists. Please use edit_file to modify it."
        
    try:
        with open(full_path, "w", encoding='utf-8') as f:
            f.write(content)
        return f"Successfully created test file at: {os.path.abspath(full_path)}"
    except Exception as e:
        return f"Error creating test file: {str(e)}"
