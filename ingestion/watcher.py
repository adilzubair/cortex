import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ingestion.pipeline import index_file
from indexing.indexer import Indexer
from indexing.state import StateManager

class CodebaseHandler(FileSystemEventHandler):
    def __init__(self, source_root: str):
        self.source_root = os.path.abspath(source_root)
        self.indexer = Indexer()
        self.state_manager = StateManager()

    def on_modified(self, event):
        if not event.is_directory:
            try:
                index_file(event.src_path, self.source_root, self.indexer, self.state_manager)
            except Exception as e:
                print(f"Error handling modification for {event.src_path}: {e}")

    def on_created(self, event):
        if not event.is_directory:
            try:
                index_file(event.src_path, self.source_root, self.indexer, self.state_manager)
            except Exception as e:
                print(f"Error handling creation for {event.src_path}: {e}")

def start_watching(path: str):
    print(f"Starting to watch for changes in: {os.path.abspath(path)}")
    event_handler = CodebaseHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def start_background_watcher(path: str):
    """Starts the watcher in a non-blocking way."""
    event_handler = CodebaseHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    return observer
