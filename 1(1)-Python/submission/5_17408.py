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
input = sys.stdin.readline


class Pair(tuple[int, int]):
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: 'Pair', b: 'Pair') -> 'Pair':
        # 두 구간에서 가장 큰 값 2개를 뽑아 합침
        candidates = sorted([a[0], a[1], b[0], b[1]], reverse=True)
        return Pair(candidates[0], candidates[1])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    n = int(input())
    arr = list(map(int, input().split()))
    m = int(input())

    arr_pair = [Pair.f_conv(x) for x in arr]
    st = SegmentTree(arr_pair, Pair.f_merge, Pair.default())

    for _ in range(m):
        query = list(map(int, input().split()))
        if query[0] == 1:
            # 업데이트
            i, v = query[1], query[2]
            st.update(i - 1, Pair.f_conv(v))
        else:
            # 구간 쿼리
            l, r = query[1], query[2]
            res = st.query(l - 1, r - 1)
            print(res.sum())


if __name__ == "__main__":
    main()
