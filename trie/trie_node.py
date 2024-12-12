from typing import Dict, Callable, Optional


class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.command: Optional[Callable[[], None]] = None
