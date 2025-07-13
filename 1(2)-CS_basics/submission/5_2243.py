from typing import TypeVar, Generic, Callable, List

U = TypeVar('U')

class SegmentTree(Generic[U]):
    def __init__(self, arr: List[U], func: Callable[[U, U], U], identity: U) -> None:
        """
        arr: 초기 데이터 리스트
        func: 구간 합성 함수 (예: 합, 최소, 최대)
        identity: func의 항등원 (예: 합일 때 0, 최소일 때 큰 값)
        """
        n = 1
        while n < len(arr):
            n <<= 1
        self.n: int = n
        self.tree: List[U] = [identity] * (2 * self.n)
        self.func: Callable[[U, U], U] = func
        self.identity: U = identity

        # 리프 노드 초기화
        for i in range(len(arr)):
            self.tree[self.n + i] = arr[i]

        # 내부 노드 초기화
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.func(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, idx: int, val: U) -> None:
        """idx번째 원소를 val로 변경"""
        idx += self.n
        self.tree[idx] = val
        idx //= 2
        while idx > 0:
            self.tree[idx] = self.func(self.tree[2 * idx], self.tree[2 * idx + 1])
            idx //= 2

    def query(self, left: int, right: int) -> U:
        """[left, right] 구간의 합성 함수 결과 반환"""
        left += self.n
        right += self.n
        res_left = self.identity
        res_right = self.identity

        while left <= right:
            if left % 2 == 1:
                res_left = self.func(res_left, self.tree[left])
                left += 1
            if right % 2 == 0:
                res_right = self.func(self.tree[right], res_right)
                right -= 1
            left //= 2
            right //= 2

        return self.func(res_left, res_right)


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