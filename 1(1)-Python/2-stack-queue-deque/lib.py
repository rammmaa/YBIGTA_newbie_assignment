from __future__ import annotations
from collections import deque

def create_circular_queue(n: int) -> deque[int]:
    """
    1~n 연속된 정수로 이루어진 deque 생성

    Args:
        n (int): deque에서의 최댓값

    Returns:
        deque[int]: 1~n 연속된 정수로 이루어진 deque
    """
    return deque(range(1, n + 1))

def rotate_and_remove(queue: deque[int], k: int) -> int:
    """
    deque를 k-1만큼 앞으로 회전시킨 뒤, 가장 앞에 있는 요소를 popleft()
    Args:
        queue (deque[int]): 회전시킬 deque
        k (int): 회전수

    Returns:
        int: 제거된 요소의 값
    """
    queue.rotate(-(k - 1))
    removed = queue.popleft()
    return removed