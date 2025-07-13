from lib import SegmentTree
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
