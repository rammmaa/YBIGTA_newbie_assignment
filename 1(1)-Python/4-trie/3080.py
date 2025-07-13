from lib import Trie
import sys

MOD = 1_000_000_007

def factorial_up_to(n: int):
    """
    1부터 n+1까지의 팩토리얼 값을 미리 계산하여 리스트로 반환
    각 팩토리얼 값은 MOD(1,000,000,007)로 나눈 나머지를 사용

    Args:
        n (int): 계산할 최대 팩토리얼 수

    Returns:
        list[int]: 0부터 n+1까지의 팩토리얼 값을 담은 리스트
    """
    facto = [1] * (n+2)
    for i in range(2, n+2):
        facto[i] = (facto[i-1] * i) % MOD
    return facto

def main() -> None:
    input = sys.stdin.readline

    n = int(input())
    names = [input().rstrip() for _ in range(n)]
    names.sort()

    facto = factorial_up_to(n)

    queue = [(0, n, 0)]  
    result = 1

    while queue:
        s, e, idx = queue.pop(0)
        group_count = 0
        check_short = False

        i = s
        while i < e:
            if len(names[i]) <= idx:
                check_short = True
                i += 1
                continue

            current_char = names[i][idx]
            start_group = i
            i += 1
            while i < e and len(names[i]) > idx and names[i][idx] == current_char:
                i += 1

            queue.append((start_group, i, idx + 1))
            group_count += 1

        if check_short:
            group_count += 1

        result = (result * facto[group_count]) % MOD

    print(result)

if __name__ == "__main__":
    main()
