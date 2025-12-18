"""
Функциональный подход без инкапсуляции
Прямая работа с данными, без объектов
"""
import json
import datetime as dt
from typing import Dict, List, Any, Tuple
import uuid


def create_person_dict(name: str, born_in: dt.datetime) -> Dict[str, Any]:
    """Создает словарь с данными о человеке (не объект!)"""
    return {
        'name': name,
        'born_in': born_in,
        'friends': [],  # список индексов друзей
        'id': str(uuid.uuid4())
    }


def add_friend_dict(person1: Dict[str, Any], person2: Dict[str, Any],
                    persons_list: List[Dict[str, Any]]) -> None:
    """Добавляет взаимную дружбу между двумя 'людьми' в списке"""
    if person2['id'] not in [persons_list[i]['id'] for i in person1['friends']]:
        # Находим индексы в общем списке
        idx1 = next(i for i, p in enumerate(persons_list) if p['id'] == person1['id'])
        idx2 = next(i for i, p in enumerate(persons_list) if p['id'] == person2['id'])

        person1['friends'].append(idx2)
        person2['friends'].append(idx1)


def encode_pure_functional(persons_list: List[Dict[str, Any]],
                           root_index: int = 0) -> bytes:
    """
    Чисто функциональная сериализация.
    Работает только со структурами данных.
    """
    # Конвертируем даты в строки
    serializable_list = []
    for person in persons_list:
        serializable_person = person.copy()
        serializable_person['born_in'] = person['born_in'].isoformat()
        # Заменяем ссылки на объекты ссылками на ID
        serializable_person['friends'] = [
            persons_list[friend_idx]['id'] for friend_idx in person['friends']
        ]
        serializable_list.append(serializable_person)

    # Добавляем индекс корневого элемента
    result = {
        'root_id': persons_list[root_index]['id'],
        'persons': serializable_list
    }

    return json.dumps(result, indent=2).encode('utf-8')


def decode_pure_functional(data: bytes) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Чисто функциональная десериализация.
    Возвращает список всех людей и корневого человека.
    """
    parsed = json.loads(data.decode('utf-8'))
    root_id = parsed['root_id']

    # Восстанавливаем структуры данных
    persons_list = []
    id_to_index: Dict[str, int] = {}

    # Сначала создаем все объекты
    for i, person_data in enumerate(parsed['persons']):
        person_dict = {
            'name': person_data['name'],
            'born_in': dt.datetime.fromisoformat(person_data['born_in']),
            'friends': [],  # временно пусто
            'id': person_data['id']
        }
        persons_list.append(person_dict)
        id_to_index[person_data['id']] = i

    # Затем восстанавливаем связи
    for i, person_data in enumerate(parsed['persons']):
        persons_list[i]['friends'] = [
            id_to_index[friend_id] for friend_id in person_data['friends']
        ]

    # Находим корневого человека
    root_person = persons_list[id_to_index[root_id]]

    return persons_list, root_person


def find_person_by_name(persons_list: List[Dict[str, Any]], name: str) -> Dict[str, Any]:
    """Находит человека по имени (функциональный стиль)"""
    return next(p for p in persons_list if p['name'] == name)


# === Пример использования ===
if __name__ == "__main__":
    print("\n=== Функциональный без инкапсуляции ===")

    # Создаем "людей" как структуры данных
    persons = [
        create_person_dict("Ivan", dt.datetime(2020, 4, 12)),
        create_person_dict("Petr", dt.datetime(2021, 9, 27)),
        create_person_dict("Anna", dt.datetime(2019, 3, 15))
    ]

    # Добавляем друзей (работаем с индексами)
    add_friend_dict(persons[0], persons[1], persons)
    add_friend_dict(persons[1], persons[2], persons)

    # Кодируем
    encoded = encode_pure_functional(persons, 0)

    print("Закодированные данные:")
    print(encoded.decode('utf-8'))

    # Декодируем
    decoded_list, root_person = decode_pure_functional(encoded)

    print(f"\nВосстановлено людей: {len(decoded_list)}")
    print(f"Корневой: {root_person['name']}, родился: {root_person['born_in']}")
    print(f"Друзья корневого (индексы): {root_person['friends']}")

    # Получаем имена друзей
    print("\nИмена друзей корневого:")
    for friend_idx in root_person['friends']:
        friend = decoded_list[friend_idx]
        print(f"  - {friend['name']} (индекс {friend_idx})")

    # Тест с циклической ссылкой
    add_friend_dict(persons[2], persons[0], persons)  # Анна дружит с Иваном

    encoded2 = encode_pure_functional(persons, 0)
    decoded_list2, root2 = decode_pure_functional(encoded2)

    print(f"\nС циклической ссылкой:")
    anna = find_person_by_name(decoded_list2, "Anna")
    print(f"У Анны друзей: {len(anna['friends'])}")
    print(f"Первый друг Анны: {decoded_list2[anna['friends'][0]]['name']}")
