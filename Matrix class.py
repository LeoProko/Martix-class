from sys import stdin


class MatrixError(BaseException):
    def __init__(self, a1, a2):
        self.matrix1 = Matrix(a1.arr)
        self.matrix2 = Matrix(a2.arr)


class Matrix:
    def __init__(self, arr):
        self.arr = arr[:]

    def __str__(self):
        return '\n'.join(['\t'.join(map(str, line)) for line in self.arr])

    def __add__(self, other):
        if self.size() == other.size():
            return Matrix(
                list(
                    map(
                        lambda x: list(
                            map(
                                lambda y: y[0] + y[1],
                                x
                            )
                        ),
                        map(
                            lambda x, y: list(zip(x, y)),
                            self.arr, other.arr
                        )
                    )
                )
            )
        else:
            raise MatrixError(self, other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Matrix(
                list(
                    map(
                        lambda x: list(
                            map(
                                lambda y: other * y,
                                x
                            )
                        ),
                        self.arr
                    )
                )
            )

    __rmul__ = __mul__

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.size()[1] == other.size()[0]:
                a = len(self.arr)
                b = len(other.arr)
                c = len(other.arr[0])
                marr = []
                for i in range(a):
                    foo = []
                    for j in range(c):
                        foo.append(0)
                    marr.append(foo)
                for i in range(a):
                    for j in range(c):
                        for k in range(b):
                            marr[i][j] += self.arr[i][k] * other.arr[k][j]
                return Matrix(marr)
            else:
                raise MatrixError(self, other)
        else:
            raise MatrixError(self, other)

    def size(self):
        return len(self.arr), len(self.arr[0])

    def transposed(self):
        return Matrix(list(map(lambda x: list(x), zip(*self.arr))))

    def transpose(self):
        arr_t = list(map(lambda x: list(x), zip(*self.arr)))
        self.arr = arr_t
        return Matrix(self.arr)

    def solve(self, b):
        def find_no_zero(a):
            for i in range(len(a) - 1):
                if a[i] != 0:
                    return i
            return -1

        def is_e(a):
            j = i = 0
            while j < len(a) and i < len(a[0]):
                if a[i][j] != 1:
                    return -1
                i += 1
                j += 1
            return 1

        def e1(arr, i, j, l):
            arr[i] = list(map(lambda x, y: x + y, arr[i],
                              map(lambda x: x * l, arr[j])))

        def e3(arr, i, l):
            arr[i] = list(map(lambda x: x * l, arr[i]))

        a = [line.copy() for line in self.arr]

        for i in range(len(a)):
            a[i].append(b[i])
        for i in range(len(a)):
            t = find_no_zero(a[i])
            if t != -1:
                e3(a, i, 1 / a[i][t])
                for j in range(i + 1, len(a) - 1):
                    e1(a, j, i, -a[j][t])
        a.sort()
        for i in range(len(a)):
            t = find_no_zero(a[i])
            for j in range(i + 1, len(a)):
                e1(a, j, i, -a[j][t])
        a.sort(reverse=True)
        if is_e(a) == 1:
            return list(map(lambda x: x[-1], a))
        else:
            raise MatrixError(self, b)


class SquareMatrix(Matrix):
    def __pow__(self, power, modulo=None):
        a = self.arr[:]
        if power == 0:
            t = []
            j = 0
            for i in range(len(a)):
                h = [0] * len(a[0])
                if j < len(a[0]):
                    h[j] = 1
                j += 1
                t.append(h)
            return SquareMatrix(t)
        elif power % 2 == 0:

            return SquareMatrix((self * self).arr) ** (power // 2)
        else:
            return self * (self ** (power - 1))


exec(stdin.read())

