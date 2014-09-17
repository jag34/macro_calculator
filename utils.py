__author__ = 'jag'

def enum(**enums):
    return type('Enum', (), enums)

##
# Sedentary (little or no exercise): 1.2
# Lightly active (easy exercise/sports 1-3 days/week): 1.375
# Moderately active (moderate exercise/sports 3-5 days/week): 1.55
# Very active (hard exercise/sports 6-7 days a week): 1.725
# Extremely active (very hard exercise/sports and physical job): 1.9
##
Stage = enum(bulk = 1, recomp = 2, cut = 3)

ActivityLevel = enum(sedentary = 1.2,
                     lightly_active = 1.375,
                     moderat_active = 1.55,
                     very_active = 1.725,
                     extrem_activ = 1.9)

class MissingArgs(Exception):
    def __init__(self, vals):
        self.vals = vals
    def __str__(self):
        return "Arguments missing : %s" % ', '.join(self.vals)

def feet_to_meters(feet, inches):
    inches += feet * 12
    return float(inches) * 2.54

def lbs_to_kg(weight):
    return (float(weight) * 453.6)/1000