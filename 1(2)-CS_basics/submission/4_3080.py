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


import sys

MOD = 1_000_000_007

def factorial_up_to(n: int):
    facto = [1] * (n+2)
    for i in range(2, n+2):
        facto[i] = (facto[i-1] * i) % MOD
    return facto

def main():
    input = sys.stdin.readline

    n = int(input())
    names = [input().rstrip() for _ in range(n)]
    names.sort()

    facto = factorial_up_to(n)

    queue = [(0, n, 0)]  # list로 큐 흉내, pop(0) 써야 함. 비효율이지만 조건상 어쩔 수 없음.
    result = 1

    while queue:
        s, e, idx = queue.pop(0)
        group_count = 0
        check_short = False

        i = s
        while i < e:
            if len(names[i]) <= idx:
                check_short = True
                i += 1
                continue

            current_char = names[i][idx]
            start_group = i
            i += 1
            while i < e and len(names[i]) > idx and names[i][idx] == current_char:
                i += 1

            queue.append((start_group, i, idx + 1))
            group_count += 1

        if check_short:
            group_count += 1

        result = (result * facto[group_count]) % MOD

    print(result)

if __name__ == "__main__":
    main()
