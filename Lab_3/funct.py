"""
Функциональный подход с инкапсуляцией
Использует только публичный интерфейс объектов
"""
import json
import datetime as dt
from typing import Dict, List, Any, Callable

# Определяем типы для работы с Person
PersonLike = Any  # Любой объект с определенным интерфейсом


def encode_functional_encapsulated(person: PersonLike) -> bytes:
    """
    Функциональный стиль с соблюдением инкапсуляции.
    Работает только через публичные методы объекта.
    """

    def get_id(p: PersonLike) -> str:
        """Получает ID объекта через его метод"""
        if hasattr(p, 'get_id'):
            return p.get_id()
        # Если нет метода get_id, создаем на основе хэша
        return str(hash(p))

    def get_name(p: PersonLike) -> str:
        """Получает имя через публичный метод"""
        return p.get_name()

    def get_birth_date(p: PersonLike) -> dt.datetime:
        """Получает дату рождения через публичный метод"""
        return p.get_birth_date()

    def get_friends(p: PersonLike) -> List[PersonLike]:
        """Получает друзей через публичный метод"""
        return p.get_friends()

    # Основная логика кодирования
    all_objects_data: List[Dict[str, Any]] = []
    visited_ids: set = set()

    def process_person(p: PersonLike):
        """Рекурсивно обрабатывает персону и ее друзей"""
        current_id = get_id(p)

        if current_id in visited_ids:
            return

        visited_ids.add(current_id)

        # Собираем данные через публичные методы
        obj_data = {
            'id': current_id,
            'name': get_name(p),
            'born_in': get_birth_date(p).isoformat(),
            'friends': [get_id(friend) for friend in get_friends(p)]
        }
        all_objects_data.append(obj_data)

        # Рекурсивно обрабатываем друзей
        for friend in get_friends(p):
            process_person(friend)

    process_person(person)
    return json.dumps(all_objects_data, indent=2).encode('utf-8')


def decode_functional_encapsulated(
        data: bytes,
        person_factory: Callable[[str, dt.datetime], PersonLike]
) -> PersonLike:
    """
    Декодирует данные в объекты, используя фабрику.
    Восстанавливает связи через публичные методы.
    """
    objects_data = json.loads(data.decode('utf-8'))

    # Создаем временные объекты
    temp_objects: Dict[str, Dict[str, Any]] = {}

    # Фаза 1: Создаем объекты без связей
    for obj_data in objects_data:
        temp_objects[obj_data['id']] = {
            'obj': person_factory(obj_data['name'],
                                  dt.datetime.fromisoformat(obj_data['born_in'])),
            'friend_ids': obj_data['friends']
        }

    # Фаза 2: Восстанавливаем связи
    # Для этого нужны методы add_friend у объектов
    for obj_id, data in temp_objects.items():
        person_obj = data['obj']
        for friend_id in data['friend_ids']:
            friend_obj = temp_objects[friend_id]['obj']
            person_obj.add_friend(friend_obj)

    # Возвращаем первый объект
    first_id = objects_data[0]['id']
    return temp_objects[first_id]['obj']


# === Вспомогательный класс для демонстрации ===
class FunctionalPerson:
    """Класс для демонстрации функционального подхода"""

    def __init__(self, name: str, born_in: dt.datetime):
        self._name = name
        self._born_in = born_in
        self._friends: List['FunctionalPerson'] = []
        self._id = f"person_{hash((name, born_in))}"

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_birth_date(self) -> dt.datetime:
        return self._born_in

    def get_friends(self) -> List['FunctionalPerson']:
        return self._friends.copy()

    def add_friend(self, friend: 'FunctionalPerson'):
        if friend not in self._friends:
            self._friends.append(friend)
            friend._friends.append(self)


# === Пример использования ===
if __name__ == "__main__":
    print("\n=== Функциональный с инкапсуляцией ===")

    # Создаем объекты
    p1 = FunctionalPerson("Ivan", dt.datetime(2020, 4, 12))
    p2 = FunctionalPerson("Petr", dt.datetime(2021, 9, 27))
    p1.add_friend(p2)

    # Кодируем
    encoded = encode_functional_encapsulated(p1)


    # Декодируем с использованием фабрики
    def create_person(name: str, birth_date: dt.datetime) -> FunctionalPerson:
        return FunctionalPerson(name, birth_date)


    recreated = decode_functional_encapsulated(encoded, create_person)

    print(f"Исходный: {p1.get_name()}, ID: {p1.get_id()}")
    print(f"Восстановленный: {recreated.get_name()}, ID: {recreated.get_id()}")
    print(f"Друзей: {len(recreated.get_friends())}")
    print(f"Имя друга: {recreated.get_friends()[0].get_name()}")

    # Тест с циклом
    p3 = FunctionalPerson("Anna", dt.datetime(2019, 3, 15))
    p1.add_friend(p3)
    p3.add_friend(p1)

    encoded2 = encode_functional_encapsulated(p1)
    recreated2 = decode_functional_encapsulated(encoded2, create_person)

    print(f"\nС циклической ссылкой:")
    print(f"У {recreated2.get_name()} друзей: {len(recreated2.get_friends())}")
    print(f"Проверка цикла: {recreated2.get_friends()[1].get_friends()[0].get_name()}")
