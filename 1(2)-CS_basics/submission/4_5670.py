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
    """
    Trie의 각 노드를 표현하는 클래스

    Attributes:
        body (Optional[T]): 해당 노드가 저장하고 있는 값 (문자 하나 등)
        children (list[int]): 자식 노드들의 인덱스를 저장한 리스트
        is_end (bool): 단어가 이 노드에서 끝나는지를 나타내는 플래그
    """
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    """
    Trie 자료구조 클래스
    - 리스트를 상속하여 TrieNode들을 인덱스로 관리
    - 루트 노드는 body=None인 노드로 초기화됨
    """
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        주어진 시퀀스를 Trie에 삽입

        Args:
            seq (Iterable[T]): 삽입할 문자열이나 시퀀스 
        """
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

def count(trie: Trie, query_seq: str) -> int:
    """
    주어진 문자열을 입력할 때, 자동완성이 작동하지 않아 직접 눌러야 하는 
    최소 키 입력 횟수를 계산

    자동완성 기준:
    - 현재 노드가 여러 자식을 가질 경우
    - 현재 노드가 단어의 끝일 경우

    Args:
        trie (Trie): 단어들이 저장된 Trie 자료구조
        query_seq (str): 키 입력 횟수를 구하고자 하는 단어

    Returns:
        int: 해당 단어를 입력할 때 필요한 최소 키 입력 수
    """
    pointer: int = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index: Optional[int] = None
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break

        if new_index is None:
            break

        pointer = new_index

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
