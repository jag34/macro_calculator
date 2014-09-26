__author__ = 'jag'

from utils import lbs_to_kg, feet_to_meters, ActivityLevel, MissingArgs, Stage

#
# By default tuples represent (rest day value, training day value)
#

##
# Bmr calculations
##
def get_bmr(lean_mass=None, gender=None, weight=None, height=None, age=None):
    # Let's use The Mifflin St Jeor Equation
    if lean_mass is None:
        args = {'gender':gender, 'weight':weight, 'height':height, 'age':age}
        if None not in args.values():
            if gender == 'male':
                s = 5.0
            else:
                s = -161.0
            bmr = (10.0*weight) + (6.25*height) - (5.0*age) + s
            return bmr
        else:
            missing_args = []
            for arg, val in args.items():
                if val is None:
                    missing_args.append(arg)

            raise MissingArgs(missing_args)

    else:
        return 370 + 21.6*lean_mass

def get_adjusted_bmr(bmr, activity_level):
    return bmr*activity_level

##
# Cutting : +10%kCal and -30/35%kCal
# Slow-Bulking :+40%kCal and -10%kCal
# Body-Recomp : +20%kCal and -20%kCal
##
def get_calorie_targets(adj_bmr, stage):
    rest_percent = 1
    train_percent = 1
    if stage == Stage.cut:
        train_percent = 0.1
        rest_percent = 0.33
    elif stage == Stage.bulk:
        train_percent = 0.4
        rest_percent = 0.1
    elif stage == Stage.recomp:
        train_percent = 0.2
        rest_percent = 0.2
    else:
        print "Unknown stage"
        return (0,0)

    return (adj_bmr-(adj_bmr*rest_percent), adj_bmr+(adj_bmr*train_percent))
##
# Macros
##
##
# Protein, try going here and guess
# http://www.nowloss.com/online-body-fat-percentage-calculator.htm
##
def get_protein_macro(lbm_percent, weight, stage ):
    lean_mass = abs((float(lbm_percent)/100)*weight - weight)
    if stage == Stage.cut:
        return lean_mass*2.5, lean_mass*3
    else:
        return lean_mass*2, lean_mass*3

##
# Fat, it's a range
##
def get_fat_macro(lbm_percent):
    return (xrange(60,95), xrange(40,65))

##
# Carbs, it's a filler
##
def get_carb_macro(prot_macro, fat_macro, calorie_tuple):
    # tuple should come as (rest day calories, train day calories)
    rest_carb_calorie = calorie_tuple[0] - prot_macro[0]*4 - fat_macro[0]*9
    train_carb_calorie = calorie_tuple[1] - prot_macro[1]*4 - fat_macro[1]*9

    return (rest_carb_calorie/4, train_carb_calorie/4)

if __name__ == '__main__':
    height = feet_to_meters(feet=5, inches=6.5)
    weight = lbs_to_kg(154)
    print "Weight: %s Height: %s" % (weight, height)
    lbm = 20

    base_bmr = get_bmr(gender='male', weight=weight, height=height, age=24)
    adj_bmr = get_adjusted_bmr(bmr=base_bmr, activity_level=ActivityLevel.sedentary)

    kcal_num = get_calorie_targets(adj_bmr, Stage.cut)
    protein_macro = get_protein_macro(lbm, weight, Stage.cut)

    fat_macro_range = get_fat_macro(lbm)
    rest_range = [i for i in fat_macro_range[0]]
    workout_range = [i for i in fat_macro_range[1]]

    fat_macro_rest = raw_input("Pick fat macro (Rest): (%s - %s)\n->" % (rest_range[1], rest_range[-1]))
    fat_macro_workout = raw_input("Pick fat macro (Workout): (%s - %s)\n->" % (workout_range[1], workout_range[-1]))

    fat_macro = (int(fat_macro_rest), int(fat_macro_workout))
    carb_macro = get_carb_macro(protein_macro, fat_macro, kcal_num)

    print "Calories Rest: {}, Workout: {}".format(kcal_num[0],kcal_num[1])
    print "Protein Rest: {}, Workout: {}".format(protein_macro[0], protein_macro[1])
    print "Fat Rest: {}, Workout: {}".format(fat_macro[0],fat_macro[1])
    print "Carb Rest: {}, Workout: {}".format(carb_macro[0],carb_macro[1])