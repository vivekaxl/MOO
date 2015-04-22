import random
import jmoo_properties
from jmoo_individual import *
distance_matrix = []
ideal_points = []

import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../Techniques")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from euclidean_distance import euclidean_distance

def assign_weights(number, summa = 100):
    assert(float(number).is_integer() is True), "Number is not correct"
    assert(float(summa).is_integer() is True), "sum is not correct"
    assert(number <= summa), "Integers can't be generated"
    ret_results = []
    min_value = 1
    temp_sum = 0
    for i in xrange(number-1):
        tem = random.randint(min_value, summa - (min_value * (number - (i+1))) - temp_sum)
        ret_results.append(tem)
        temp_sum += tem
    ret_results.append(summa - sum(ret_results))
    assert(sum(ret_results) == summa), "Result is wrong"
    return [x/float(summa) for x in ret_results]

def create_distance_matrix(population):
    global distance_matrix
    weights = [pop.weight for pop in population]
    distance_matrix = [[[0, i] for i, _ in enumerate(xrange(len(weights)))] for _ in xrange(len(weights))]
    for i in xrange(len(weights)):
        for j in xrange(len(weights)):
            distance_matrix[i][j][0] = euclidean_distance(weights[i], weights[j])

def create_ideal_points(problem):
    global ideal_points
    ideal_points = [1e30 if obj.lismore else 1e-30 for obj in problem.objectives]


def update_ideal_points(problem, individual):
    global ideal_points
    obj_in = individual.fitness.fitness
    assert(len(ideal_points) == len(obj_in)), "Length of ideal points are not equal to length of objectives"
    for i, obj in enumerate(problem.objectives):
        if obj.lismore:
            if ideal_points[i] > obj_in[i]:
                ideal_points[i] = obj_in[i]
        else:
            if ideal_points[i] < obj_in[i]:
                ideal_points[i] = obj_in[i]

def find_neighbours(pop_id):
    return [x[1] for x in sorted(distance_matrix[pop_id], key=lambda l: l[0])[:jmoo_properties.T]]

def trim(mutated, low, up):
    assert(low < up), "There is a mix up between low and up"
    if random.random > 0.5:
        return max(low, min(mutated, up))
    else:
        return low + ((mutated - low) % (up - low))


def assign_id_to_member(population):
    for i, pop in enumerate(population):
        pop.id = i
    return population



def mutate(problem, individual, rate):
    """
    I am not really sure how this mutation function works. Need to work that out!
    :param problem:
    :param individual:
    :param rate:
    :return:
    """
    eta_m = 20
    ret_result = []
    for i, decision in enumerate(problem.decisions):
        y = individual[i]
        yl = decision.low
        yu = decision.up

        delta1 = (y - yl) / (yu - yl)
        delta2 = (yu - y) / (yu - yl)

        rnd = random.random()
        mut_pow = 1 / (eta_m + 1)

        if rnd <= 0.5:
            xy = 1 - delta1
            val = 2.0 * rnd + (1 - 2.0 * rnd) + xy ** (eta_m + 1.0)
            deltaq = (val ** mut_pow) - 1
        else:
            xy = 1 - delta2
            val = 2.0 * (1.0 - rnd) + 2.0 * (rnd - 0.5) + xy ** (eta_m + 1.0)
            deltaq = 1.0 - (val ** mut_pow)

        ret_result.append(trim(y + deltaq * (yu - yl), decision.low, decision.up))

    return ret_result










def genetic_operation(problem, individual, population):
    assert(len(population) > 3), "Genetic operation is not possible without 3 individual"
    neighbours = list(individual.neighbor)
    a, b, c = sorted(neighbours, key=lambda k: random.random())[:3]
    item_a = [x for x in population if x.id == a][-1]
    item_b = [x for x in population if x.id == b][-1]
    item_c = [x for x in population if x.id == c][-1]
    mutant = []
    for i, decision in enumerate(problem.decisions):
        if random.random() < jmoo_properties.MOEAD_CF:
            value = trim(item_a.decisionValues[i] + jmoo_properties.MOEAD_F *
                         (item_b.decisionValues[i] - item_c.decisionValues[i]), decision.low, decision.up)
        else:
            value = individual.decisionValues[i]
        mutant.append(value)

    mutant = mutate(problem, mutant, len(problem.decisions) ** -1)
    return mutant

def weighted_tche(problem, weight_vector, individual):
    global ideal_points
    assert(len(weight_vector) == len(individual.fitness.fitness)), "Number of weights should be equal to objectives"
    distance = -1 * 1e30
    for i in xrange(len(problem.objectives)):
        diff = ideal_points[i] - individual.fitness.fitness[i]
        if weight_vector[i] == 0:
            temp = 0.0001 * diff
        else:
            temp = weight_vector[i] * diff
        if distance < temp:
            distance = temp
    return distance


def update_neighbor(problem, individual, mutant, population, dist_function):
    global ideal_points
    count = 0
    for i in individual.neighbor:
        neigh = [pop for pop in population if pop.id == i][-1]
        d = dist_function(problem, individual.weight, neigh)
        e = dist_function(problem, individual.weight, mutant)
        if d < e:
            # step 2.5
            # print "Before: ", [pop.fitness.fitness for pop in population if pop.id == i]
            # print "Changes:", count
            # count += 1
            neigh.decisionValues = list(mutant.decisionValues)
            neigh.fitness.fitness = list(mutant.fitness.fitness)
            # print "Change in individual: ", i
            # print "Mutant: ", mutant.fitness.fitness
            # print "After: ", [pop.fitness.fitness for pop in population if pop.id == i]
            # print ideal_points
            # print
            # exit()
    # print(id(population))
    return population






def evolve_neighbor(problem, individual, population):
    mutant = genetic_operation(problem, individual, population)
    mutant = jmoo_individual(problem, [float(d) for d in mutant], None)
    mutant.evaluate()
    return update_neighbor(problem, individual, mutant, population, weighted_tche)


def initialize_population(problem, population):
    for individual in population:
        if not individual.valid:
            individual.evaluate()
    population = assign_id_to_member(population)
    for pop in population:
        pop.weight = assign_weights(len(problem.objectives))
    create_ideal_points(problem)
    create_distance_matrix(population)
    for i, pop in enumerate(population):
        pop.neighbor = find_neighbours(i)
    for pop in population:
        update_ideal_points(problem, pop)
    return population, len(population)

# remeber to add len(population) to number of evals

def moead_selector(problem, population):
    for pop in population:
        population = evolve_neighbor(problem, pop, population)
        update_ideal_points(problem, pop)
    return population, len(population)


def moead_mutate(problem, population):
    return population, 0
def moead_recombine(problem, unusedSlot, mutants, MU):
    return mutants, 0




# ------------------------------------------------ Tests --------------------------------------------------- #
def _find_weights():
    def one_test():
        summa = random.randint(1,100)
        number = random.randint(1,summa)
        ret = assign_weights(number, summa)
        print ret
        exit()
        return ret

    def test_list(lis):
        temp = [1 if num < 1/100 else 0 for num in lis]
        if sum(temp) > 0:
            return True
        elif sum(temp) == 0:
            return False
        else:
            raise Exception("Shouldn't happen")

    for _ in xrange(100):
        assert(test_list(one_test()) is False), "Something's wrong"


def _euclidean_distance():
    def one_test():
        dimension = random.randint(1, 100)
        first = [random.randint(-100, 100) for _ in xrange(dimension)]
        second = [random.randint(-100, 100) for _ in xrange(dimension)]
        from scipy.spatial import distance
        try:
            assert(round(euclidean_distance(first, second), 6) == round(distance.euclidean(first, second),6)), "Mistakes" \
                                                                                                               " discovered"
        except:
            print "First: ", first
            print "Second: ", second
            print "My: ", euclidean_distance(first, second)
            print "Their: ", distance.euclidean(first, second)
            return False
        return True

    for _ in xrange(10000):
        print ".",
        assert(one_test() is True), "Test Failed"




if __name__ == "__main__":
    _find_weights()