from jmoo_stats_box import *


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import jmoo_properties
from ANYWHERE.Helper.mutator import extrapolate
from ANYWHERE.Helper.geometry import find_central_point
from ANYWHERE.Helper.poles import find_poles
from ANYWHERE.Helper.better import rearrange
from ANYWHERE.Helper.scores import scores
from ANYWHERE.Helper.nudge import nudge



def anywhere_selector(problem, individuals):
    new_population = []
    mutated_population = []
    new_population.extend(individuals)
    for count in xrange(jmoo_properties.ANYWHERE_EXPLOSION):
        new_population.extend([extrapolate(problem, individuals, individual, jmoo_properties.F, jmoo_properties.CF)
                               for individual in individuals])
    poles = find_poles(new_population)

    stars = []
    for p1, p2 in poles:
        stars.append(p1)
        stars.append(p2)
    midpoint = jmoo_individual(problem, find_central_point(poles), None)
    stars = rearrange(problem, midpoint, stars)
    for individual in new_population:
        correct_poles, individual = scores(individual, stars)
        temp_individual = nudge(problem, individual, stars[correct_poles].east, individual.anyscore)
        temp_individual.anyscore = individual.anyscore
        mutated_population.append(temp_individual)
    assert(len(new_population) == len(mutated_population)), "Mutation has gone wrong"
    mutated_population = sorted(mutated_population, key=lambda x: x.anyscore, reverse=True)[:jmoo_properties.MU]
    return mutated_population, len(stars)

def anywhere_mutate(problem, population):
    return population, 0

def anywhere_recombine(problem, unusedSlot, mutants, MU):
    return mutants, 0