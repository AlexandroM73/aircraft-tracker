"""
Абстрактный класс для работы с API.
Реализован в соответствии с принципом наследования (Шаг 1) и SOLID (OCP).
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AbstractAPI(ABC):
    """Абстрактный базовый класс для работы с внешними API."""

    @abstractmethod
    def get_country_bbox(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Получить географические координаты (bounding box) страны.
        Возвращает словарь с ключами 'south', 'north', 'west', 'east'
        или None, если страна не найдена.
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> Optional[List[Any]]:
        """
        Получить список самолётов над указанной страной.
        Возвращает список сырых состояний (states) или None при ошибке.
        """
        pass

    @abstractmethod
    def get_raw_states(self, lamin: float, lamax: float,
                       lomin: float, lomax: float) -> Optional[List[Any]]:
        """
        Получить сырые данные о самолётах по координатам.
        """
        pass
