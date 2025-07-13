from lib import SegmentTree
import sys

MAX_TASTE = 1_000_000

def query_kth(st: SegmentTree[int, int], k: int) -> int:
    """
    k번째 사탕의 맛 점수 인덱스를 찾아 반환

    Args:
        st (SegmentTree): 사탕의 개수를 저장한 세그먼트 트리
        k (int): 찾고자 하는 k번째 사탕 (1-based index)

    Returns:
        int: k번째 사탕의 맛 점수 인덱스 (0-based)
    """
    idx = 1
    while idx < st.n:
        left = st.tree[2 * idx]
        if left >= k:
            idx = 2 * idx
        else:
            k -= left
            idx = 2 * idx + 1
    return idx - st.n

def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = [0] * MAX_TASTE
    st = SegmentTree[int, int](arr, lambda a, b: a + b, 0, convert=lambda x: x)

    for _ in range(n):
        cmd = list(map(int, input().split()))
        if cmd[0] == 1:
            k = cmd[1]
            taste_idx = query_kth(st, k)
            print(taste_idx + 1)
            current_val = st.query(taste_idx, taste_idx)
            st.update(taste_idx, current_val - 1)
        else:
            taste, cnt = cmd[1], cmd[2]
            taste_idx = taste - 1
            current_val = st.query(taste_idx, taste_idx)
            st.update(taste_idx, current_val + cnt)

if __name__ == "__main__":
    main()
