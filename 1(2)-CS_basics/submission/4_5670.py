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
from typing import Optional

def count(trie: Trie, query_seq: str) -> int:
    pointer: int = 0
    cnt = 0

    for element in query_seq:
        # 버튼 누르는 조건: 분기점이거나 단어 끝
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        # 다음 노드 인덱스 찾기
        new_index: Optional[int] = None
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break

        if new_index is None:
            # 일치하는 자식이 없으면 중단 (필요에 따라 예외 처리 가능)
            break

        pointer = new_index

    # 시작할 때 첫 글자는 무조건 눌러야 함
    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    input = sys.stdin.readline

    while True:
        n = input()
        if not n:
            break
        n = int(n)
        words = [input().strip() for _ in range(n)]

        trie: Trie = Trie()
        for w in words:
            trie.push(w)

        total_presses = 0
        for w in words:
            total_presses += count(trie, w)

        avg = total_presses / n
        print(f"{avg:.2f}")


if __name__ == "__main__":
    main()
