from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from core.config import get_vector_persist_dir
import os
import jedi

def get_embeddings():
    return OllamaEmbeddings(model="qwen3-embedding:0.6b", base_url="http://localhost:11434")

class ProjectTools:
    def __init__(self, project_path: str = "."):
        self.project_path = os.path.abspath(project_path)
        self.vectorstore = Chroma(
            collection_name="cortex",
            embedding_function=get_embeddings(),
            persist_directory=get_vector_persist_dir(self.project_path)
        )

    def get_tools(self):
        @tool("search_code", description="Search for relevant code snippets in the indexed codebase. Useful for answering questions about how things work or finding specific logic.")
        def search_code(query: str):
            results = self.vectorstore.similarity_search(query, k=5)
            formatted = []
            for doc in results:
                formatted.append(f"File: {doc.metadata.get('path')}\nContent:\n{doc.page_content}\n---")
            return "\n".join(formatted)

        @tool("read_file", description="Read the full content of a file from the local filesystem. Use this when you need more context than the search results provide.")
        def read_file(path: str):
            try:
                # If path is relative, make it relative to project_path
                full_path = path if os.path.isabs(path) else os.path.join(self.project_path, path)
                with open(full_path, 'r') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file {path}: {str(e)}"

        @tool("get_symbol_info", description="Find definitions of a code symbol (class, function, variable) across the project.")
        def get_symbol_info(symbol_name: str):
            """Search for symbol definitions using static analysis."""
            project = jedi.Project(self.project_path)
            names = project.search(symbol_name)
            results = []
            for name in names:
                if name.is_definition():
                    results.append(
                        f"Symbol: {name.full_name}\n"
                        f"Type: {name.type}\n"
                        f"File: {name.module_path}\n"
                        f"Line: {name.line}, Column: {name.column}\n"
                    )
            
            if not results:
                return f"No definitions found for symbol '{symbol_name}'."
            
            return "\n---\n".join(results)

        @tool("find_references", description="Find where a specific code symbol is used across the project.")
        def find_references(symbol_name: str):
            """Search for usages of a symbol across the project."""
            project = jedi.Project(self.project_path)
            names = project.search(symbol_name)
            results = []
            for name in names:
                if name.is_definition():
                    refs = name.references()
                    for ref in refs:
                        results.append(
                            f"File: {ref.module_path}\n"
                            f"Line: {ref.line}, Column: {ref.column}\n"
                            f"Context: {ref.description}\n"
                        )
            
            if not results:
                return f"No references found for symbol '{symbol_name}'."
            
            unique_results = list(dict.fromkeys(results))[:15]
            return "Top Usages:\n" + "\n---\n".join(unique_results)

        @tool("list_files", description="List all files in a given directory (recursive). Useful for seeing the project structure or finding where a specific file might be located.")
        def list_files(directory: str = "."):
            """List files in the project, ignoring common artifacts."""
            # Resolve directory relative to project_path
            search_path = directory if os.path.isabs(directory) else os.path.join(self.project_path, directory)
            
            files_list = []
            ignore_list = [".git", "__pycache__", ".venv", ".cortex", ".gemini", ".pytest_cache"]
            
            for root, dirs, files in os.walk(search_path):
                dirs[:] = [d for d in dirs if not (d.startswith(".") or d in ignore_list)]
                
                for file in files:
                    if not (file.startswith(".") or file.endswith((".pyc", ".pyo", "-journal", ".tmp"))):
                        rel_path = os.path.relpath(os.path.join(root, file), self.project_path)
                        files_list.append(rel_path)
            
            if not files_list:
                return f"No files found in directory '{directory}' (or everything is ignored)."
                
            return "\n".join(files_list[:100])

        return [search_code, read_file, get_symbol_info, find_references, list_files]
