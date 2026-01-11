from dataclasses import dataclass
from typing import Dict

@dataclass
class Chunk:
    content: str
    metadata: Dict
    start_line: int = 0
    end_line: int = 0
