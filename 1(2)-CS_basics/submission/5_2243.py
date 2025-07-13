from __future__ import annotations
from typing import TypeVar, Generic, Callable, List

T = TypeVar("T")  
U = TypeVar("U") 

class SegmentTree(Generic[T, U]):
    def __init__(
        self,
        arr: List[T],
        merge: Callable[[U, U], U],
        identity: U,
        convert: Callable[[T], U]
    ) -> None:
        """
        세그먼트 트리 초기화

        Args:
            arr (List[T]): 원본 입력 배열
            merge (Callable[[U, U], U]): 두 노드를 병합하는 함수
            identity (U): 항등원 (merge 연산에 영향 주지 않는 값)
            convert (Callable[[T], U], optional): 입력 배열 원소를 노드 타입으로 변환하는 함수
        """
        self.n = 1
        while self.n < len(arr):
            self.n <<= 1

        self.tree: List[U] = [identity for _ in range(2 * self.n)]
        self.merge = merge
        self.identity = identity

        for i in range(len(arr)):
            self.tree[self.n + i] = convert(arr[i])

        for i in range(self.n - 1, 0, -1):
            self.tree[i] = merge(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, idx: int, val: U) -> None:
        """
        idx 번째 값을 갱신 (val은 원본 타입 T)

        Args:
            idx (int): 0-based 인덱스
            val (T): 새로 갱신할 값
        """
        idx += self.n
        self.tree[idx] = val

        while idx > 1:
            idx //= 2
            self.tree[idx] = self.merge(self.tree[2 * idx], self.tree[2 * idx + 1])

    def query(self, l: int, r: int) -> U:
        """
        구간 [l, r]에 대한 질의

        Args:
            l (int): 왼쪽 인덱스 (0-based)
            r (int): 오른쪽 인덱스 (0-based)

        Returns:
            U: 구간 [l, r]에 대한 merge 결과
        """
        l += self.n
        r += self.n

        res_left = self.identity
        res_right = self.identity

        while l <= r:
            if l % 2 == 1:
                res_left = self.merge(res_left, self.tree[l])
                l += 1
            if r % 2 == 0:
                res_right = self.merge(self.tree[r], res_right)
                r -= 1
            l //= 2
            r //= 2

        return self.merge(res_left, res_right)



import sys

MAX_TASTE = 1_000_000

def query_kth(st: SegmentTree[int, int], k: int) -> int:
    """
    k번째 사탕의 맛 점수 인덱스를 찾아 반환

    Args:
        st (SegmentTree): 사탕의 개수를 저장한 세그먼트 트리
        k (int): 찾고자 하는 k번째 사탕 (1-based index)

    Returns:
        int: k번째 사탕의 맛 점수 인덱스 (0-based)
    """
    idx = 1
    while idx < st.n:
        left = st.tree[2 * idx]
        if left >= k:
            idx = 2 * idx
        else:
            k -= left
            idx = 2 * idx + 1
    return idx - st.n

def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = [0] * MAX_TASTE
    st = SegmentTree[int, int](arr, lambda a, b: a + b, 0, convert=lambda x: x)

    for _ in range(n):
        cmd = list(map(int, input().split()))
        if cmd[0] == 1:
            k = cmd[1]
            taste_idx = query_kth(st, k)
            print(taste_idx + 1)
            current_val = st.query(taste_idx, taste_idx)
            st.update(taste_idx, current_val - 1)
        else:
            taste, cnt = cmd[1], cmd[2]
            taste_idx = taste - 1
            current_val = st.query(taste_idx, taste_idx)
            st.update(taste_idx, current_val + cnt)

if __name__ == "__main__":
    main()
