from __future__ import division
import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from jmoo_individual import *


def find_ideal_points(problem, objectives):
    assert(len(problem.objectives) == len(objectives[0])), "Length of the objectives is not correct"
    utopia = [1e32 if x.lismore is True else -1e32 for x in problem.objectives]
    for individual in objectives:
        for i, obj in enumerate(individual):
           if problem.objectives[i].lismore is True:
               if obj < utopia[i]:
                   utopia[i] = obj
           else:
               if obj > utopia[i]:
                   utopia[i] = obj
    return utopia

def translate_objectives(problem, population, utopia):
    assert(len(problem.objectives) == len(population[0].fitness.fitness)), "Length of the objectives is not correct"
    print "Length of the population: ", len(population)
    for individual in population:
        obj = individual.fitness.fitness
        temp = []
        for i in xrange(len(obj)):
            t = obj[i] - utopia[i]
            assert(t >= 0), "t should be greater or equal to 0"
            temp.append(t)
        individual.translated = temp
    return population

def get_extreme_points(problem, population):
    """
    :param problem:
    :param objectives: This is the translated objectives
    :return: intercepts of ith objective axis
    """
    def compute_asf(objectives, weights):
        temp = -1e32
        for o,w in zip(objectives, weights):
            t = o/w
            if t > temp:
                temp = t
        return temp

    points = []
    for i, obj in enumerate(problem.objectives):
        weight = [1e-6 for _ in problem.objectives]
        weight[i] = 1
        asf = 1e32
        extreme = None
        for individual in population:
            t = compute_asf(individual.translated, weight)
            if t < asf:
                asf = t
                extreme = individual.fitness.fitness
        points.append(extreme)
    return [point[i] for i, point in enumerate(points)]


def maxpoints(problem, population):
    utopia = [-1e32 if x.lismore is True else 1e32 for x in problem.objectives]
    for individual in population:
        for i, obj in enumerate(individual):
           if problem.objectives[i].lismore is True:
               if obj > utopia[i]:
                   utopia[i] = obj
           else:
               if obj < utopia[i]:
                   utopia[i] = obj
    return utopia


def normalize(problem, already_chosen, reference_points):
    population = []
    for i,dIndividual in enumerate(already_chosen):
        cells = []
        for j in xrange(len(dIndividual)):
            cells.append(dIndividual[j])
        population.append(jmoo_individual(problem, cells, dIndividual.fitness.values))


    assert(len(already_chosen) == len(population)), "The length of the already_chosen and population should the same"
    objectives = [list(individual.fitness.fitness) for individual in population]
    utopia = find_ideal_points(problem, objectives)
    print "Utopia: ", utopia
    t_population = translate_objectives(problem, population, utopia)
    assert(len(t_population) == len(population)), "The length of the population and translated should be the same"
    print "Need to check the first two steps of nsga2"

    extreme_points = get_extreme_points(problem, t_population)
    # Duplicate exists. So solving it using Dr. Chiang's approach
    # <http://web.ntnu.edu.tw/~tcchiang/publications/nsga3cpp/nsga3cpp-validation.htm>

    if len(extreme_points) != len(set(extreme_points)):
        print "Duplicate exists"
        extreme_points = [maxpoints(problem, population)] * len(problem.objectives)

    intercept_points = []
    for i, point in enumerate(extreme_points):
        temp = [0 for _ in xrange(len(problem.objectives))]
        temp[i] = point
        intercept_points.append(temp)

    print intercept_points
    # ---- Testing ---- #



    exit()



