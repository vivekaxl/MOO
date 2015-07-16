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
    def get_training_data(self, filename, percentage=0.8, method=base_line):
        from random import sample
        random_selection = sample(self.data, int(len(self.data) * percentage))
        self.get_testing_data([x[0] for x in random_selection])

        temp_file_generation(self.header, random_selection)
        training = method(temp_file_name)
        temp_file_removal()
        return [row[:-1] for row in training], [row[-1] for row in training]

    def get_testing_data(self, list):
        testing_data = []
        for row in self.data:
            if row[0] not in list:
                testing_data.append(row)
        self.testing_independent = [row[1:-1] for row in testing_data]
        self.testing_dependent = [float(row[-1]) for row in testing_data]

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
            input = [decision.value for decision in self.decisions]
            assert(len(input) == len(self.decisions)), "Something's wrong"
            prediction = self.CART.predict(input)
            return prediction
        else:
            assert(False), "BOOM"
            exit()


    def evalConstraints(prob,input = None):
        return False

class cpm_apache_training_reduction(cpm_reduction):
    def __init__(self, treatment, requirements=9, fraction=0.5, name="CPM_APACHE", filename="./data/Apache_AllMeasurements.csv"):
    # def __init__(self, requirements=9, fraction=0.5, name="CPM_APACHE", filename="./Problems/CPM/data/Apache_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(filename, fraction, method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_BDBC(cpm_reduction):
    def __init__(self, treatment, requirements=18, fraction=0.5, name="CPM_BDBC", filename="./data/BDBC_AllMeasurements.csv"):
    # def __init__(self, requirements=18, fraction=0.5, name="CPM_BDBC", filename="./Problems/CPM/data/BDBC_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(filename, fraction, method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_BDBJ(cpm_reduction):
    def __init__(self, treatment, requirements=26, fraction=0.5, name="CPM_BDBJ", filename="./data/BDBJ_AllMeasurements.csv"):
    # def __init__(self, requirements=26, fraction=0.5, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(filename, fraction, method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_LLVM(cpm_reduction):
    def __init__(self, treatment, requirements=11, fraction=0.5, name="CPM_LLVM", filename="./data/LLVM_AllMeasurements.csv"):
    # def __init__(self, requirements=11, fraction=0.5, name="CPM_LLVM", filename="./Problems/CPM/data/LLVM_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(filename, fraction, method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_SQL_100(cpm_reduction):
    def __init__(self, treatment, requirements=39, fraction=0.5, name="CPM_SQL_100", filename="./data/SQL_100testing.csv"):
    # def __init__(self, requirements=39, fraction=0.5, name="CPM_SQL_100", filename="./Problems/CPM/data/SQL_100testing.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(filename, fraction, method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_SQL_4553(cpm_reduction):
    def __init__(self, treatment, requirements=39, fraction=0.5, name="CPM_SQL_4553", filename="./data/SQL_4553training.csv"):
    # def __init__(self, requirements=39, fraction=0.5, name="CPM_SQL_4553", filename="./Problems/CPM/data/SQL_4553training.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(filename, fraction, method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_X264(cpm_reduction):
    def __init__(self, treatment, requirements=16, fraction=0.5, name="cpm_X264", filename="./data/X264_AllMeasurements.csv"):
    # def __init__(self, treatment, requirements=16, fraction=0.5, name="cpm_X264", filename="./Problems/CPM/data/X264_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(filename, fraction, method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)


class data_container:
    def __init__(self, fraction, value):
        self.fraction = fraction
        self.value = value

def performance_test(dataset, treatment):
    repeat = 10
    scores = []
    for x in [i * 0.01 for i in xrange(50, 90)]:
        temp_store = []
        for p in xrange(repeat):
            problem = dataset(treatment, fraction=x)
            temp_store.append(problem.test_data())
        scores.append(data_container(x, sum(temp_store)/len(temp_store)))
    return scores
    #draw([x.fraction for x in scores], [x.value for x in scores], problem.name)

def draw(scores1, name):
    import pylab as pl
    for score in scores1:
        print score[-1]
        pl.plot(score[0], score[1], label=score[-1])
    pl.xlim(min([min(s0[0]) for s0 in scores1]) * 0.9, max([max(s0[0]) for s0 in scores1]) * 1.4)
    pl.ylim(min([min(s1[1]) for s1 in scores1]) * 0.9, max([max(s1[1]) for s1 in scores1]) * 1.4)
    pl.xlabel('Training set range')
    pl.ylabel('MRE variation over 10 repeats')
    pl.legend(loc='upper right')
    pl.title(name)
    pl.savefig("./figures/" + name + ".png")
    pl.close()

# This is a function that would help to generate numbers to compare the elbow (trade off between amount of training
# and accuracy)
if __name__ == "__main__":
    problems = [cpm_apache_training_reduction, cpm_BDBC, cpm_BDBJ, cpm_LLVM, cpm_SQL_100, cpm_SQL_4553,  cpm_X264]
    treatments = [base_line, exemplar_where, east_west_where]
    for problem in problems:
        print problem
        scores = []
        for treatment in treatments:
            temp = performance_test(problem, treatment)
            scores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__])
        draw(scores, problem.__name__)
