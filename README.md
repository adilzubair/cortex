# Cortex: Local AI-Powered Codebase Assistant

Cortex is a powerful, local-first RAG (Retrieval-Augmented Generation) agent designed to help you understand, navigate, and query your codebases with ease. It leverages LangChain and local LLMs (via Ollama) to provide precise answers while keeping your data private.

## 🚀 Key Features

- **Local-First RAG**: Uses Ollama for embeddings and LLM inference.
- **Incremental Indexing**: SHA-256 based change detection ensures only modified files are re-indexed.
- **Automated Background Watching**: Stays in sync with your code changes in real-time using `watchdog`.
- **Symbolic Intelligence (LSP)**: Integrated with Jedi for precise symbol definition and reference lookup.
- **Professional CLI**: Polished terminal interface using `Typer` and `Rich`.
- **Model Agnostic**: Easily switch between local models (Ministral, Llama, Qwen) or OpenAI.

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/cortex.git
cd cortex

# Install dependencies using uv
uv sync
```

### Setup Ollama
Cortex is optimized for `ministral-3:3b` and `llama3.1:8b`.
```bash
ollama run ministral-3:3b
ollama run qwen3-embedding:0.6b
```

## 📖 Usage

### Initial Indexing
Index your project to build the knowledge base:
```bash
uv run python main.py index .
```

### Ask a Question
Quickly query your codebase from the terminal:
```bash
uv run python main.py ask "How does the StateManager handle file hashing?"
```

### Interactive Chat
Start a conversation with your code:
```bash
uv run python main.py chat
```

### Real-Time Monitoring
The `chat` and `ask` commands automatically start a background watcher. To run the watcher manually:
```bash
uv run python main.py watch .
```

## 🏗️ Architecture

- **Ingestion**: Recursive file loading with targeted chunking for Python and Text.
- **Storage**: ChromaDB for vector retrieval.
- **Agent**: LangGraph-based ReAct agent for multi-step reasoning and tool usage.
- **LSP**: Jedi for static analysis and symbolic navigation.

## 📄 License
MIT
