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



def simulate_card_game(n: int) -> int:
    """
    가장 위에 있는 카드를 버리고, 그 다음 카드를 아래로 이동

    Args:
        n (int): 카드의 개수

    Returns:
        int: 마지막으로 남은 카드
    """
    q = create_circular_queue(n)
    while len(q) > 1:
        q.popleft()
        q.append(q.popleft())
    return q[0]

def solve_card2() -> None:
    """입, 출력 format"""
    n: int = int(input())
    result: int = simulate_card_game(n)
    print(result)

if __name__ == "__main__":
    solve_card2()