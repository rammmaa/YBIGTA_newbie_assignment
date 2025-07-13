from lib import SegmentTree
import sys
input = sys.stdin.readline


class Pair(tuple[int, int]):
    """
    최대값 2개를 저장
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        """
        새로운 Pair 객체 생성

        Args:
            a (int): 가장 큰 값
            b (int): 두 번째로 큰 값

        Returns:
            Pair: 생성된 Pair 객체
        """
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        세그먼트 트리의 기본값 반환 (값이 없을 때)

        Returns:
            Pair: (0, 0)
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        단일 정수를 Pair로 변환

        Args:
            w (int): 정수 값

        Returns:
            Pair: (w, 0) — 하나의 값만 있는 경우
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: 'Pair', b: 'Pair') -> 'Pair':
        """
        두 Pair를 병합하여 최대값 2개로 구성된 새로운 Pair를 반환

        Args:
            a (Pair): 왼쪽 자식의 Pair
            b (Pair): 오른쪽 자식의 Pair

        Returns:
            Pair: 두 구간에서 가장 큰 두 수
        """
        candidates = sorted([a[0], a[1], b[0], b[1]], reverse=True)
        return Pair(candidates[0], candidates[1])

    def sum(self) -> int:
        """
        현재 Pair의 두 값을 더해 반환

        Returns:
            int: self[0] + self[1]
        """
        return self[0] + self[1]


def main() -> None:
    n = int(input())
    arr = list(map(int, input().split()))
    m = int(input())

    arr_pair = [Pair.f_conv(x) for x in arr]
    st = SegmentTree[int, Pair](arr, Pair.f_merge, Pair.default(), convert=Pair.f_conv)

    for _ in range(m):
        query = list(map(int, input().split()))
        if query[0] == 1:
            i, v = query[1], query[2]
            st.update(i - 1, Pair.f_conv(v))
        else:
            l, r = query[1], query[2]
            res = st.query(l - 1, r - 1)
            print(res.sum())


if __name__ == "__main__":
    main()
