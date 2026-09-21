"""
Тесты для класса Aeroplane (Шаг 5).
"""
import unittest
from src.aeroplane import Aeroplane


class TestAeroplaneCreation(unittest.TestCase):
    """Тесты создания и валидации."""

    def test_valid_creation(self):
        a = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        self.assertEqual(a.callsign, "UAL1621")
        self.assertEqual(a.origin_country, "United States")
        self.assertEqual(a.velocity, 268.79)
        self.assertEqual(a.baro_altitude, 10203.18)

    def test_empty_callsign_defaults_to_na(self):
        a = Aeroplane("", "United States")
        self.assertEqual(a.callsign, "N/A")

    def test_none_callsign_defaults_to_na(self):
        a = Aeroplane(None, "United States")
        self.assertEqual(a.callsign, "N/A")

    def test_empty_country_raises(self):
        with self.assertRaises(ValueError):
            Aeroplane("UAL1621", "")

    def test_none_country_raises(self):
        with self.assertRaises(ValueError):
            Aeroplane("UAL1621", None)

    def test_negative_velocity_raises(self):
        with self.assertRaises(ValueError):
            Aeroplane("UAL1621", "United States", velocity=-100)

    def test_invalid_longitude_raises(self):
        with self.assertRaises(ValueError):
            Aeroplane("UAL1621", "United States", longitude=200.0)

    def test_invalid_latitude_raises(self):
        with self.assertRaises(ValueError):
            Aeroplane("UAL1621", "United States", latitude=-95.0)

    def test_invalid_true_track_raises(self):
        with self.assertRaises(ValueError):
            Aeroplane("UAL1621", "United States", true_track=400.0)

    def test_none_velocity_defaults_to_zero(self):
        a = Aeroplane("UAL1621", "United States", velocity=None)
        self.assertEqual(a.velocity, 0.0)

    def test_none_altitude_defaults_to_zero(self):
        a = Aeroplane("UAL1621", "United States", baro_altitude=None)
        self.assertEqual(a.baro_altitude, 0.0)

    def test_whitespace_callsign_stripped(self):
        a = Aeroplane("  UAL1621  ", "United States")
        self.assertEqual(a.callsign, "UAL1621")

    def test_whitespace_country_stripped(self):
        a = Aeroplane("UAL1621", "  United States  ")
        self.assertEqual(a.origin_country, "United States")

    def test_icao24_default_na(self):
        a = Aeroplane("UAL1621", "United States")
        self.assertEqual(a.icao24, "N/A")

    def test_on_ground_default_false(self):
        a = Aeroplane("UAL1621", "United States")
        self.assertFalse(a.on_ground)


class TestAeroplaneComparison(unittest.TestCase):
    """Тесты сравнения по скорости и высоте."""

    def test_lt_speed(self):
        a = Aeroplane("A1", "Russia", velocity=200)
        b = Aeroplane("A2", "Russia", velocity=300)
        self.assertTrue(a < b)

    def test_gt_speed(self):
        a = Aeroplane("A1", "Russia", velocity=300)
        b = Aeroplane("A2", "Russia", velocity=200)
        self.assertTrue(a > b)

    def test_le_speed(self):
        a = Aeroplane("A1", "Russia", velocity=200)
        b = Aeroplane("A2", "Russia", velocity=200)
        self.assertTrue(a <= b)

    def test_ge_speed(self):
        a = Aeroplane("A1", "Russia", velocity=300)
        b = Aeroplane("A2", "Russia", velocity=300)
        self.assertTrue(a >= b)

    def test_eq_same_speed_and_altitude(self):
        a = Aeroplane("A1", "Russia", velocity=200, baro_altitude=1000)
        b = Aeroplane("A2", "Russia", velocity=200, baro_altitude=1000)
        self.assertTrue(a == b)

    def test_eq_different_speed(self):
        a = Aeroplane("A1", "Russia", velocity=200)
        b = Aeroplane("A2", "Russia", velocity=300)
        self.assertFalse(a == b)

    def test_higher_than(self):
        a = Aeroplane("A1", "Russia", baro_altitude=10000)
        b = Aeroplane("A2", "Russia", baro_altitude=5000)
        self.assertTrue(a.higher_than(b))

    def test_lower_than(self):
        a = Aeroplane("A1", "Russia", baro_altitude=5000)
        b = Aeroplane("A2", "Russia", baro_altitude=10000)
        self.assertTrue(a.lower_than(b))

    def test_altitude_equals(self):
        a = Aeroplane("A1", "Russia", baro_altitude=10000)
        b = Aeroplane("A2", "Russia", baro_altitude=10000)
        self.assertTrue(a.altitude_equals(b))


class TestCastToObjectList(unittest.TestCase):
    """Тесты фабричного метода cast_to_object_list."""

    def test_cast_valid_states(self):
        states = [
            ["abc123", "UAL1621", "United States", None, None,
             -87.9, 41.9, 10203.18, False, 268.79, 180.0, 0, None, None, None, False, 1],
            ["def456", "AFL123", "Russia", None, None,
             37.6, 55.7, 9000.0, False, 250.0, 90.0, 0, None, None, None, False, 1],
        ]
        aeroplanes = Aeroplane.cast_to_object_list(states)
        self.assertEqual(len(aeroplanes), 2)
        self.assertEqual(aeroplanes[0].callsign, "UAL1621")
        self.assertEqual(aeroplanes[1].callsign, "AFL123")

    def test_cast_empty_list(self):
        result = Aeroplane.cast_to_object_list([])
        self.assertEqual(result, [])

    def test_cast_skips_invalid_data(self):
        states = [
            ["abc", None, None, None, None, None, None, None, None, None, None],
        ]
        result = Aeroplane.cast_to_object_list(states)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "N/A")
        self.assertEqual(result[0].origin_country, "Unknown")

    def test_cast_handles_short_state(self):
        states = [["abc", "CS1"]]
        result = Aeroplane.cast_to_object_list(states)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "CS1")


class TestSerialization(unittest.TestCase):
    """Тесты to_dict / from_dict."""

    def test_to_dict_contains_all_fields(self):
        a = Aeroplane("UAL1621", "United States", velocity=268.79,
                      baro_altitude=10203.18, longitude=-87.9, latitude=41.9,
                      icao24="abc123", true_track=180.0, on_ground=False)
        d = a.to_dict()
        self.assertEqual(d["callsign"], "UAL1621")
        self.assertEqual(d["origin_country"], "United States")
        self.assertEqual(d["velocity"], 268.79)
        self.assertEqual(d["baro_altitude"], 10203.18)
        self.assertEqual(d["icao24"], "abc123")

    def test_from_dict_roundtrip(self):
        original = Aeroplane("UAL1621", "United States", velocity=268.79,
                             baro_altitude=10203.18, longitude=-87.9,
                             latitude=41.9, icao24="abc123")
        d = original.to_dict()
        restored = Aeroplane.from_dict(d)
        self.assertEqual(restored.callsign, original.callsign)
        self.assertEqual(restored.origin_country, original.origin_country)
        self.assertEqual(restored.velocity, original.velocity)
        self.assertEqual(restored.baro_altitude, original.baro_altitude)


if __name__ == "__main__":
    unittest.main()
