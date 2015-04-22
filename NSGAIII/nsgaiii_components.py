import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../DEAP")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from deap import base
from deap import creator
from deap import tools

from jmoo_individual import *

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "..")))
print cmd_subfolder
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from jmoo_algorithms import *

def nsgaiii_recombine(problem, population, selectees, k):
    # Evaluate any new guys
    for individual in population+selectees:
        if not individual.valid:
            individual.evaluate()
    # for i, individual in enumerate(population+selectees):
    #     print i, individual.fitness
    # Format a population data structure usable by DEAP's package
    dIndividuals = jmoo_algorithms.deap_format(problem, population+selectees)

    # for i, individual in enumerate(dIndividuals):
    #     print i, individual.fitness

    # print "Length of dIndividuals: ", len(dIndividuals)
    # Combine
    population = tools.selNSGA3(problem, dIndividuals, k)

    return population, k