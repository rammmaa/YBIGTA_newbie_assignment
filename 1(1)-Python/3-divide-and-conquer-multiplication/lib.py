from __future__ import annotations
import copy

class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix:
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        """
        행렬 요소 설정, 값은 MOD로 나눈 나머지를 저장

        Args:
            key (tuple[int, int]): _(행, 열)
            value (int): 저장할 값
        """        
        row, col = key
        self.matrix[row][col] = value % self.MOD


    def __matmul__(self, matrix: Matrix) -> Matrix:
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]

        return result

    def __pow__(self, n: int) -> Matrix:
        """
        행렬의 거듭제곱 연산

        Args:
            n (int): 지수(0 이상)

        Returns:
            Matrix: 거듭제곱한 결과 행렬
        """    
        assert n >= 0
        result = Matrix.eye(self.shape[0])
        base = self.clone()

        while n > 0:
            if n & 1:
                result = result @ base
            base = base @ base
            n >>= 1

        return result


    def __repr__(self) -> str:
        """
        행렬 > 문자열 변환

        Returns:
            str: 행렬을 변환한 문자열
        """        
        rows = [" ".join(str(x) for x in row) for row in self.matrix]
        return "\n".join(rows)