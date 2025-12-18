"""
ООП подход без инкапсуляции
Прямой доступ к приватным полям _name, _friends, _born_in
"""
import json
import datetime as dt
from typing import Dict, List, Any
import uuid


class Person:
    def __init__(self, name: str, born_in: dt.datetime) -> None:
        self._name = name
        self._friends: List['Person'] = []
        self._born_in = born_in
        self._id = str(uuid.uuid4())

    def add_friend(self, friend: 'Person') -> None:
        if friend not in self._friends:
            self._friends.append(friend)
            friend._friends.append(self)


class DirectAccessSerializer:
    """
    Сериализатор с прямым доступом к приватным полям.
    Нарушает инкапсуляцию для упрощения кода.
    """

    @staticmethod
    def encode(person: Person) -> bytes:
        """Кодирует с прямым доступом к полям"""
        all_objects: List[Dict[str, Any]] = []
        visited_ids = set()

        def collect(p: Person):
            if p._id in visited_ids:
                return

            visited_ids.add(p._id)

            # ПРЯМОЙ ДОСТУП к приватным полям - нарушение инкапсуляции!
            obj_data = {
                'id': p._id,
                'name': p._name,  # Напрямую!
                'born_in': p._born_in.isoformat(),  # Напрямую!
                'friends': [f._id for f in p._friends]  # Напрямую!
            }
            all_objects.append(obj_data)

            # Рекурсивно собираем друзей
            for friend in p._friends:  # Напрямую!
                collect(friend)

        collect(person)
        return json.dumps(all_objects, indent=2).encode('utf-8')

    @staticmethod
    def decode(data: bytes) -> Person:
        """Декодирует с прямым доступом к полям"""
        objects_data = json.loads(data.decode('utf-8'))
        obj_cache: Dict[str, Person] = {}

        # Фаза 1: Создаем объекты
        for obj_data in objects_data:
            obj = Person.__new__(Person)
            # ПРЯМОЙ ДОСТУП для установки значений
            obj._id = obj_data['id']
            obj._name = obj_data['name']
            obj._born_in = dt.datetime.fromisoformat(obj_data['born_in'])
            obj._friends = []  # Пока пустой список
            obj_cache[obj._id] = obj

        # Фаза 2: Восстанавливаем связи
        for obj_data in objects_data:
            obj = obj_cache[obj_data['id']]
            # Прямой доступ для восстановления связей
            obj._friends = [obj_cache[friend_id] for friend_id in obj_data['friends']]

        return obj_cache[objects_data[0]['id']]


# === Пример использования ===
if __name__ == "__main__":
    print("\n=== ООП без инкапсуляции ===")

    p1 = Person("Ivan", dt.datetime(2020, 4, 12))
    p2 = Person("Petr", dt.datetime(2021, 9, 27))
    p1.add_friend(p2)

    serializer = DirectAccessSerializer()
    encoded = serializer.encode(p1)

    # Можно посмотреть что внутри
    print("Закодированные данные:")
    print(encoded.decode('utf-8')[:200] + "...")

    recreated = serializer.decode(encoded)

    # Прямой доступ к приватным полям для проверки
    print(f"\nПрямой доступ к полям восстановленного объекта:")
    print(f"_name: {recreated._name}")  # Нарушение инкапсуляции!
    print(f"_born_in: {recreated._born_in}")  # Нарушение инкапсуляции!
    print(f"Количество друзей (_friends): {len(recreated._friends)}")  # Нарушение!

    # Тест с циклической ссылкой
    p3 = Person("Anna", dt.datetime(2019, 3, 15))
    p1.add_friend(p3)
    p3.add_friend(p1)

    encoded2 = serializer.encode(p1)
    recreated2 = serializer.decode(encoded2)

    print(f"\nС циклической ссылкой:")
    print(f"У {recreated2._name} друзей: {len(recreated2._friends)}")
    print(f"У {recreated2._friends[1]._name} тоже есть друг: {recreated2._friends[1]._friends[0]._name}")
