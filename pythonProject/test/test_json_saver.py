"""
Тесты для JSONSaver (Шаг 5).
"""
import json
import os
import tempfile
import unittest

from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver


class TestJSONSaverBasic(unittest.TestCase):
    """Базовые тесты хранилища."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.filepath = os.path.join(self.tmpdir, "test_aeroplanes.json")
        self.saver = JSONSaver(self.filepath)
        self.samples = [
            Aeroplane("UAL1", "United States", velocity=250, baro_altitude=10000,
                      longitude=-87.0, latitude=41.0, icao24="abc1"),
            Aeroplane("AFL1", "Russia", velocity=200, baro_altitude=8000,
                      longitude=37.0, latitude=55.0, icao24="def2"),
            Aeroplane("DLH1", "Germany", velocity=300, baro_altitude=12000,
                      longitude=10.0, latitude=50.0, icao24="ghi3"),
        ]

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_file_created_on_init(self):
        self.assertTrue(os.path.exists(self.filepath))

    def test_empty_file_returns_empty_list(self):
        self.assertEqual(self.saver.get_all(), [])

    def test_add_single_aeroplane(self):
        self.saver.add_aeroplane(self.samples[0])
        result = self.saver.get_all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "UAL1")

    def test_add_multiple_aeroplanes(self):
        self.saver.add_aeroplanes(self.samples)
        result = self.saver.get_all()
        self.assertEqual(len(result), 3)

    def test_add_duplicate_ignored(self):
        self.saver.add_aeroplane(self.samples[0])
        self.saver.add_aeroplane(self.samples[0])
        result = self.saver.get_all()
        self.assertEqual(len(result), 1)

    def test_add_duplicates_in_batch(self):
        self.saver.add_aeroplanes(self.samples)
        self.saver.add_aeroplanes(self.samples)
        result = self.saver.get_all()
        self.assertEqual(len(result), 3)

    def test_delete_aeroplane(self):
        self.saver.add_aeroplanes(self.samples)
        self.saver.delete_aeroplane(self.samples[0])
        result = self.saver.get_all()
        self.assertEqual(len(result), 2)
        callsigns = [a.callsign for a in result]
        self.assertNotIn("UAL1", callsigns)

    def test_delete_all(self):
        self.saver.add_aeroplanes(self.samples)
        self.saver.delete_all()
        self.assertEqual(self.saver.get_all(), [])

    def test_get_by_country(self):
        self.saver.add_aeroplanes(self.samples)
        result = self.saver.get_by_country("Russia")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "AFL1")

    def test_get_by_country_case_insensitive(self):
        self.saver.add_aeroplanes(self.samples)
        result = self.saver.get_by_country("russia")
        self.assertEqual(len(result), 1)

    def test_get_by_country_not_found(self):
        self.saver.add_aeroplanes(self.samples)
        result = self.saver.get_by_country("Japan")
        self.assertEqual(result, [])

    def test_get_top_by_altitude(self):
        self.saver.add_aeroplanes(self.samples)
        top = self.saver.get_top_by_altitude(2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0].callsign, "DLH1")
        self.assertEqual(top[0].baro_altitude, 12000)
        self.assertEqual(top[1].callsign, "UAL1")
        self.assertEqual(top[1].baro_altitude, 10000)

    def test_get_top_more_than_available(self):
        self.saver.add_aeroplanes(self.samples)
        top = self.saver.get_top_by_altitude(10)
        self.assertEqual(len(top), 3)

    def test_get_top_zero(self):
        self.saver.add_aeroplanes(self.samples)
        top = self.saver.get_top_by_altitude(0)
        self.assertEqual(len(top), 0)

    def test_export_to_csv(self):
        self.saver.add_aeroplanes(self.samples)
        csv_path = os.path.join(self.tmpdir, "export.csv")
        self.saver.export_to_csv(csv_path)
        self.assertTrue(os.path.exists(csv_path))
        with open(csv_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("callsign", content)
        self.assertIn("UAL1", content)
        self.assertIn("AFL1", content)

    def test_export_to_csv_empty(self):
        csv_path = os.path.join(self.tmpdir, "empty.csv")
        self.saver.export_to_csv(csv_path)
        self.assertFalse(os.path.exists(csv_path))


if __name__ == "__main__":
    unittest.main()
