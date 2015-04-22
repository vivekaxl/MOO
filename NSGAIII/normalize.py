from __future__ import division
import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from jmoo_individual import *
from ref_point import cover


def find_ideal_points(problem, objectives):
    # print "U Length of the population: ", len(objectives)
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
    # print "Length of the population: ", len(population)
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
    return points
    #return [point[i] for i, point in enumerate(points)]


def maxpoints(problem, population):
    # print "MX Length of the population: ", len(population)
    assert(len(population) != 1), "Length of population can't be 1"
    maxp = [-1e32 if x.lismore is True else 1e32 for x in problem.objectives]
    for individual in population:
        for i, obj in enumerate(individual.fitness.fitness):
            if problem.objectives[i].lismore is True:
                if obj > maxp[i]:
                    maxp[i] = obj
            else:
                if obj < maxp[i]:
                    maxp[i] = obj
    # print "maxp: ", maxp
    return maxp

def final_normalize(problem, intercepts, utopia, population):
    # print "Intercepts: ", intercepts
    # print "Utopia: ", utopia
    for individual in population:
        temp = []
        for no, (i, u) in enumerate(zip(intercepts, utopia)):
            temp.append(individual.translated[no] / (i - u + 0.00000001))
        individual.normalized = temp
    return population

def deduplicate(lis):
    new_k = []
    for elem in lis:
        if elem not in new_k:
            new_k.append(elem)
    return new_k

def gauss_elimination(A):
    """
    http://martin-thoma.com/solving-linear-equations-with-gaussian-elimination/#tocAnchor-1-3
    """
    n = len(A)
    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n+1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]

    # Solve equation Ax=b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x


def normalize(problem, already_chosen, last_level):
    # print "Normalize : length: ", len(already_chosen)
    population = []
    lpopulation = []
    for i,dIndividual in enumerate(already_chosen):
        cells = []
        for j in xrange(len(dIndividual)):
            cells.append(dIndividual[j])
        population.append(jmoo_individual(problem, cells, dIndividual.fitness.values))

    for i,dIndividual in enumerate(last_level):
        cells = []
        for j in xrange(len(dIndividual)):
            cells.append(dIndividual[j])
        lpopulation.append(jmoo_individual(problem, cells, dIndividual.fitness.values))

    assert(len(already_chosen) == len(population)), "The length of the already_chosen and population should the same"
    objectives = [list(individual.fitness.fitness) for individual in population + lpopulation]
    utopia = find_ideal_points(problem, objectives)
    # print "Utopia: ", utopia
    population = translate_objectives(problem, population, utopia)
    lpopulation = translate_objectives(problem, lpopulation, utopia)
    # assert(len(t_population) == len(population)), "The length of the population and translated should be the same"

    extreme_points = get_extreme_points(problem, population + lpopulation)
    # Duplicate exists. So solving it using Dr. Chiang's approach
    # <http://web.ntnu.edu.tw/~tcchiang/publications/nsga3cpp/nsga3cpp-validation.htm>
    # print "extreme points: ", extreme_points
    if len(extreme_points) != len(deduplicate(extreme_points)):
        # print "Duplicate exists",
        intercepts = maxpoints(problem, population + lpopulation)
    else:
        from fractions import Fraction
        n = len(extreme_points)
        A = [[0 for j in range(n+1)] for i in range(n)]
        for i in xrange(n):
            for j in xrange(n):
                A[i][j] = Fraction(extreme_points[i][j])
        for i in xrange(n):
            A[i][n] = Fraction(1)
        intercepts = gauss_elimination(A)

    population = final_normalize(problem, intercepts, utopia, population)
    lpopulation = final_normalize(problem, intercepts, utopia, lpopulation)

    # need to allows users to pass reference points

    return population, lpopulation


