"""
Тесты для API-классов (Шаг 5).
"""
import unittest
from abc import ABC

from src.abstract_api import AbstractAPI
from src.aeroplanes_api import AeroplanesAPI


class TestAbstractAPI(unittest.TestCase):
    """Тесты абстрактного класса API."""

    def test_is_abstract(self):
        self.assertTrue(issubclass(AbstractAPI, ABC))

    def test_cannot_instantiate(self):
        with self.assertRaises(TypeError):
            AbstractAPI()

    def test_has_abstract_methods(self):
        self.assertTrue(hasattr(AbstractAPI, "get_country_bbox"))
        self.assertTrue(hasattr(AbstractAPI, "get_aeroplanes"))
        self.assertTrue(hasattr(AbstractAPI, "get_raw_states"))


class TestAeroplanesAPI(unittest.TestCase):
    """Тесты конкретной реализации API (без реальных запросов)."""

    def test_inherits_abstract(self):
        self.assertTrue(issubclass(AeroplanesAPI, AbstractAPI))

    def test_can_instantiate(self):
        api = AeroplanesAPI()
        self.assertIsNotNone(api)

    def test_has_correct_urls(self):
        api = AeroplanesAPI()
        self.assertIn("nominatim", api._nominatim_url)
        self.assertIn("opensky", api._opensky_url)


if __name__ == "__main__":
    unittest.main()
