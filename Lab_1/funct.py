from typing import Optional, List, Tuple, Dict, Any
import copy


# ========== QUEUE Функциональный стиль ==========

def create_queue() -> Dict[str, Any]:
    """Создать очередь"""
    return {"items": []}


def queue_enqueue(queue: Dict[str, Any], item: Any) -> Dict[str, Any]:
    """Добавить в очередь"""
    new_queue = copy.deepcopy(queue)
    new_queue["items"].append(item)
    return new_queue


def queue_dequeue(queue: Dict[str, Any]) -> Tuple[Optional[Any], Dict[str, Any]]:
    """Взять из очереди"""
    if not queue["items"]:
        return None, queue

    new_queue = copy.deepcopy(queue)
    item = new_queue["items"].pop(0)
    return item, new_queue


def queue_peek(queue: Dict[str, Any]) -> Optional[Any]:
    """Посмотреть первый элемент"""
    if not queue["items"]:
        return None
    return queue["items"][0]


def queue_is_empty(queue: Dict[str, Any]) -> bool:
    """Проверка на пустоту"""
    return len(queue["items"]) == 0


def queue_size(queue: Dict[str, Any]) -> int:
    """Размер очереди"""
    return len(queue["items"])


def queue_to_str(queue: Dict[str, Any]) -> str:
    """Строковое представление"""
    return f"Очередь: {queue['items']}"


# ========== STACK Функциональный стиль ==========

def create_stack() -> Dict[str, Any]:
    """Создать стек"""
    return {"items": []}


def stack_push(stack: Dict[str, Any], item: Any) -> Dict[str, Any]:
    """Добавить в стек"""
    new_stack = copy.deepcopy(stack)
    new_stack["items"].append(item)
    return new_stack


def stack_pop(stack: Dict[str, Any]) -> Tuple[Optional[Any], Dict[str, Any]]:
    """Взять из стека"""
    if not stack["items"]:
        return None, stack

    new_stack = copy.deepcopy(stack)
    item = new_stack["items"].pop()
    return item, new_stack


def stack_peek(stack: Dict[str, Any]) -> Optional[Any]:
    """Посмотреть верхний элемент"""
    if not stack["items"]:
        return None
    return stack["items"][-1]


def stack_is_empty(stack: Dict[str, Any]) -> bool:
    """Проверка на пустоту"""
    return len(stack["items"]) == 0


def stack_size(stack: Dict[str, Any]) -> int:
    """Размер стека"""
    return len(stack["items"])


def stack_to_str(stack: Dict[str, Any]) -> str:
    """Строковое представление"""
    return f"Стек: {stack['items']}"


# Тестируем функциональный стиль с ТАКИМ ЖЕ выводом
print("\n=== ФУНКЦИОНАЛЬНЫЙ СТИЛЬ ===")

# Очередь - ТОЧНО ТАКОЙ ЖЕ ВЫВОД КАК В ООП
print("\n1. Очередь (Queue):")
queue = create_queue()
queue = queue_enqueue(queue, "первый")
queue = queue_enqueue(queue, "второй")
queue = queue_enqueue(queue, "третий")
print(queue_to_str(queue))
print(f"Первый в очереди: {queue_peek(queue)}")
print(f"Извлекаем: {queue_dequeue(queue)[0]}")
item, queue = queue_dequeue(queue)  # Обновляем очередь после извлечения
print(f"Теперь первый: {queue_peek(queue)}")
print(f"Размер: {queue_size(queue)}")

# Стек - ТОЧНО ТАКОЙ ЖЕ ВЫВОД КАК В ООП
print("\n2. Стек (Stack):")
stack = create_stack()
stack = stack_push(stack, "A")
stack = stack_push(stack, "B")
stack = stack_push(stack, "C")
print(stack_to_str(stack))
print(f"Верхний элемент: {stack_peek(stack)}")
print(f"Извлекаем: {stack_pop(stack)[0]}")
item, stack = stack_pop(stack)  # Обновляем стек после извлечения
print(f"Теперь верхний: {stack_peek(stack)}")
print(f"Размер: {stack_size(stack)}")