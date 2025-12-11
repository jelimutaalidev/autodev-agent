# AutoDev Agent 🤖💻

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-v0.3-green?logo=chainlink&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Stateful-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

**AutoDev Agent** is an advanced, autonomous AI programming assistant designed to execute Test-Driven Development (TDD) workflows with precision and safety. Unlike standard code assistants, AutoDev operates as a stateful agent that writes implementation code, runs unit tests in a sandboxed environment, and iteratively fixes bugs until all tests pass—all while keeping the user in the control loop.

## 🚀 Key Features

*   **Autonomous TDD Workflow**: The agent explores requirements, plans the implementation, writes code, and verifies it against tests automatically.
*   **Human-in-the-Loop (HITL)**: Critical actions like writing or editing files trigger an interrupt, strictly requiring user approval before execution. This ensures safety and aligns with user intent.
*   **Multi-Agent Architecture**: specifically orchestrates specialized subagents (e.g., `qa_tester`) to handle distinct tasks like running pytest suites.
*   **Sandboxed Execution**: All file operations and test executions are confined to a `virtual_mode` sandbox, preventing accidental modification of host system files.
*   **Stateful Memory**: Leveraging **LangGraph**, the agent maintains context across steps, allowing for complex, multi-turn reasoning and backtracking.
*   **Professional UI**: Built with `Rich`, offering a beautiful, streaming command-line interface that distinguishes between human, AI, and tool outputs.

## 🛠️ Tech Stack

*   **Core**: Python 3.12+
*   **Orchestration**: LangChain & LangGraph
*   **Agent Framework**: Deep Agents (Custom Wrapper)
*   **UI/CLI**: Rich
*   **Testing**: Pytest

## 🏗️ Architecture

AutoDev uses a graph-based control flow:
1.  **User Input**: User defines a goal (e.g., "Implement a calculator").
2.  **Planner**: The main agent analyzes the request and existing tests.
3.  **Executor**: The agent utilizes tool lookups to write implementation code.
4.  **Verifier**: The `qa_tester` subagent runs the test suite.
5.  **Refiner**: If tests fail, the agent receives the error logs and iterates on the code.
6.  **Human Gate**: Before committing any file change, the system pauses for user review.

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/jelimutaalidev/autodev-agent.git
    cd autodev-agent
    ```

2.  **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Make sure you have your API keys set up (e.g., `GOOGLE_API_KEY` for Gemini models).

## 🏃 Usage

Run the main application entry point:

```bash
python main.py
```

The agent will initialize the sandbox, create a sample failing test (in Hard Mode), and immediately begin the cycle to solve it.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

*Built with ❤️ by [Jeli Mutaali](https://github.com/jelimutaalidev)*
