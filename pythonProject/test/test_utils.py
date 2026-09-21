"""
Тесты для вспомогательных функций (Шаг 5).
"""
import unittest

from src.aeroplane import Aeroplane
from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    sort_aeroplanes,
    get_top_aeroplanes,
    print_aeroplanes,
)


class TestFilterAeroplanes(unittest.TestCase):
    def setUp(self):
        self.samples = [
            Aeroplane("A1", "Russia", velocity=200, baro_altitude=5000),
            Aeroplane("A2", "United States", velocity=300, baro_altitude=10000),
            Aeroplane("A3", "Russia", velocity=250, baro_altitude=8000),
            Aeroplane("A4", "Germany", velocity=280, baro_altitude=12000),
            Aeroplane("A5", "Russia", velocity=220, baro_altitude=3000),
        ]

    def test_filter_by_single_country(self):
        result = filter_aeroplanes(self.samples, ["Russia"])
        self.assertEqual(len(result), 3)
        for a in result:
            self.assertEqual(a.origin_country, "Russia")

    def test_filter_by_multiple_countries(self):
        result = filter_aeroplanes(self.samples, ["Russia", "Germany"])
        self.assertEqual(len(result), 4)

    def test_filter_case_insensitive(self):
        result = filter_aeroplanes(self.samples, ["russia"])
        self.assertEqual(len(result), 3)

    def test_filter_empty_words_returns_all(self):
        result = filter_aeroplanes(self.samples, [])
        self.assertEqual(len(result), 5)

    def test_filter_no_match(self):
        result = filter_aeroplanes(self.samples, ["Japan"])
        self.assertEqual(result, [])


class TestAltitudeRange(unittest.TestCase):
    def setUp(self):
        self.samples = [
            Aeroplane("A1", "Russia", velocity=200, baro_altitude=5000),
            Aeroplane("A2", "United States", velocity=300, baro_altitude=10000),
            Aeroplane("A3", "Russia", velocity=250, baro_altitude=8000),
            Aeroplane("A4", "Germany", velocity=280, baro_altitude=12000),
            Aeroplane("A5", "Russia", velocity=220, baro_altitude=3000),
        ]

    def test_range_inclusive(self):
        result = get_aeroplanes_by_altitude(self.samples, "5000 - 10000")
        self.assertEqual(len(result), 3)

    def test_range_no_spaces(self):
        result = get_aeroplanes_by_altitude(self.samples, "3000-8000")
        self.assertEqual(len(result), 3)

    def test_range_full(self):
        result = get_aeroplanes_by_altitude(self.samples, "0 - 20000")
        self.assertEqual(len(result), 5)

    def test_range_empty(self):
        result = get_aeroplanes_by_altitude(self.samples, "15000 - 20000")
        self.assertEqual(result, [])

    def test_invalid_range_returns_all(self):
        result = get_aeroplanes_by_altitude(self.samples, "invalid")
        self.assertEqual(len(result), 5)


class TestSortAndTop(unittest.TestCase):
    def setUp(self):
        self.samples = [
            Aeroplane("A1", "Russia", velocity=200, baro_altitude=5000),
            Aeroplane("A2", "United States", velocity=300, baro_altitude=10000),
            Aeroplane("A3", "Russia", velocity=250, baro_altitude=8000),
            Aeroplane("A4", "Germany", velocity=280, baro_altitude=12000),
            Aeroplane("A5", "Russia", velocity=220, baro_altitude=3000),
        ]

    def test_sort_by_altitude_desc(self):
        result = sort_aeroplanes(self.samples)
        self.assertEqual(result[0].baro_altitude, 12000)
        self.assertEqual(result[-1].baro_altitude, 3000)

    def test_top_3(self):
        result = get_top_aeroplanes(self.samples, 3)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].baro_altitude, 12000)
        self.assertEqual(result[1].baro_altitude, 10000)
        self.assertEqual(result[2].baro_altitude, 8000)

    def test_top_more_than_available(self):
        result = get_top_aeroplanes(self.samples, 100)
        self.assertEqual(len(result), 5)

    def test_top_zero(self):
        result = get_top_aeroplanes(self.samples, 0)
        self.assertEqual(len(result), 0)


class TestPrint(unittest.TestCase):
    def test_print_non_empty(self):
        import io
        from contextlib import redirect_stdout
        samples = [
            Aeroplane("A1", "Russia", velocity=200, baro_altitude=5000),
            Aeroplane("A2", "United States", velocity=300, baro_altitude=10000),
        ]
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_aeroplanes(samples)
        self.assertIn("A1", buf.getvalue())
        self.assertIn("A2", buf.getvalue())

    def test_print_empty(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_aeroplanes([])
        self.assertIn("не найдены", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
