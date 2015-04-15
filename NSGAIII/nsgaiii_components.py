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

    # Format a population data structure usable by DEAP's package
    dIndividuals = jmoo_algorithms.deap_format(problem, population+selectees)

    print "Length of dIndividuals: ", len(dIndividuals)


    # Combine
    dIndividuals = tools.selNSGA3(problem, dIndividuals, k)

    # Copy from DEAP structure to JMOO structure
    population = []
    for i,dIndividual in enumerate(dIndividuals):
        cells = []
        for j in range(len(dIndividual)):
            cells.append(dIndividual[j])
        population.append(jmoo_individual(problem, cells, dIndividual.fitness.values))

    return population, k