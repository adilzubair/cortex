# Cortex: Local AI-Powered Codebase Assistant

Cortex is a powerful, local-first RAG (Retrieval-Augmented Generation) agent designed to help you understand, navigate, and query your codebases with ease. It leverages LangChain and local LLMs (via Ollama) to provide precise answers while keeping your data private.

## 🚀 Key Features

- **Multi-Project Aware**: Stores all metadata, indices, and state locally in a `.cortex` directory within each project. Work on as many projects as you want independently.
- **Incremental Indexing**: Uses SHA-256 hashing to detect changes. Only modified files are re-indexed, making updates lightning fast.
- **Symbolic Intelligence (LSP)**: Integrated with **Jedi** for precise symbol definition and reference lookup. The agent doesn't just "guess"; it knows exactly where your classes and functions are defined.
- **Agentic Reasoning**: Uses a LangGraph-based ReAct agent that can search code, read files, find symbol definitions, and list files to solve complex queries.
- **Automated Background Watching**: Stays in sync with your code changes in real-time using `watchdog`. Changes are reflected in your queries immediately.
- **Professional CLI**: Polished terminal interface using `Typer` and `Rich` for a premium developer experience.
- **Model Agnostic**: Optimized for `ministral-3:3b` and `qwen3-embedding:0.6b`, but easily configurable for OpenAI or other local models.

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/cortex.git
cd cortex

# Install dependencies using uv
uv sync
```

### Setup Models
Cortex uses `ministral-3:3b` for inference and `qwen3-embedding:0.6b` for embeddings. You can install them automatically:
```bash
./scripts/install_models.sh
```

## 📖 Usage

### Initial Indexing
Index any project (current or external folder) to build the knowledge base. A `.cortex` folder will be created at the target path.
```bash
uv run python main.py index .
# Or index an external project
uv run python main.py index /path/to/another/project
```

### Ask a Question
Quickly query your codebase. Cortex will automatically start a background watcher for the project during the query.
```bash
uv run python main.py ask "How does the StateManager handle file hashing?"
# Query a specific project
uv run python main.py ask "List all tools" -p /path/to/project
```

### Interactive Chat
Start a persistent conversation with your code. Supports multiple providers and models.
```bash
uv run python main.py chat
# Chat with a specific project using OpenAI
uv run python main.py chat --project /path/to/project --provider openai --model gpt-4o
```

### Real-Time Monitoring
While `ask` and `chat` handle watching automatically, you can run the watcher manually to keep indices in sync:
```bash
uv run python main.py watch .
```

## 🏗️ Architecture

- **Ingestion**: Recursive file loading with targeted chunking for Python and Text.
- **State Management**: SQLite-based file hashing stored in `.cortex/indexing/state.db`.
- **Storage**: ChromaDB for vector retrieval stored in `.cortex/chroma/`.
- **Agent**: LangGraph-based ReAct agent for multi-step reasoning.
- **LSP**: Jedi for static analysis and symbolic navigation.

## 📄 License
MIT
