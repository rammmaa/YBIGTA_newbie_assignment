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

MOD = 1_000_000_007

def factorial_up_to(n: int):
    """
    1부터 n+1까지의 팩토리얼 값을 미리 계산하여 리스트로 반환
    각 팩토리얼 값은 MOD(1,000,000,007)로 나눈 나머지를 사용

    Args:
        n (int): 계산할 최대 팩토리얼 수

    Returns:
        list[int]: 0부터 n+1까지의 팩토리얼 값을 담은 리스트
    """
    facto = [1] * (n+2)
    for i in range(2, n+2):
        facto[i] = (facto[i-1] * i) % MOD
    return facto

def main() -> None:
    input = sys.stdin.readline

    n = int(input())
    names = [input().rstrip() for _ in range(n)]
    names.sort()

    facto = factorial_up_to(n)

    queue = [(0, n, 0)]  
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
