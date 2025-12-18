print("\n" + "=" * 50)
print("ФУНКЦИОНАЛЬНЫЙ СТИЛЬ")
print("=" * 50)


# Создание матрицы
def create_matrix(data):
    return {
        'data': data,
        'rows': len(data),
        'cols': len(data[0])
    }


# Сложение матриц
def add_matrices(m1, m2):
    if m1['rows'] != m2['rows'] or m1['cols'] != m2['cols']:
        return f"ОШИБКА: размеры не совпадают ({m1['rows']}x{m1['cols']} != {m2['rows']}x{m2['cols']})"

    result = []
    for i in range(m1['rows']):
        row = []
        for j in range(m1['cols']):
            row.append(m1['data'][i][j] + m2['data'][i][j])
        result.append(row)
    return create_matrix(result)


# Умножение на скаляр
def multiply_scalar(m, scalar):
    result = []
    for i in range(m['rows']):
        row = []
        for j in range(m['cols']):
            row.append(m['data'][i][j] * scalar)
        result.append(row)
    return create_matrix(result)


# Умножение матриц
def multiply_matrices(m1, m2):
    if m1['cols'] != m2['rows']:
        return f"ОШИБКА: нельзя умножить {m1['rows']}x{m1['cols']} * {m2['rows']}x{m2['cols']}"

    result = []
    for i in range(m1['rows']):
        row = []
        for j in range(m2['cols']):
            sum_val = 0
            for k in range(m1['cols']):
                sum_val += m1['data'][i][k] * m2['data'][k][j]
            row.append(sum_val)
        result.append(row)
    return create_matrix(result)


# Транспонирование
def transpose_matrix(m):
    result = []
    for j in range(m['cols']):
        row = []
        for i in range(m['rows']):
            row.append(m['data'][i][j])
        result.append(row)
    return create_matrix(result)


# Вывод матрицы
def matrix_to_string(m):
    if isinstance(m, dict):
        lines = []
        for row in m['data']:
            line = " ".join(f"{x:6}" for x in row)
            lines.append(line)
        return "\n".join(lines)
    else:
        return str(m)


# Создаем матрицы
A_func = create_matrix([[1, 2, 3],
                        [4, 5, 6]])  # 2x3

B_func = create_matrix([[2, 0, 1],
                        [1, 2, 3]])  # 2x3

C_func = create_matrix([[1, 2],
                        [3, 4],
                        [5, 6]])  # 3x2

print("Матрица A (2x3):")
print(matrix_to_string(A_func))
print("\nМатрица B (2x3):")
print(matrix_to_string(B_func))
print("\nМатрица C (3x2):")
print(matrix_to_string(C_func))

# Все операции между матрицами
print("\n" + "=" * 50)
print("ВСЕ ОПЕРАЦИИ МЕЖДУ МАТРИЦАМИ (Функциональный):")
print("=" * 50)

# 1. Сложение A + B
print("\n1. Сложение A + B:")
result = add_matrices(A_func, B_func)
print(matrix_to_string(result))

#Попытка сложить A + C
print("Попытка сложить A + C:")
result = add_matrices(A_func, C_func)
print(result)

# 2. Умножение A * C
print("\n2. Умножение A * C:")
result = multiply_matrices(A_func, C_func)
print(matrix_to_string(result))

# Умножение B * C
print("Умножение B * C:")
result = multiply_matrices(B_func, C_func)
print(matrix_to_string(result))

# 3. Умножение на скаляр
print("\n3. Умножение матрицы A на скаляр 2:")
result = multiply_scalar(A_func, 2)
print(matrix_to_string(result))

print("Умножение матрицы B на скаляр 2:")
result = multiply_scalar(B_func, 2)
print(matrix_to_string(result))

print("Умножение матрицы C на скаляр 2:")
result = multiply_scalar(C_func, 2)
print(matrix_to_string(result))


# 4. Транспонирование
print("\n4. Транспонирование матрицы A:")
result = transpose_matrix(A_func)
print(matrix_to_string(result))

print("Транспонирование матрицы B:")
result = transpose_matrix(B_func)
print(matrix_to_string(result))

print("Транспонирование матрицы C:")
result = transpose_matrix(C_func)
print(matrix_to_string(result))
