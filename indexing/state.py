import sqlite3
import hashlib
import os
from datetime import datetime

from core.config import get_state_db_path

class StateManager:
    def __init__(self, project_path: str = ".", db_path: str = None):
        if db_path is None:
            self.db_path = get_state_db_path(project_path)
        else:
            self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_states (
                    path TEXT PRIMARY KEY,
                    hash TEXT NOT NULL,
                    last_indexed TEXT NOT NULL
                )
            """)

    def get_file_hash(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def has_changed(self, file_path):
        current_hash = self.get_file_hash(file_path)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT hash FROM file_states WHERE path = ?", (file_path,))
            row = cursor.fetchone()
            if row is None or row[0] != current_hash:
                return True, current_hash
            return False, current_hash

    def update_state(self, file_path, file_hash):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO file_states (path, hash, last_indexed) VALUES (?, ?, ?)",
                (file_path, file_hash, datetime.now().isoformat())
            )