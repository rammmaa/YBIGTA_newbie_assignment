from lib import Trie
import sys

def count(trie: Trie, query_seq: str) -> int:
    """
    주어진 문자열을 입력할 때, 자동완성이 작동하지 않아 직접 눌러야 하는 
    최소 키 입력 횟수를 계산

    자동완성 기준:
    - 현재 노드가 여러 자식을 가질 경우
    - 현재 노드가 단어의 끝일 경우

    Args:
        trie (Trie): 단어들이 저장된 Trie 자료구조
        query_seq (str): 키 입력 횟수를 구하고자 하는 단어

    Returns:
        int: 해당 단어를 입력할 때 필요한 최소 키 입력 수
    """
    pointer: int = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index: Optional[int] = None
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break

        if new_index is None:
            break

        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    input = sys.stdin.readline

    while True:
        n = input()
        if not n:
            break
        n = int(n)
        words = [input().strip() for _ in range(n)]

        trie: Trie = Trie()
        for w in words:
            trie.push(w)

        total_presses = 0
        for w in words:
            total_presses += count(trie, w)

        avg = total_presses / n
        print(f"{avg:.2f}")


if __name__ == "__main__":
    main()
