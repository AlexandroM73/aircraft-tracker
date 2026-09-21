"""
Точка входа в программу. Консольный интерфейс для взаимодействия
с пользователем (Шаг 4) и объединение всех компонентов (Шаг 5).
"""
import sys
import os

# Добавляем корень проекта в sys.path для корректных импортов
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.aeroplanes_api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver
from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    sort_aeroplanes,
    get_top_aeroplanes,
    print_aeroplanes,
)


def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    api = AeroplanesAPI()
    saver = JSONSaver()

    print("\n" + "=" * 50)
    print("  Трекер самолётов (OpenSky Network)")
    print("=" * 50)

    while True:
        print("\n--- Меню ---")
        print("1. Запросить самолёты над страной")
        print("2. Топ-N по высоте полёта")
        print("3. Фильтр по стране регистрации")
        print("4. Показать все сохранённые самолёты")
        print("5. Диапазон высот + сортировка + топ-N")
        print("6. Очистить хранилище")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "0":
            print("До встречи! ✈")
            break

        elif choice == "1":
            country = input("Введите название страны: ").strip()
            if not country:
                print("Страна не указана.")
                continue
            print(f"Запрашиваю самолёты над '{country}'...")
            raw_states = api.get_aeroplanes(country)
            if raw_states is None:
                print("Не удалось получить данные.")
                continue
            aeroplanes = Aeroplane.cast_to_object_list(raw_states)
            print(f"Получено самолётов: {len(aeroplanes)}")
            saver.add_aeroplanes(aeroplanes)
            print(f"Сохранено в {saver._file_path}")
            print_aeroplanes(aeroplanes[:20])

        elif choice == "2":
            try:
                n = int(input("Введите N (количество для топа): "))
            except ValueError:
                print("Введите число.")
                continue
            top = saver.get_top_by_altitude(n)
            print_aeroplanes(top)

        elif choice == "3":
            filter_words = input(
                "Введите названия стран для фильтрации (через пробел): "
            ).split()
            all_aeroplanes = saver.get_all()
            filtered = filter_aeroplanes(all_aeroplanes, filter_words)
            print_aeroplanes(filtered)

        elif choice == "4":
            all_aeroplanes = saver.get_all()
            print_aeroplanes(all_aeroplanes)

        elif choice == "5":
            country = input("Введите название страны: ").strip()
            if not country:
                print("Страна не указана.")
                continue
            raw_states = api.get_aeroplanes(country)
            if raw_states is None:
                print("Не удалось получить данные.")
                continue
            aeroplanes = Aeroplane.cast_to_object_list(raw_states)

            try:
                top_n = int(input("Введите количество самолётов для топ N: "))
            except ValueError:
                print("Введите число.")
                continue

            filter_words = input(
                "Введите названия стран для фильтрации по стране регистрации: "
            ).split()

            altitude_range = input(
                "Введите диапазон высот полёта (пример: 1000 - 15000): "
            ).strip()

            filtered = filter_aeroplanes(aeroplanes, filter_words)
            ranged = get_aeroplanes_by_altitude(filtered, altitude_range)
            sorted_aero = sort_aeroplanes(ranged)
            top = get_top_aeroplanes(sorted_aero, top_n)
            print_aeroplanes(top)

        elif choice == "6":
            saver.delete_all()
            print("Хранилище очищено.")

        else:
            print("Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
