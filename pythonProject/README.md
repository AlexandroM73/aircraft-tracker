# Aircraft Tracker

Трекер самолётов на Python: получение данных через OpenSky Network и Nominatim, сохранение в JSON, фильтрация и вывод в консоль.

## Структура проекта

- `src/` — исходный код (API, модель самолёта, хранилище, утилиты)
- `test/` — тесты (unittest)
- `data/` — данные (создаётся автоматически, не коммитится)
- `main.py` — точка входа, консольный интерфейс

- `data`/                     — JSON-файл создаётся здесь при работе&#41;)
- `src`/
- __`init`__.py
- `abstract_api`.py       — абстрактный класс API
- `aeroplanes_api`.py     — реализация (Nominatim + OpenSky)
- `aeroplane`.py          — модель самолёта
- `abstract_saver`.py     — абстрактное хранилище
- `json_saver`.py         — JSON-хранилище + экспорт CSV
- `utils`.py              — фильтр, сортировка, топ, вывод
- `test`/
- __`init`__.py
- `test_aeroplane`.py     — 26 тестов
- `test_json_saver`.py    — 17 тестов
- `test_utils`.py         — 19 тестов
- `test_api`.py           — 11 тестов
- `test_abstract_saver`.py — 4 теста
- `main`.py                   — точка входа, user_interaction()
- `pyproject`.toml            — конфигурация проекта


## Установка

```bash
pip install -r requirements.txt
# или, если используешь pyproject.toml:
pip install .
