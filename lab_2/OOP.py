# ООП СТИЛЬ (классы)

class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    # Сложение матриц
    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            return "ОШИБКА: размеры не совпадают"

        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            result.append(row)
        return Matrix(result)

    # Умножение (на матрицу или скаляр)
    def __mul__(self, other):
        if isinstance(other, (int, float)):  # Умножение на число
            result = []
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    row.append(self.data[i][j] * other)
                result.append(row)
            return Matrix(result)
        else:  # Умножение на матрицу
            if self.cols != other.rows:
                return "ОШИБКА: нельзя умножить"

            result = []
            for i in range(self.rows):
                row = []
                for j in range(other.cols):
                    sum_val = 0
                    for k in range(self.cols):
                        sum_val += self.data[i][k] * other.data[k][j]
                    row.append(sum_val)
                result.append(row)
            return Matrix(result)

    # Транспонирование
    def transpose(self):
        result = []
        for j in range(self.cols):
            row = []
            for i in range(self.rows):
                row.append(self.data[i][j])
            result.append(row)
        return Matrix(result)

    def __str__(self):
        lines = []
        for row in self.data:
            line = " ".join(f"{x:4}" for x in row)
            lines.append(line)
        return "\n".join(lines)


print("=" * 40)
print("ООП СТИЛЬ")
print("=" * 40)

# Создаем матрицы
A = Matrix([[1, 2, 3],
            [4, 5, 6]])
B = Matrix([[2, 0, 1],
            [1, 2, 3]])
C = Matrix([[1, 2],
            [3, 4],
            [5, 6]])

print("Матрица A (2x3):")
print(A)
print("\nМатрица B (2x3):")
print(B)
print("\nМатрица C (3x2):")
print(C)

# Сложение
print("\n1. Сложение A + B:")
print(A + B)

print("Сложение A + C:")
print(A + C)

# Умножение на скаляр
print("\n2. Умножение A * 2:")
print(A * 2)

print("Умножение B * 2:")
print(B * 2)

print("Умножение C * 2:")
print(C * 2)

# Умножение матриц
print("\n3. Умножение матриц A * C:")
print(A * C)

print("Умножение матриц B * C:")
print(B * C)

# Транспонирование
print("\n4. Транспонирование A:")
print(A.transpose())
print("Транспонирование B:")
print(B.transpose())
print("Транспонирование C:")
print(C.transpose())