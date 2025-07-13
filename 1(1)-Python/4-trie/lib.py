from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        node_idx = 0

        for element in seq:
            curr_node = self[node_idx]

            found = False
            for child_idx in curr_node.children:
                if self[child_idx].body == element:
                    node_idx = child_idx
                    found = True
                    break

            if not found:
                new_node = TrieNode(body=element)
                self.append(new_node)
                new_idx = len(self) - 1
                curr_node.children.append(new_idx)
                node_idx = new_idx

        self[node_idx].is_end = True