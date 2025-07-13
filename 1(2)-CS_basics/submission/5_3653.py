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
input = sys.stdin.readline

def solve():
    T = int(input())
    MAX = 200_000

    for _ in range(T):
        n, m = map(int, input().split())
        movies = list(map(int, input().split()))

        size = n + m
        arr = [0] * size
        pos = [0] * (n + 1)

        # 초기 위치 세팅: 영화 i 위치는 n - i (0-based)
        for i in range(1, n + 1):
            pos[i] = n - i
            arr[pos[i]] = 1

        st = SegmentTree(arr, lambda a, b: a + b, 0)
        curr_top = n  # 새로 올릴 DVD 위치 (0-based 인덱스)

        res = []

        for movie in movies:
            cur_pos = pos[movie]

            # 위에 있는 DVD 개수는 cur_pos+1 부터 curr_top-1까지 합
            count_above = 0
            if cur_pos < curr_top:
                count_above = st.query(cur_pos + 1, curr_top - 1)

            res.append(count_above)

            # 현재 위치 DVD 제거
            current_val = st.query(cur_pos, cur_pos)
            st.update(cur_pos, current_val - 1)

            # 가장 위로 올림
            st.update(curr_top, 1)
            pos[movie] = curr_top
            curr_top += 1

        print(" ".join(map(str, res)))

if __name__ == "__main__":
    solve()
