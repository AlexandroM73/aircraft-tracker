"""
Конкретная реализация API для Nominatim + OpenSky.
Наследуется от AbstractAPI (принцип наследования, Шаг 1).
"""
from typing import Any, Dict, List, Optional

from src.abstract_api import AbstractAPI


class AeroplanesAPI(AbstractAPI):
    """Класс для работы с API nominatim.openstreetmap.org и opensky-network.org."""

    def __init__(self) -> None:
        self._nominatim_url = "https://nominatim.openstreetmap.org/search"
        self._opensky_url = "https://opensky-network.org/api/states/all"

    def get_country_bbox(self, country: str) -> Optional[Dict[str, float]]:
        """Получает bounding box страны через Nominatim."""
        from requests import get

        headers = {"User-Agent": "test-app/1.0"}
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        try:
            response = get(
                url=self._nominatim_url, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Ошибка при запросе к Nominatim: {e}")
            return None

        if not data:
            print(f"Страна '{country}' не найдена в Nominatim.")
            return None

        bbox = data[0].get("boundingbox")
        if not bbox or len(bbox) != 4:
            print("Не удалось получить корректные координаты для страны.")
            return None

        south, north, west, east = map(float, bbox)
        return {"south": south, "north": north, "west": west, "east": east}

    def get_raw_states(self, lamin: float, lamax: float,
                       lomin: float, lomax: float) -> Optional[List[Any]]:
        """Получает сырые данные о самолётах через OpenSky API."""
        from requests import get

        headers = {"User-Agent": "test-app/1.0"}
        params = {
            "lamin": lamin,
            "lamax": lamax,
            "lomin": lomin,
            "lomax": lomax,
        }

        try:
            response = get(
                url=self._opensky_url, params=params, headers=headers, timeout=15
            )
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            print(f"Ошибка при запросе к OpenSky: {e}")
            return None

        return result.get("states", [])

    def get_aeroplanes(self, country: str) -> Optional[List[Any]]:
        """
        Получает список самолётов над указанной страной.
        Сначала получает bounding box страны через Nominatim,
        затем запрашивает самолёты через OpenSky.
        """
        bbox = self.get_country_bbox(country)
        if bbox is None:
            return None

        return self.get_raw_states(
            lamin=bbox["south"],
            lamax=bbox["north"],
            lomin=bbox["west"],
            lomax=bbox["east"],
        )
