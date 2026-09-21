"""
Тесты абстрактного класса-коннектора хранилища (Шаг 5).
"""
import unittest
from abc import ABC

from src.abstract_saver import AbstractSaver
from src.json_saver import JSONSaver


class TestAbstractSaver(unittest.TestCase):
    def test_is_abstract(self):
        self.assertTrue(issubclass(AbstractSaver, ABC))

    def test_cannot_instantiate(self):
        with self.assertRaises(TypeError):
            AbstractSaver()

    def test_has_required_methods(self):
        methods = [
            "add_aeroplane", "add_aeroplanes", "get_all",
            "get_by_country", "get_top_by_altitude",
            "delete_aeroplane", "delete_all",
        ]
        for m in methods:
            self.assertTrue(hasattr(AbstractSaver, m), f"Метод {m} не найден")

    def test_json_saver_inherits(self):
        self.assertTrue(issubclass(JSONSaver, AbstractSaver))


if __name__ == "__main__":
    unittest.main()
