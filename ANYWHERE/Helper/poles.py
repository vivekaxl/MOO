import os, inspect, sys, random

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../Techniques")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from euclidean_distance import euclidean_distance


cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import jmoo_properties


def find_extreme(one, population):
    temp = []
    for individual in population:
        temp_distance = euclidean_distance(one.decisionValues, individual.decisionValues), individual
        assert(temp_distance > 1), "Something's wrong"
        temp.append([temp_distance, individual])
    return sorted(temp, key=lambda x: x[0], reverse=True)[0][1]

def find_poles(population):
    poles = []
    for _ in xrange(jmoo_properties.ANYWHERE_POLES):
        while True:
            one = random.choice(population)
            east = find_extreme(one, population)
            west = find_extreme(east, population)
            if east != west and east != one and west != one: break
        poles.append([east, west])
    return poles
