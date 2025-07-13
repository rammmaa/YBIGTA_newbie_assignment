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

        for i in range(len(arr)):
            self.tree[self.n + i] = arr[i]

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