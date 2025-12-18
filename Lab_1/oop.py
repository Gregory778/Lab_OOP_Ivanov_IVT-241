from typing import Optional, List, TypeVar, Generic

T = TypeVar('T')


class Queue:
    """Очередь (FIFO) - ООП стиль"""

    def __init__(self):
        self.items: List[T] = []

    def enqueue(self, item: T) -> None:
        """Добавить элемент в очередь"""
        self.items.append(item)

    def dequeue(self) -> Optional[T]:
        """Взять элемент из очереди"""
        if self.is_empty():
            return None
        return self.items.pop(0)

    def peek(self) -> Optional[T]:
        """Посмотреть первый элемент"""
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return len(self.items) == 0

    def size(self) -> int:
        """Размер очереди"""
        return len(self.items)

    def __str__(self):
        return f"Очередь: {self.items}"


class Stack:
    """Стек (LIFO) - ООП стиль"""

    def __init__(self):
        self.items: List[T] = []

    def push(self, item: T) -> None:
        """Добавить элемент в стек"""
        self.items.append(item)

    def pop(self) -> Optional[T]:
        """Взять элемент из стека"""
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self) -> Optional[T]:
        """Посмотреть верхний элемент"""
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return len(self.items) == 0

    def size(self) -> int:
        """Размер стека"""
        return len(self.items)

    def __str__(self):
        return f"Стек: {self.items}"


# Тестируем ООП
print("=== ООП СТИЛЬ ===")

# Очередь
print("\n1. Очередь (Queue):")
q = Queue()
q.enqueue("первый")
q.enqueue("второй")
q.enqueue("третий")
print(q)
print(f"Первый в очереди: {q.peek()}")
print(f"Извлекаем: {q.dequeue()}")
print(f"Теперь первый: {q.peek()}")
print(f"Размер: {q.size()}")

# Стек
print("\n2. Стек (Stack):")
s = Stack()
s.push("A")
s.push("B")
s.push("C")
print(s)
print(f"Верхний элемент: {s.peek()}")
print(f"Извлекаем: {s.pop()}")
print(f"Теперь верхний: {s.peek()}")
print(f"Размер: {s.size()}")