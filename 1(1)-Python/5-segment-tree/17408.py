from lib import SegmentTree
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
