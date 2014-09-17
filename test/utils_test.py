from unittest import TestCase
from utils import lbs_to_kg, feet_to_meters, MissingArgs
__author__ = 'jag'


class UtilsTests(TestCase):
    def test_lbs_to_kg(self):
        ret = lbs_to_kg(212)
        self.assertTrue(int(ret) == 96)
        ret = lbs_to_kg(152)
        self.assertTrue(int(ret) == 68)

    def test_feet_to_meters(self):
        ret = feet_to_meters(feet=2, inches=3)
        self.assertTrue(int(ret) == 68)
        ret = feet_to_meters(feet=4, inches=1)
        self.assertTrue(int(ret) == 124)