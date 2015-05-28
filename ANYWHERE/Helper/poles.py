import os, inspect, sys, random

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../Techniques")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from euclidean_distance import euclidean_distance
from ndimes import generate_direction
from perpendicular_distance import perpendicular_distance
from geometry import find_extreme_point, find_midpoint
from better import rearrange

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import jmoo_properties
from jmoo_individual import jmoo_individual


def find_extreme(one, population):
    temp = []
    for individual in population:
        temp_distance = euclidean_distance(one.decisionValues, individual.decisionValues), individual
        assert(temp_distance > 1), "Something's wrong"
        temp.append([temp_distance, individual])
    return sorted(temp, key=lambda x: x[0], reverse=True)[0][1]


def look_for_duplicates(element, lst, field=lambda x: x):
    for l in lst:
        if field(element) == field(l):
            return True
    return False

def find_poles(problem, population):
    poles = []
    #remove duplicates
    temp_poles = []
    for _ in xrange(jmoo_properties.ANYWHERE_POLES):
        while True:
            one = random.choice(population)
            east = find_extreme(one, population)
            west = find_extreme(east, population)
            if east != west and east != one and west != one and east not in list(temp_poles) and west not in list(temp_poles): break
        poles.append(east)
        poles.append(west)
        if look_for_duplicates(east, temp_poles) is False:
            temp_poles.append(east)
        else:
            assert(True),"Something'S wrong"
        if look_for_duplicates(west, temp_poles, lambda x: x.decisionValues) is False:
            temp_poles.append(west)
        else:
            assert(True),"Something'S wrong"

    min_point, max_point = find_extreme_point([pop.decisionValues for pop in poles])
    mid_point = find_midpoint(min_point, max_point)
    mid_point = jmoo_individual(problem, mid_point, None)
    stars = rearrange(problem, mid_point, poles)
    return stars



def find_poles2(problem, population):
    poles = []
    min_point, max_point = find_extreme_point([pop.decisionValues for pop in population])
    mid_point = find_midpoint(min_point, max_point)
    directions = generate_direction(len(problem.decisions), jmoo_properties.ANYWHERE_POLES * 2, mid_point)
    mid_point = jmoo_individual(problem, mid_point, None)
    for direction in directions:
        mine = -1e32
        temp_pole = None
        for pop in population:
            y = perpendicular_distance(direction, pop.decisionValues)
            c = euclidean_distance(pop.decisionValues, [0 for _ in xrange(len(problem.decisions))])
            if (c-y) > mine:
                temp_pole = pop
                mine = (c-y)
        poles.append(temp_pole)

    stars = rearrange(problem, mid_point, poles)
    return stars

def find_poles3(problem, population):
    poles = []
    min_point, max_point = find_extreme_point([pop.decisionValues for pop in population])
    mid_point = find_midpoint(min_point, max_point)
    directions = [population[i] for i in sorted(random.sample(xrange(len(population)), jmoo_properties.ANYWHERE_POLES * 2)) ]
    mid_point = jmoo_individual(problem, mid_point, None)
    stars = rearrange(problem, mid_point, directions)
    return stars


