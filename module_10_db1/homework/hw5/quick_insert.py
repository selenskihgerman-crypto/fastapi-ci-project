def find_insert_position(arr, x):
    """Находит позицию для вставки x в отсортированный массив arr"""
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < x:
            left = mid + 1
        else:
            right = mid
    return left

# Тесты
A = [1, 2, 3, 3, 3, 5]
x = 4
assert find_insert_position(A, x) == 5
A.insert(5, x)
assert A == sorted(A)

# Крайние случаи
assert find_insert_position([], 1) == 0  # Пустой массив
assert find_insert_position([2, 3, 5], 1) == 0  # Вставка в начало
assert find_insert_position([2, 3, 5], 6) == 3  # Вставка в конец
assert find_insert_position([1, 2, 2, 2, 3], 2) == 1  # Вставка среди дубликатов
