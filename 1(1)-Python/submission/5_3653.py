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
input = sys.stdin.readline

def main():
    T = int(input())
    MAX = 200_000

    for _ in range(T):
        n, m = map(int, input().split())
        movies = list(map(int, input().split()))

        size = n + m
        arr = [0] * size
        pos = [0] * (n + 1)

        for i in range(1, n + 1):
            pos[i] = n - i
            arr[pos[i]] = 1

        st = SegmentTree[int, int](arr, lambda a, b: a + b, 0, lambda x: x)

        curr_top = n 

        res = []

        for movie in movies:
            cur_pos = pos[movie]

            count_above = 0
            if cur_pos < curr_top:
                count_above = st.query(cur_pos + 1, curr_top - 1)

            res.append(count_above)

            current_val = st.query(cur_pos, cur_pos)
            st.update(cur_pos, current_val - 1)

            st.update(curr_top, 1)
            pos[movie] = curr_top
            curr_top += 1

        print(" ".join(map(str, res)))

if __name__ == "__main__":
    main()
