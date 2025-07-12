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




def josephus_problem(n: int, k: int) -> list[int]:
    """
    요세푸스의 문제 해결:
    q를 k-1만큼 돌려서 k번째 요소가 앞으로 오면, popleft()

    Args:
        n (int): _description_
        K (int): _description_

    Returns:
        list[int]: _description_
    """
    q = create_circular_queue(n)
    result = []

    while q:
        removed = rotate_and_remove(q, k)
        result.append(removed)
    return result
    

def solve_josephus() -> None:
    """입, 출력 format"""
    n: int
    k: int
    n, k = map(int, input().split())
    result: list[int] = josephus_problem(n, k)
    
    # 출력 형식: <3, 6, 2, 7, 5, 1, 4>
    print("<" + ", ".join(map(str, result)) + ">")

if __name__ == "__main__":
    solve_josephus()