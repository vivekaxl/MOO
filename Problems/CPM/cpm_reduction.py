from __future__ import division
import sys, os, inspect
parentdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)

parentdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../Techniques")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)
from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem
from euclidean_distance import euclidean_distance
from Problems.CPM.utilities.csv_utilities import read_csv

from sklearn import tree
import itertools

def equal_list(lista, listb):
    assert(len(lista) == len(listb)), "Not a valid comparison"
    for i, j in zip(lista, listb):
        if i == j: pass
        else: return False
    return True

def WHEREDataTransformation(filename):
    from utilities.RahulTool.methods1 import wrapper_createTbl
    # The data has to be access using this attribute table._rows.cells
    transformed_table = [[int(z) for z in x.cells[:-1]] + x.cells[-1:] for x in wrapper_createTbl(filename)._rows]
    cluster_numbers = set(map(lambda x: x[-1], transformed_table))

    # separating clusters
    # the element looks like [clusterno, rows]
    cluster_table = []
    for number in cluster_numbers:
        cluster_table.append([number]+ [filter(lambda x: x[-1] == number, transformed_table)])
    return cluster_table

def east_west_where(filename):
    def furthest(one, all_members):
        ret = None
        ret_distance = -1 * 1e10
        for member in all_members:
            if equal_list(one, member) is True: continue
            else:
                temp = euclidean_distance(one, member)
                if temp > ret_distance:
                    ret = member
                    ret_distance = temp
        return ret
    from random import choice
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        one = choice(cluster[-1])
        east = furthest(one, cluster[-1])
        west = furthest(east, cluster[-1])
        ret.append(east)
        ret.append(west)

    return ret
#
def exemplar_where(filename):
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        ret.append(sorted(cluster[-1], key=lambda x: x[-1])[0])
    return ret


# def median_where(self, filename):
#     # todo
#
# def mean_where(self, filename):
#     # todo
#

def base_line(filename="./data/Apache_AllMeasurements.csv"):
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        ret.extend(cluster[-1])
    return ret

temp_file_name = "temp_file.csv"
def temp_file_generation(header, listoflist):
    import csv
    with open(temp_file_name, 'wb') as fwrite:
        writer = csv.writer(fwrite, delimiter=',')
        writer.writerow(header)
        for l in listoflist:
            writer.writerow(l[1:])
    fwrite.close()


def temp_file_removal():
    os.remove(temp_file_name)





class cpm_apache_data_frame:
    newid = itertools.count().next
    def __init__(self, list):
        self.id = cpm_apache_data_frame.newid()
        self.Base = list[0]
        self.HostnameLookups = list[1]
        self.KeepAlive = list[2]
        self.EnableSendfile = list[3]
        self.FollowSymLinks = list[4]
        self.AccessLog = list[5]
        self.ExtendedStatus = list[6]
        self.InMemory = list[7]
        self.Handle = list[8]
        self.Performance = list[9]


class cpm_reduction(jmoo_problem):
    def get_training_data(self, number, percentage=1.0, method=base_line):
        from copy import deepcopy
        transformed_data = deepcopy(self.data)
        random_selection = self.get_testing_data(transformed_data)
        from random import sample
        random_selection = sample(random_selection, int(len(random_selection) * percentage))

        temp_file_generation(self.header, random_selection)
        training = method(temp_file_name)
        temp_file_removal()

        print "Length of training set: ", len(training),
        print "Length of testing set: ", len(self.testing_dependent)

        return [row[:-1] for row in training], [row[-1] for row in training]

    def get_testing_data(self, data):
        training_percent = 0.3
        total_data = len(self.data)
        from random import shuffle
        shuffle(data)
        testing_data = data[:int(training_percent * len(data))]
        self.testing_independent = [row[1:-1] for row in testing_data]
        self.testing_dependent = [float(row[-1]) for row in testing_data]
        return data[int(training_percent * len(data)):]

    def test_data(self):
        prediction = self.CART.predict(self.testing_independent)
        mre = []
        for i, j in zip(self.testing_dependent, prediction):
            mre.append(abs(i - j)/i)
        return sum(mre)/len(mre)

    def print_data(self):
        print len(self.data)

    def evaluate(self, input = None):
        if input:
            for i,decision in enumerate(self.decisions):
                decision.value = input[i]
            input = [round(decision.value, 1) for decision in self.decisions]
            # print "Input: ", input
            assert(len(input) == len(self.decisions)), "Something's wrong"
            prediction = self.CART.predict(input)
            # print prediction
            import time
            # time.sleep(0.5)
            return prediction
        else:
            assert(False), "BOOM"
            exit()


    def evalConstraints(prob,input = None):
        return False

class cpm_apache_training_reduction(cpm_reduction):
    # def __init__(self, treatment, number=50, requirements=9, name="CPM_APACHE", filename="./data/Apache_AllMeasurements.csv"):
    def __init__(self, treatment, number=50, requirements=9, name="CPM_APACHE", filename="./Problems/CPM/data/Apache_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)

        if treatment is None:
            fraction = 1.0
            treatment = east_west_where
        elif treatment.__name__ == "base_line": fraction =  (len(self.data) - number)/float((len(self.data)))
        else: fraction = 1.0


        self.training_independent, self.training_dependent = self.get_training_data(number, method=treatment, percentage=fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_BDBC(cpm_reduction):
    # def __init__(self, treatment, number=50, requirements=18, name="CPM_BDBC", filename="./data/BDBC_AllMeasurements.csv"):
    def __init__(self, treatment, number=50, requirements=18, name="CPM_BDBC", filename="./Problems/CPM//data/BDBC_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None: treatment = east_west_where
        elif treatment == 0: treatment = base_line
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)

        if treatment is None:
            fraction = 1.0
            treatment = east_west_where
        elif treatment.__name__ == "base_line":  fraction = (len(self.data) - number)/float((len(self.data)))
        else: fraction = 1.0

        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(number, method=treatment, percentage=fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_BDBJ(cpm_reduction):
    # def __init__(self, treatment, number=50, requirements=26, name="CPM_BDBJ", filename="./data/BDBJ_AllMeasurements.csv"):
    def __init__(self, treatment, number=50, requirements=26, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None: treatment = east_west_where
        elif treatment == 0: treatment = base_line
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)

        if treatment is None:
            fraction = 1.0
            treatment = east_west_where
        elif treatment.__name__ == "base_line": fraction =  (len(self.data) - number)/float((len(self.data)))
        else: fraction = 1.0

        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(number, method=treatment, percentage=fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_LLVM(cpm_reduction):
    # def __init__(self, treatment, number=50, requirements=11, fraction=0.5, name="CPM_LLVM", filename="./data/LLVM_AllMeasurements.csv"):
    def __init__(self, treatment, number=50, requirements=11, name="CPM_LLVM", filename="./Problems/CPM/data/LLVM_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None: treatment = east_west_where
        elif treatment == 0: treatment = base_line
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)

        if treatment is None:
            fraction = 1.0
            treatment = east_west_where
        elif treatment.__name__ == "base_line": fraction = (len(self.data) - number)/float((len(self.data)))
        else: fraction = 1.0

        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(number, method=treatment, percentage=fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_SQL(cpm_reduction):
    # def __init__(self, treatment, number=50, requirements=39, fraction=0.5, name="CPM_SQL", filename="./data/SQL_AllMeasurements.csv"):
    def __init__(self, treatment, number=50, requirements=39, name="CPM_SQL", filename="./Problems/CPM/data/SQL_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None: treatment = east_west_where
        elif treatment == 0: treatment = base_line
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)

        if treatment is None:
            fraction = 1.0
            treatment = east_west_where
        elif treatment.__name__ == "base_line": fraction =  (len(self.data) - number)/float((len(self.data)))
        else: fraction = 1.0

        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(number, method=treatment, percentage=fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)


class cpm_X264(cpm_reduction):
    # def __init__(self, treatment, number=50, requirements=16, fraction=0.5, name="cpm_X264", filename="./data/X264_AllMeasurements.csv"):
    def __init__(self, treatment, number=50, requirements=16, fraction=0.5, name="cpm_X264", filename="./Problems/CPM/data/X264_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None: treatment = east_west_where
        elif treatment == 0: treatment = base_line
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)

        if treatment is None:
            fraction = 1.0
            treatment = east_west_where
        elif treatment.__name__ == "base_line": fraction =  (len(self.data) - number)/float((len(self.data)))
        else: fraction = 1.0

        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(number, method=treatment, percentage=fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)


class data_container:
    def __init__(self, fraction, value):
        self.fraction = fraction
        self.value = value

def performance_test(dataset, treatment, test_numbers):
    repeats = 20
    scores = []
    print "Dataset: ", dataset.__name__, " Repeats: ", repeats, " Treatment: ", treatment.__name__
    for number in test_numbers:
        temp_store = []
        for repeat in xrange(repeats):
            print repeat, " ",
            p = dataset(treatment, number=number)
            temp_store.append(p.test_data())
        scores.append(data_container(number, sum(temp_store)/len(temp_store)))
        print
    return scores
    #draw([x.fraction for x in scores], [x.value for x in scores], problem.name)

def draw(scores1, name):
    import pylab as pl
    for score in scores1:
        print score[-1]
        pl.plot(score[0], score[1], linestyle="-", label=score[-1])
    pl.xlim(min([min(s0[0]) for s0 in scores1]) * 0.9, max([max(s0[0]) for s0 in scores1]) * 1.4)
    # pl.ylim(min([min(s1[1]) for s1 in scores1]) * 0.9, max([max(s1[1]) for s1 in scores1]) * 1.4)
    pl.ylim(0, 1.0)
    pl.xlabel('No. of Testing Instances')
    pl.ylabel('MRE variation over 10 repeats')
    pl.legend(loc='upper right')
    pl.title(name)
    pl.savefig("./figures/" + name + ".png")
    pl.close()

    print "#" * 20, "END", "#" * 20

# This is a function that would help to generate numbers to compare the elbow (trade off between amount of training
# and accuracy)


def test_cpm_apache():
    problems = [cpm_apache_training_reduction]
    treatments = [base_line, exemplar_where, east_west_where]
    numbers = [50, 100, 115]
    scores = []
    for problem in problems:
        for treatment in treatments:
            temp = performance_test(problem, treatment, numbers)
            scores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__])
    draw(scores, problem.__name__)

def test_BDBJ():
    problems = [cpm_BDBJ]
    treatments = [base_line, exemplar_where, east_west_where]
    numbers = [50, 100, 110]
    scores = []
    for problem in problems:
        for treatment in treatments:
            temp = performance_test(problem, treatment, numbers)
            scores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__])
    draw(scores, problem.__name__)

def test_BDBC():
    problems = [cpm_BDBC]
    treatments = [base_line, exemplar_where, east_west_where]
    numbers = [50, 100, 200, 400, 800, 1600]
    scores = []
    for problem in problems:
        for treatment in treatments:
            temp = performance_test(problem, treatment, numbers)
            scores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__])
    draw(scores, problem.__name__)


def test_SQL():
    problems = [cpm_SQL]
    treatments = [base_line, exemplar_where, east_west_where]
    numbers = [50, 100, 200, 400, 800, 1600, 3000]
    scores = []
    for problem in problems:
        for treatment in treatments:
            temp = performance_test(problem, treatment, numbers)
            scores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__])
    draw(scores, problem.__name__)


def test_x264():
    problems = [cpm_X264]
    treatments = [base_line, exemplar_where, east_west_where]
    numbers = [50, 100, 200, 400, 800]
    scores = []
    for problem in problems:
        for treatment in treatments:
            temp = performance_test(problem, treatment, numbers)
            scores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__])
    draw(scores, problem.__name__)

def test_LLVM():
    problems = [cpm_LLVM]
    treatments = [base_line, exemplar_where, east_west_where]
    numbers = [50, 100, 200, 400, 700]
    scores = []
    for problem in problems:
        for treatment in treatments:
            temp = performance_test(problem, treatment, numbers)
            scores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__])
    draw(scores, problem.__name__)


def start_test():
    test_cpm_apache()
    test_BDBC()
    test_BDBJ()
    test_SQL()
    test_x264()
    test_LLVM()

if __name__ == "__main__":
    start_test()