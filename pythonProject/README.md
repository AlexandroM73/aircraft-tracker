# Aircraft Tracker

Трекер самолётов на Python: получение данных через OpenSky Network и Nominatim, сохранение в JSON, фильтрация и вывод в консоль.

## Структура проекта

- `src/` — исходный код (API, модель самолёта, хранилище, утилиты)
- `test/` — тесты (unittest)
- `data/` — данные (создаётся автоматически, не коммитится)
- `main.py` — точка входа, консольный интерфейс

## Установка

```bash
pip install -r requirements.txt
# или, если используешь pyproject.toml:
pip install .
