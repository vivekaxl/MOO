import os
import sys
import inspect
import random

from jmoo_individual import *
from jmoo_algorithms import *
from jmoo_stats_box import *


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import jmoo_properties

def three_others(individuals, one):
    seen = [one]

    def other():
        while True:
            random_selection = random.randint(0, len(individuals) - 1)
            if individuals[random_selection] not in seen:
                seen.append(individuals[random_selection])
                break
        return individuals[random_selection]

    return other(), other(), other()

def trim(mutated, low, up):
    return max(low, min(mutated, up))

def extrapolate(problem, individuals, one, f, cf):
    two, three, four = three_others(individuals, one)
    solution = []
    for d, decision in enumerate(problem.decisions):
        assert isinstance(two, jmoo_individual)
        x, y, z = two.decisionValues[d], three.decisionValues[d], four.decisionValues[d]
        if random.random() < cf:
            mutated = x + f * (y - z)
            solution.append(trim(mutated, decision.low, decision.up))
        else:
            solution.append(one.decisionValues[d])

    return jmoo_individual(problem, [float(d) for d in solution], None)

def anywhere_selector(problem, individuals):
    for individual in individuals:


def anywhere_mutate():

def anywhere_recombine():