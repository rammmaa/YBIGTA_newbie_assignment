from lib import Trie
import sys
from typing import Optional

def count(trie: Trie, query_seq: str) -> int:
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
