"""
Класс самолёта с инкапсуляцией и методами сравнения (Шаг 2).
"""
from typing import Any, List, Optional


class Aeroplane:
    """
    Модель самолёта.
    Атрибуты инкапсулированы: доступ через @property, валидация в setter-ах.
    Поддерживает сравнение по скорости (operator overloading) и по высоте.
    """

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: Optional[float] = None,
        baro_altitude: Optional[float] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        icao24: Optional[str] = None,
        true_track: Optional[float] = None,
        on_ground: bool = False,
    ) -> None:
        self._callsign = None
        self._origin_country = None
        self._velocity = None
        self._baro_altitude = None
        self._longitude = None
        self._latitude = None
        self._icao24 = None
        self._true_track = None
        self._on_ground = False

        # Через setters — валидация
        self.callsign = callsign
        self.origin_country = origin_country
        self.velocity = velocity
        self.baro_altitude = baro_altitude
        self.longitude = longitude
        self.latitude = latitude
        self.icao24 = icao24
        self.true_track = true_track
        self.on_ground = on_ground

    # --- Properties & Setters ---

    @property
    def callsign(self) -> str:
        return self._callsign

    @callsign.setter
    def callsign(self, value: Optional[str]) -> None:
        self._callsign = value.strip() if value and value.strip() else "N/A"

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @origin_country.setter
    def origin_country(self, value: Optional[str]) -> None:
        if not value or not value.strip():
            raise ValueError("Страна регистрации не может быть пустой.")
        self._origin_country = value.strip()

    @property
    def velocity(self) -> float:
        return self._velocity if self._velocity is not None else 0.0

    @velocity.setter
    def velocity(self, value: Optional[float]) -> None:
        if value is not None and value < 0:
            raise ValueError("Скорость не может быть отрицательной.")
        self._velocity = float(value) if value is not None else None

    @property
    def baro_altitude(self) -> float:
        return self._baro_altitude if self._baro_altitude is not None else 0.0

    @baro_altitude.setter
    def baro_altitude(self, value: Optional[float]) -> None:
        self._baro_altitude = float(value) if value is not None else None

    @property
    def longitude(self) -> Optional[float]:
        return self._longitude

    @longitude.setter
    def longitude(self, value: Optional[float]) -> None:
        if value is not None and not (-180.0 <= value <= 180.0):
            raise ValueError("Долгота должна быть в диапазоне [-180, 180].")
        self._longitude = float(value) if value is not None else None

    @property
    def latitude(self) -> Optional[float]:
        return self._latitude

    @latitude.setter
    def latitude(self, value: Optional[float]) -> None:
        if value is not None and not (-90.0 <= value <= 90.0):
            raise ValueError("Широта должна быть в диапазоне [-90, 90].")
        self._latitude = float(value) if value is not None else None

    @property
    def icao24(self) -> str:
        return self._icao24 if self._icao24 else "N/A"

    @icao24.setter
    def icao24(self, value: Optional[str]) -> None:
        self._icao24 = value.strip() if value and value.strip() else None

    @property
    def true_track(self) -> Optional[float]:
        return self._true_track

    @true_track.setter
    def true_track(self, value: Optional[float]) -> None:
        if value is not None and not (0.0 <= value <= 360.0):
            raise ValueError("Курс должен быть в диапазоне [0, 360].")
        self._true_track = float(value) if value is not None else None

    @property
    def on_ground(self) -> bool:
        return self._on_ground

    @on_ground.setter
    def on_ground(self, value: bool) -> None:
        self._on_ground = bool(value)

    # --- Сравнение по скорости ---

    def __lt__(self, other: "Aeroplane") -> bool:
        return self.velocity < other.velocity

    def __le__(self, other: "Aeroplane") -> bool:
        return self.velocity <= other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        return self.velocity > other.velocity

    def __ge__(self, other: "Aeroplane") -> bool:
        return self.velocity >= other.velocity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity == other.velocity and self.baro_altitude == other.baro_altitude

    # --- Сравнение по высоте ---

    def higher_than(self, other: "Aeroplane") -> bool:
        return self.baro_altitude > other.baro_altitude

    def lower_than(self, other: "Aeroplane") -> bool:
        return self.baro_altitude < other.baro_altitude

    def altitude_equals(self, other: "Aeroplane") -> bool:
        return self.baro_altitude == other.baro_altitude

    # --- Строковое представление ---

    def __repr__(self) -> str:
        return (
            f"Aeroplane(callsign={self.callsign!r}, "
            f"origin_country={self.origin_country!r}, "
            f"velocity={self.velocity}, "
            f"baro_altitude={self.baro_altitude})"
        )

    def __str__(self) -> str:
        return (
            f"{self.callsign} | {self.origin_country} | "
            f"Скорость: {self.velocity:.2f} м/с | "
            f"Высота: {self.baro_altitude:.2f} м | "
            f"Координаты: ({self.latitude}, {self.longitude})"
        )

    # --- Фабричные методы ---

    @staticmethod
    def cast_to_object_list(states: List[List[Any]]) -> List["Aeroplane"]:
        """
        Преобразует список сырых состояний из OpenSky API
        в список объектов Aeroplane.
        """
        result = []
        for state in states:
            try:
                aeroplane = Aeroplane(
                    callsign=state[1] if len(state) > 1 and state[1] else "N/A",
                    origin_country=state[2] if len(state) > 2 and state[2] else "Unknown",
                    velocity=state[9] if len(state) > 9 else None,
                    baro_altitude=state[7] if len(state) > 7 else None,
                    longitude=state[5] if len(state) > 5 else None,
                    latitude=state[6] if len(state) > 6 else None,
                    icao24=state[0] if len(state) > 0 and state[0] else None,
                    true_track=state[10] if len(state) > 10 else None,
                    on_ground=state[8] if len(state) > 8 else False,
                )
                result.append(aeroplane)
            except (ValueError, TypeError, IndexError) as e:
                # Пропускаем записи с некорректными данными
                continue
        return result

    def to_dict(self) -> dict:
        """Сериализация в словарь для сохранения в JSON."""
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "baro_altitude": self.baro_altitude,
            "velocity": self.velocity,
            "true_track": self.true_track,
            "on_ground": self.on_ground,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Aeroplane":
        """Десериализация из словаря."""
        return cls(
            callsign=data.get("callsign", "N/A"),
            origin_country=data.get("origin_country", "Unknown"),
            velocity=data.get("velocity"),
            baro_altitude=data.get("baro_altitude"),
            longitude=data.get("longitude"),
            latitude=data.get("latitude"),
            icao24=data.get("icao24"),
            true_track=data.get("true_track"),
            on_ground=data.get("on_ground", False),
        )
