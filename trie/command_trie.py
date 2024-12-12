from typing import Callable, Optional, Tuple

from trie.trie_node import TrieNode


class CommandTrie:
    def __init__(self):
        self.root: TrieNode = TrieNode()

    def insert(self, command: str, func: Callable[[], None]) -> None:
        node = self.root
        for char in command:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.command = func

    def search(self, command: str) -> Tuple[Optional[Callable[[], None]], bool]:
        node = self.root
        for char in command:
            if char not in node.children:
                return None, False
            node = node.children[char]
        return node.command, True
