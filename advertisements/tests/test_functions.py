from django.test import TestCase

from advertisements.functions import get_distance_from_lat_lon_in_km


class TestFunctions(TestCase):

    def test_get_distance_from_lat_lon_in_km(self):
        self.assertAlmostEqual(get_distance_from_lat_lon_in_km(40.730610,-73.935242,63.446827,10.421906), 5771.4, 1)