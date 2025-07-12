from lib import SegmentTree
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