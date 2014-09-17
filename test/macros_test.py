__author__ = 'jag'

from unittest import TestCase
from utils import MissingArgs, ActivityLevel, Stage
from macros_calc import get_adjusted_bmr, get_bmr, get_calorie_targets, \
                        get_carb_macro, get_fat_macro, get_protein_macro

class MacroUnitTest(TestCase):
    def test_get_bmr(self):
        ret = get_bmr(gender='male', age=24, height=182, weight=72)
        self.assertTrue(ret == 1982.5)
        ret = get_bmr(gender='female', age=21, height=144, weight=55)
        self.assertTrue(ret == 1394)
        ret = get_bmr(lean_mass=94)
        self.assertTrue(ret == 2400.4)
        try:
           get_bmr()
           self.fail()
        except MissingArgs as e:
            print e
            for arg in e.vals:
                print arg

    def test_get_adjusted_bmr(self):
        ret = get_adjusted_bmr(2400.4, activity_level=ActivityLevel.extrem_activ)
        self.assertTrue(ret == 2400.4*ActivityLevel.extrem_activ)
        ret = get_adjusted_bmr(2800, activity_level=ActivityLevel.sedentary)
        self.assertTrue(ret == 2800*ActivityLevel.sedentary)
        ret = get_adjusted_bmr(1290, activity_level=ActivityLevel.lightly_active)
        self.assertFalse(ret == 2400*ActivityLevel.lightly_active)

    def test_get_calorie_targets(self):
        ret = get_calorie_targets(1258, Stage.cut)
        self.assertTrue(abs(ret[0] - 842.86) <= 1 and abs(ret[1] - 1383.8) <= 1)
        ret = get_calorie_targets(2800, Stage.bulk)
        self.assertTrue(abs(ret[0] - 2520.0) <= 1 and abs(ret[1] - 3920.0) <= 1)
        ret = get_calorie_targets(2200, Stage.recomp)
        self.assertTrue(abs(ret[0] -1760.0) <= 1 and abs(ret[1] - 2640.0) <= 1)