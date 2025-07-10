from lib import create_circular_queue

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