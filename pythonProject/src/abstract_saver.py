"""
Абстрактный класс-коннектор хранилища (Шаг 3).
Обязывает реализовать методы для добавления, получения и удаления
информации о самолётах.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.aeroplane import Aeroplane


class AbstractSaver(ABC):
    """
    Абстрактный класс для работы с хранилищем данных.
    Классы-наследники могут использовать JSON, CSV, TXT, БД и т.д. (SOLID — OCP).
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить информацию об одном самолёте в хранилище."""
        pass

    @abstractmethod
    def add_aeroplanes(self, aeroplanes: List[Aeroplane]) -> None:
        """Добавить список самолётов в хранилище."""
        pass

    @abstractmethod
    def get_all(self) -> List[Aeroplane]:
        """Получить все самолёты из хранилища."""
        pass

    @abstractmethod
    def get_by_country(self, country: str) -> List[Aeroplane]:
        """Получить самолёты по стране регистрации."""
        pass

    @abstractmethod
    def get_top_by_altitude(self, n: int) -> List[Aeroplane]:
        """Получить топ-N самолётов по высоте полёта."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удалить информацию о самолёте из хранилища."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Удалить всю информацию из хранилища."""
        pass
