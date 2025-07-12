from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    def __init__(self, arr: List[T], func: Callable[[U, U], U], identity: U) -> None:
        """
        arr: 초기 데이터 리스트
        func: 구간 합성 함수 (예: 합, 최소, 최대)
        identity: func의 항등원 (예: 합일 때 0, 최소일 때 큰 값)
        """
        n = 1
        while n < len(arr):
            n <<= 1
        self.n = n
        self.tree: List[U] = [identity] * (2 * self.n)
        self.func = func
        self.identity = identity

        # 리프 노드 초기화
        for i in range(len(arr)):
            self.tree[self.n + i] = arr[i]  # arr[i]가 U 타입이라고 가정

        # 내부 노드 초기화
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.func(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, idx: int, val: U) -> None:
        """
        idx: 0-based 인덱스
        val: 변경할 값
        """
        idx += self.n
        self.tree[idx] = val
        while idx > 1:
            idx >>= 1
            self.tree[idx] = self.func(self.tree[2 * idx], self.tree[2 * idx + 1])

    def query(self, l: int, r: int) -> U:
        """
        [l, r] 구간 질의 (0-based, 양끝 포함)
        """
        ret_left = self.identity
        ret_right = self.identity
        l += self.n
        r += self.n
        while l <= r:
            if l & 1:
                ret_left = self.func(ret_left, self.tree[l])
                l += 1
            if not (r & 1):
                ret_right = self.func(self.tree[r], ret_right)
                r -= 1
            l >>= 1
            r >>= 1
        return self.func(ret_left, ret_right)


import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""

MAX_TASTE = 1_000_000

def query_kth(st: SegmentTree, k: int) -> int:
    idx = 1
    while idx < st.n:
        left = st.tree[2 * idx]
        if left >= k:
            idx = 2 * idx
        else:
            k -= left
            idx = 2 * idx + 1
    return idx - st.n  # 0-based 인덱스 반환

def main() -> None:
    n = int(input())
    arr = [0] * MAX_TASTE
    st = SegmentTree(arr, lambda a, b: a + b, 0)

    for _ in range(n):
        cmd = list(map(int, input().split()))
        if cmd[0] == 1:
            k = cmd[1]
            taste_idx = query_kth(st, k)
            print(taste_idx + 1)  # 맛 번호는 1-based
            # 현재 값 읽기
            current_val = st.query(taste_idx, taste_idx)
            st.update(taste_idx, current_val - 1)  # 1개 줄이기
        else:
            taste, cnt = cmd[1], cmd[2]
            taste_idx = taste - 1
            current_val = st.query(taste_idx, taste_idx)
            st.update(taste_idx, current_val + cnt)

if __name__ == "__main__":
    main()