"""
Вспомогательные функции для фильтрации, сортировки и вывода (Шаг 4).
Каждая функция отвечает за одну задачу (SOLID — SRP).
"""
from typing import List, Optional, Tuple

from src.aeroplane import Aeroplane


def filter_aeroplanes(
    aeroplanes: List[Aeroplane], filter_words: List[str]
) -> List[Aeroplane]:
    """
    Фильтрует самолёты по странам регистрации.
    filter_words — список названий стран для фильтрации.
    """
    if not filter_words:
        return aeroplanes
    lower_words = [w.lower() for w in filter_words]
    return [
        a for a in aeroplanes
        if a.origin_country.lower() in lower_words
    ]


def get_aeroplanes_by_altitude(
    aeroplanes: List[Aeroplane], altitude_range: str
) -> List[Aeroplane]:
    """
    Фильтрует самолёты по диапазону высот.
    altitude_range — строка вида "1000 - 5000" или "1000-5000".
    """
    try:
        parts = altitude_range.replace(" ", "").split("-")
        if len(parts) != 2:
            return aeroplanes
        min_alt = float(parts[0])
        max_alt = float(parts[1])
    except (ValueError, IndexError):
        return aeroplanes

    return [a for a in aeroplanes if min_alt <= a.baro_altitude <= max_alt]


def sort_aeroplanes(aeroplanes: List[Aeroplane]) -> List[Aeroplane]:
    """
    Сортирует самолёты по высоте полёта (по убыванию).
    """
    return sorted(aeroplanes, key=lambda a: a.baro_altitude, reverse=True)


def get_top_aeroplanes(
    aeroplanes: List[Aeroplane], n: int
) -> List[Aeroplane]:
    """
    Возвращает топ-N самолётов по высоте полёта.
    """
    sorted_list = sort_aeroplanes(aeroplanes)
    return sorted_list[:n]


def print_aeroplanes(aeroplanes: List[Aeroplane]) -> None:
    """
    Выводит список самолётов в консоль в читаемом формате.
    """
    if not aeroplanes:
        print("Самолёты не найдены.")
        return

    print(f"\n{'='*80}")
    print(f"Найдено самолётов: {len(aeroplanes)}")
    print(f"{'='*80}")
    for i, a in enumerate(aeroplanes, 1):
        print(f"{i}. {a}")
    print(f"{'='*80}\n")
