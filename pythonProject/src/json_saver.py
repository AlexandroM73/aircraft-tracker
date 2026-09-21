"""
JSON-хранилище. Сохраняет данные о самолётах в JSON-файл (Шаг 3).
"""
import json
import os
from typing import List, Optional

from src.abstract_saver import AbstractSaver
from src.aeroplane import Aeroplane


class JSONSaver(AbstractSaver):
    """Класс для сохранения информации о самолётах в JSON-файл."""

    def __init__(self, file_path: str = "data/aeroplanes.json") -> None:
        self._file_path = file_path
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Создаёт файл и директорию, если их нет."""
        dir_path = os.path.dirname(self._file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(self._file_path):
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_data(self) -> List[dict]:
        """Читает сырые данные из JSON-файла."""
        with open(self._file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_data(self, data: List[dict]) -> None:
        """Записывает сырые данные в JSON-файл."""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет один самолёт в хранилище."""
        data = self._read_data()
        aeroplane_dict = aeroplane.to_dict()
        # Проверка дубликатов по icao24 + callsign
        for existing in data:
            if (existing.get("icao24") == aeroplane_dict["icao24"]
                    and existing.get("callsign") == aeroplane_dict["callsign"]):
                return  # уже есть
        data.append(aeroplane_dict)
        self._write_data(data)

    def add_aeroplanes(self, aeroplanes: List[Aeroplane]) -> None:
        """Добавляет список самолётов в хранилище."""
        data = self._read_data()
        existing_keys = {
            (d.get("icao24"), d.get("callsign")) for d in data
        }
        for a in aeroplanes:
            key = (a.icao24, a.callsign)
            if key not in existing_keys:
                data.append(a.to_dict())
                existing_keys.add(key)
        self._write_data(data)

    def get_all(self) -> List[Aeroplane]:
        """Возвращает все самолёты из хранилища."""
        data = self._read_data()
        return [Aeroplane.from_dict(d) for d in data]

    def get_by_country(self, country: str) -> List[Aeroplane]:
        """Возвращает самолёты, зарегистрированные в указанной стране."""
        data = self._read_data()
        return [
            Aeroplane.from_dict(d)
            for d in data
            if d.get("origin_country", "").lower() == country.lower()
        ]

    def get_top_by_altitude(self, n: int) -> List[Aeroplane]:
        """Возвращает топ-N самолётов по высоте полёта (по убыванию)."""
        all_aeroplanes = self.get_all()
        sorted_list = sorted(
            all_aeroplanes, key=lambda a: a.baro_altitude, reverse=True
        )
        return sorted_list[:n]

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из хранилища по icao24 и callsign."""
        data = self._read_data()
        filtered = [
            d for d in data
            if not (d.get("icao24") == aeroplane.icao24
                    and d.get("callsign") == aeroplane.callsign)
        ]
        self._write_data(filtered)

    def delete_all(self) -> None:
        """Очищает хранилище."""
        self._write_data([])

    def export_to_csv(self, csv_path: str = "data/aeroplanes.csv") -> None:
        """Дополнительно: экспорт данных в CSV (заглушка для расширяемости)."""
        import csv
        data = self._read_data()
        if not data:
            return
        fieldnames = list(data[0].keys())
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
