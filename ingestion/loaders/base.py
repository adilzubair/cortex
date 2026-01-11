from dataclasses import dataclass
from typing import Dict

@dataclass
class IngestedDocument:
    content: str
    metadata: Dict
