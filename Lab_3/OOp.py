"""
ООП подход с инкапсуляцией
Класс Person предоставляет публичные методы для сериализации/десериализации
"""
import json
import datetime as dt
from typing import Dict, List, Any, Optional
import uuid


class Person:
    def __init__(self, name: str, born_in: dt.datetime) -> None:
        self._name = name
        self._friends: List['Person'] = []
        self._born_in = born_in
        self._id = str(uuid.uuid4())  # Уникальный ID для обработки ссылок

    def add_friend(self, friend: 'Person') -> None:
        """Добавляет друга (взаимная связь)"""
        if friend not in self._friends:
            self._friends.append(friend)
            friend._friends.append(self)

    def get_name(self) -> str:
        """Геттер для имени"""
        return self._name

    def get_birth_date(self) -> dt.datetime:
        """Геттер для даты рождения"""
        return self._born_in

    def get_friends(self) -> List['Person']:
        """Геттер для списка друзей"""
        return self._friends.copy()  # Возвращаем копию для защиты от изменений

    # === Методы для сериализации ===

    def to_serializable_dict(self) -> Dict[str, Any]:
        """
        Конвертирует объект в словарь для сериализации.
        Не нарушает инкапсуляцию - использует геттеры.
        """
        return {
            'type': 'Person',
            'id': self._id,
            'name': self.get_name(),
            'born_in': self.get_birth_date().isoformat(),
            'friends': [friend._id for friend in self.get_friends()]
        }

    @classmethod
    def from_serializable_dict(cls, data: Dict[str, Any],
                               obj_cache: Optional[Dict[str, 'Person']] = None) -> 'Person':
        """
        Создает объект из словаря.
        Восстанавливает связи между объектами.
        """
        if obj_cache is None:
            obj_cache = {}

        # Если объект уже есть в кэше, возвращаем его
        if data['id'] in obj_cache:
            return obj_cache[data['id']]

        # Создаем новый объект
        obj = cls.__new__(cls)
        obj._id = data['id']
        obj._name = data['name']
        obj._born_in = dt.datetime.fromisoformat(data['born_in'])
        obj._friends = []

        # Сохраняем в кэш
        obj_cache[data['id']] = obj

        # Пока не восстанавливаем связи, только создаем объект
        return obj

    @classmethod
    def restore_connections(cls, data_list: List[Dict[str, Any]],
                            obj_cache: Dict[str, 'Person']) -> None:
        """Восстанавливает связи между объектами"""
        for data in data_list:
            obj = obj_cache[data['id']]
            # Восстанавливаем друзей
            obj._friends = [obj_cache[friend_id] for friend_id in data['friends']]


class PersonSerializer:
    """Класс для сериализации/десериализации объектов Person"""

    @staticmethod
    def encode(person: Person) -> bytes:
        """Кодирует объект Person в байты (JSON)"""
        # Собираем все объекты в графе
        objects_to_save: List[Dict[str, Any]] = []
        visited_ids: set = set()

        def collect_objects(p: Person):
            if p._id in visited_ids:
                return

            visited_ids.add(p._id)
            objects_to_save.append(p.to_serializable_dict())

            # Рекурсивно собираем друзей
            for friend in p.get_friends():
                collect_objects(friend)

        collect_objects(person)

        # Сериализуем в JSON
        return json.dumps(objects_to_save, indent=2).encode('utf-8')

    @staticmethod
    def decode(data: bytes) -> Person:
        """Декодирует байты в объект Person"""
        # Парсим JSON
        objects_data = json.loads(data.decode('utf-8'))

        # Создаем кэш для объектов
        obj_cache: Dict[str, Person] = {}

        # Фаза 1: Создаем все объекты без связей
        for obj_data in objects_data:
            Person.from_serializable_dict(obj_data, obj_cache)

        # Фаза 2: Восстанавливаем связи
        Person.restore_connections(objects_data, obj_cache)

        # Возвращаем первый объект (корневой)
        return obj_cache[objects_data[0]['id']]


# === Пример использования ===
if __name__ == "__main__":
    # Создаем объекты
    p1 = Person("Ivan", dt.datetime(2020, 4, 12))
    p2 = Person("Petr", dt.datetime(2021, 9, 27))
    p1.add_friend(p2)

    # Кодируем
    serializer = PersonSerializer()
    encoded: bytes = serializer.encode(p1)

    # Декодируем
    recreated_p1 = serializer.decode(encoded)

    print("=== ООП с инкапсуляцией ===")
    print(f"Исходный: {p1.get_name()}, друзей: {len(p1.get_friends())}")
    print(f"Восстановленный: {recreated_p1.get_name()}, друзей: {len(recreated_p1.get_friends())}")
    print(f"Друг: {recreated_p1.get_friends()[0].get_name()}")

    # Проверяем циклические ссылки
    p3 = Person("Anna", dt.datetime(2019, 3, 15))
    p1.add_friend(p3)
    p3.add_friend(p1)  # Циклическая ссылка

    encoded2 = serializer.encode(p1)
    recreated2 = serializer.decode(encoded2)
    print(f"\nС циклической ссылкой: друзей у {recreated2.get_name()}: {len(recreated2.get_friends())}")
    print(
        f"У друга {recreated2.get_friends()[1].get_name()} тоже есть друзья: {len(recreated2.get_friends()[1].get_friends())}")
