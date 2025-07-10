from __future__ import annotations
import copy
from collections import deque
from collections import defaultdict
from typing import DefaultDict, List


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
    def __init__(self, n: int) -> None:
        """
        무방향 그래프 생성

        Args:
            n (int): 노드의 개수
        """        
        self.n = n
        self.graph: DefaultDict[int, List[int]] = defaultdict(list)
    
    def add_edge(self, u: int, v: int) -> None:
        """
        두 노드 u, v를 연결하는 간선을 추가

        Args:
            u (int): 간선의 한쪽 노드
            v (int): 다른쪽 노드
        """
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def dfs(self, start: int) -> list[int]:
        """
        dfs 수행, 방문 순서대로 노드 리스트 반환

        Args:
            start (int): 시작 노드

        Returns:
            list[int]: 방문 순서대로 노드 번호 리스트
        """    
        visited = set()
        result = []
        stack: deque[int] = deque()
        stack.append(start)

        while stack:
            node = stack.pop()  
            if node not in visited:
                visited.add(node)
                result.append(node)
                for n in sorted(self.graph[node], reverse=True):
                    if n not in visited:
                        stack.append(n)
        return result
    
    def bfs(self, start: int) -> list[int]:
        """
        BFS를 수행하여 방문 순서대로 노드 리스트 반환

        Args:
            start (int): 시작 노드

        Returns:
            list[int]: 방문 순서대로 노드 번호 리스트
        """
        visited = set()
        result = []
        queue: deque[int] = deque()
        queue.append(start)

        while queue:
            node = queue.popleft()  
            if node not in visited:
                visited.add(node)
                result.append(node)
                for n in sorted(self.graph[node]):
                    if n not in visited:
                        queue.append(n)
        return result
    
    def search_and_print(self, start: int) -> None:
        """
        시작 노드부터 dfs, bsf 수행 후 각각의 방문 순서 출력

        Args:
            start (int): 시작 노드
        """
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))