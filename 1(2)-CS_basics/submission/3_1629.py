# lib.py의 Matrix 클래스를 참조하지 않음
import sys

def fast_power(base: int, exp: int, mod: int) -> int:
    """
    분할 정복을 이용한 모듈러 거듭제곱 계산

    Args:
        base (int): 밑
        exp (int): 지수
        mod (int): 모듈러 값

    Returns:
        int: _(base^exp) % mod
    """
    if exp == 0:
        return 1
    result = fast_power(base, exp // 2, mod)
    result = (result * result) % mod
    if exp % 2:
        result = (result * base) % mod
    return result

def main() -> None:
    A: int
    B: int
    C: int
    A, B, C = map(int, input().split()) # 입력 고정
    
    result: int = fast_power(A, B, C) # 출력 형식
    print(result) 

if __name__ == "__main__":
    main()