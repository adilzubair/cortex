from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from core.config import get_vector_persist_dir
import os
import ast
import fnmatch
import re
import subprocess
import jedi

def get_embeddings():
    return OllamaEmbeddings(model="qwen3-embedding:0.6b", base_url="http://localhost:11434")

class ProjectTools:
    def __init__(self, project_path: str = ".", llm=None):
        self.project_path = os.path.abspath(project_path)
        self.llm = llm
        self.vectorstore = Chroma(
            collection_name="cortex",
            embedding_function=get_embeddings(),
            persist_directory=get_vector_persist_dir(self.project_path)
        )

    def get_tools(self):
        @tool("search_code", description="Search for relevant code snippets in the indexed codebase. Useful for answering questions about how things work or finding specific logic.")
        def search_code(query: str):
            # Fetch more results initially for reranking
            results = self.vectorstore.similarity_search(query, k=10)
            
            # Rerank results if LLM is available
            if self.llm and results:
                from agents.reranker import Reranker
                reranker = Reranker(self.llm)
                results = reranker.rerank(query, results, top_k=5)
            else:
                # Fallback to top 5 if no LLM
                results = results[:5]
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

        @tool("search_files_by_name", description="Find files matching a pattern (e.g., '*.py', 'test_*').")
        def search_files_by_name(pattern: str):
            matches = []
            ignore = [".git", "__pycache__", ".venv", ".cortex", "node_modules"]
            
            for root, dirs, files in os.walk(self.project_path):
                dirs[:] = [d for d in dirs if d not in ignore]
                for file in files:
                    if fnmatch.fnmatch(file, pattern):
                        rel_path = os.path.relpath(os.path.join(root, file), self.project_path)
                        matches.append(rel_path)
            
            return "\n".join(matches[:30]) if matches else f"No files matching '{pattern}'"

        @tool("get_file_outline", description="Get classes and functions in a Python file without full content.")
        def get_file_outline(path: str):
            full_path = path if os.path.isabs(path) else os.path.join(self.project_path, path)
            
            try:
                with open(full_path, 'r') as f:
                    tree = ast.parse(f.read())
                
                outline = []
                for node in ast.iter_child_nodes(tree):
                    if isinstance(node, ast.ClassDef):
                        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        outline.append(f"class {node.name} (L{node.lineno}): {', '.join(methods)}")
                    elif isinstance(node, ast.FunctionDef):
                        outline.append(f"def {node.name}() (L{node.lineno})")
                
                return "\n".join(outline) if outline else "No classes/functions found"
            except Exception as e:
                return f"Error: {e}"

        @tool("grep_code", description="Search for exact regex patterns in files. Use for finding specific strings, function calls, or patterns that semantic search might miss.")
        def grep_code(pattern: str, file_pattern: str = "*.py"):
            """Search for regex pattern in files matching file_pattern."""
            matches = []
            ignore = [".git", "__pycache__", ".venv", ".cortex", "node_modules"]
            
            try:
                compiled_pattern = re.compile(pattern)
            except re.error as e:
                return f"Invalid regex pattern: {e}"
            
            for root, dirs, files in os.walk(self.project_path):
                dirs[:] = [d for d in dirs if d not in ignore]
                for file in files:
                    if fnmatch.fnmatch(file, file_pattern):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.project_path)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                for line_num, line in enumerate(f, 1):
                                    if compiled_pattern.search(line):
                                        matches.append(f"{rel_path}:{line_num}: {line.strip()}")
                        except Exception:
                            continue
            
            if not matches:
                return f"No matches found for pattern '{pattern}' in {file_pattern} files"
            
            return "\n".join(matches[:50])  # Limit to 50 matches

        # ============================================================
        # WRITE TOOLS 
        # ============================================================
        
        # @tool("write_file", description="Write content to a file. Creates the file if it doesn't exist. Use for creating new files or modifying existing ones.")
        # def write_file(path: str, content: str):
        #     """Write content to a file, creating directories if needed."""
        #     full_path = path if os.path.isabs(path) else os.path.join(self.project_path, path)
        #     
        #     # Safety check: don't write outside project
        #     if not os.path.abspath(full_path).startswith(self.project_path):
        #         return f"Error: Cannot write outside project directory"
        #     
        #     try:
        #         # Create backup if file exists
        #         if os.path.exists(full_path):
        #             backup_path = full_path + ".bak"
        #             with open(full_path, 'r') as f:
        #                 with open(backup_path, 'w') as backup:
        #                     backup.write(f.read())
        #         
        #         # Create directory if needed
        #         os.makedirs(os.path.dirname(full_path), exist_ok=True)
        #         
        #         with open(full_path, 'w') as f:
        #             f.write(content)
        #         
        #         return f"Successfully wrote {len(content)} characters to {path}"
        #     except Exception as e:
        #         return f"Error writing file: {e}"

        # @tool("run_command", description="Run a shell command in the project directory. Use for testing, building, or running scripts. Commands have a 30 second timeout.")
        # def run_command(command: str):
        #     """Run a shell command with timeout and safety checks."""
        #     # Safety check: block dangerous commands
        #     dangerous = ["rm -rf", "sudo", "mkfs", "dd if=", "> /dev/"]
        #     for d in dangerous:
        #         if d in command:
        #             return f"Error: Command blocked for safety (contains '{d}')"
        #     
        #     try:
        #         result = subprocess.run(
        #             command,
        #             shell=True,
        #             cwd=self.project_path,
        #             capture_output=True,
        #             text=True,
        #             timeout=30
        #         )
        #         
        #         output = ""
        #         if result.stdout:
        #             output += f"STDOUT:\n{result.stdout}\n"
        #         if result.stderr:
        #             output += f"STDERR:\n{result.stderr}\n"
        #         output += f"Exit code: {result.returncode}"
        #         
        #         return output if output else "Command completed with no output"
        #     except subprocess.TimeoutExpired:
        #         return "Error: Command timed out after 30 seconds"
        #     except Exception as e:
        #         return f"Error running command: {e}"

        # Return only read-only exploration tools
        exploration_tools = [search_code, read_file, get_symbol_info, find_references, 
                            list_files, search_files_by_name, get_file_outline, grep_code]
        
        return exploration_tools  # Read-only tools only
    
    def get_exploration_tools(self):
        """Get tools suitable for exploration tasks (all tools are exploration now)."""
        return self.get_tools()
    
    def get_builder_tools(self):
        """Get tools suitable for building/writing tasks. Currently returns read-only tools."""
        # Builder tools disabled - agent is read-only
        return self.get_tools()



