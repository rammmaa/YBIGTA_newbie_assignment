from lib import create_circular_queue, rotate_and_remove


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