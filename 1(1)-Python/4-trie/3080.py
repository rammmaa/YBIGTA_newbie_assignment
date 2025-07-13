import sys

MOD = 1_000_000_007

def factorial_up_to(n: int):
    facto = [1] * (n+2)
    for i in range(2, n+2):
        facto[i] = (facto[i-1] * i) % MOD
    return facto

def main():
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
