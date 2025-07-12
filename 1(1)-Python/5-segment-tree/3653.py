from lib import SegmentTree
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
