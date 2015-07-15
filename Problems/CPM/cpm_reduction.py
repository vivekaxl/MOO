from __future__ import division
import sys, os, inspect
parentdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)
from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem
from Problems.CPM.utilities.csv_utilities import read_csv
from Problems.CPM.utilities.lib import data
from Problems.CPM.utilities.where_utilities import launchWhere2
from sklearn import tree
import itertools

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
    def WHEREDataTransformation(self, filename):
        header, dataread = read_csv(filename, header=True)
        # print header
        dataread = [x[1:] for x in dataread]
        # print dataread
        datasent = data(indep=header[:-1], less=header[-1:], _rows=dataread)
        print launchWhere2(datasent)
        exit()
        #i have the data and header and now I need to put in into data and pass it to the where function


    def get_training_data(self, filename, percentage=0.8):
        self.WHEREDataTransformation(filename)
        get_clusters(self.data)
        from random import sample
        random_selection = sample(self.data, int(len(self.data) * percentage))
        self.get_testing_data([x[0] for x in random_selection])
        dependent_variables = [row[1:-1] for row in random_selection]

    def get_clusters_train(train):
            get_clusters(train)


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
    # def __init__(self, requirements=9, fraction=0.5, name="CPM_APACHE", filename="./data/Apache_AllMeasurements.csv"):
    def __init__(self, requirements=9, fraction=0.5, name="CPM_APACHE", filename="./Problems/CPM/data/Apache_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.data = read_csv(self.filename)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(filename, fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
#
# class cpm_BDBC(cpm):
#     # def __init__(self, requirements=9, fraction=0.5, name="CPM_BDBC", filename="./data/BDBC_AllMeasurements.csv"):
#     def __init__(self, requirements=18, fraction=0.5, name="CPM_BDBC", filename="./Problems/CPM/data/BDBC_AllMeasurements.csv"):
#         self.name = name
#         self.filename = filename
#         names = ["x"+str(i+1) for i in xrange(requirements)]
#         lows = [0 for _ in xrange(requirements)]
#         ups = [1 for _ in xrange(requirements)]
#         self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
#         self.objectives = [jmoo_objective("f1", True)]
#         self.data = read_csv(self.filename)
#         self.testing_independent, self.testing_dependent = [], []
#         self.training_independent, self.training_dependent = self.get_training_data(fraction)
#         self.CART = tree.DecisionTreeRegressor()
#         self.CART = self.CART.fit(self.training_independent, self.training_dependent)
#
# class cpm_BDBJ(cpm):
#     # def __init__(self, requirements=9, fraction=0.5, name="CPM_BDBJ", filename="./data/BDBJ_AllMeasurements.csv"):
#     def __init__(self, requirements=26, fraction=0.5, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):
#         self.name = name
#         self.filename = filename
#         names = ["x"+str(i+1) for i in xrange(requirements)]
#         lows = [0 for _ in xrange(requirements)]
#         ups = [1 for _ in xrange(requirements)]
#         self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
#         self.objectives = [jmoo_objective("f1", True)]
#         self.data = read_csv(self.filename)
#         self.testing_independent, self.testing_dependent = [], []
#         self.training_independent, self.training_dependent = self.get_training_data(fraction)
#         self.CART = tree.DecisionTreeRegressor()
#         self.CART = self.CART.fit(self.training_independent, self.training_dependent)
#
# class cpm_LLVM(cpm):
#     # def __init__(self, requirements=9, fraction=0.5, name="CPM_LLVM", filename="./data/LLVM_AllMeasurements.csv"):
#     def __init__(self, requirements=11, fraction=0.5, name="CPM_LLVM", filename="./Problems/CPM/data/LLVM_AllMeasurements.csv"):
#         self.name = name
#         self.filename = filename
#         names = ["x"+str(i+1) for i in xrange(requirements)]
#         lows = [0 for _ in xrange(requirements)]
#         ups = [1 for _ in xrange(requirements)]
#         self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
#         self.objectives = [jmoo_objective("f1", True)]
#         self.data = read_csv(self.filename)
#         self.testing_independent, self.testing_dependent = [], []
#         self.training_independent, self.training_dependent = self.get_training_data(fraction)
#         self.CART = tree.DecisionTreeRegressor()
#         self.CART = self.CART.fit(self.training_independent, self.training_dependent)
#
# class cpm_SQL_100(cpm):
#     # def __init__(self, requirements=9, fraction=0.5, name="CPM_SQL_100", filename="./data/SQL_100testing.csv"):
#     def __init__(self, requirements=39, fraction=0.5, name="CPM_SQL_100", filename="./Problems/CPM/data/SQL_100testing.csv"):
#         self.name = name
#         self.filename = filename
#         names = ["x"+str(i+1) for i in xrange(requirements)]
#         lows = [0 for _ in xrange(requirements)]
#         ups = [1 for _ in xrange(requirements)]
#         self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
#         self.objectives = [jmoo_objective("f1", True)]
#         self.data = read_csv(self.filename)
#         self.testing_independent, self.testing_dependent = [], []
#         self.training_independent, self.training_dependent = self.get_training_data(fraction)
#         self.CART = tree.DecisionTreeRegressor()
#         self.CART = self.CART.fit(self.training_independent, self.training_dependent)
#
# class cpm_SQL_4553(cpm):
#     # def __init__(self, requirements=9, fraction=0.5, name="CPM_SQL_4553", filename="./data/SQL_4553training.csv"):
#     def __init__(self, requirements=39, fraction=0.5, name="CPM_SQL_4553", filename="./Problems/CPM/data/SQL_4553training.csv"):
#         self.name = name
#         self.filename = filename
#         names = ["x"+str(i+1) for i in xrange(requirements)]
#         lows = [0 for _ in xrange(requirements)]
#         ups = [1 for _ in xrange(requirements)]
#         self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
#         self.objectives = [jmoo_objective("f1", True)]
#         self.data = read_csv(self.filename)
#         self.testing_independent, self.testing_dependent = [], []
#         self.training_independent, self.training_dependent = self.get_training_data(fraction)
#         self.CART = tree.DecisionTreeRegressor()
#         self.CART = self.CART.fit(self.training_independent, self.training_dependent)
#
# class cpm_X264(cpm):
#     # def __init__(self, requirements=9, fraction=0.5, name="cpm_X264", filename="./data/X264_AllMeasurements.csv"):
#     def __init__(self, requirements=16, fraction=0.5, name="cpm_X264", filename="./Problems/CPM/data/X264_AllMeasurements.csv"):
#         self.name = name
#         self.filename = filename
#         names = ["x"+str(i+1) for i in xrange(requirements)]
#         lows = [0 for _ in xrange(requirements)]
#         ups = [1 for _ in xrange(requirements)]
#         self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
#         self.objectives = [jmoo_objective("f1", True)]
#         self.data = read_csv(self.filename)
#         self.testing_independent, self.testing_dependent = [], []
#         self.training_independent, self.training_dependent = self.get_training_data(fraction)
#         self.CART = tree.DecisionTreeRegressor()
#         self.CART = self.CART.fit(self.training_independent, self.training_dependent)


class data_container:
    def __init__(self, fraction, value):
        self.fraction = fraction
        self.value = value

def performance_test(dataset):
    repeat = 10
    scores = []
    for x in [i * 0.01 for i in xrange(50, 100)]:
        temp_store = []
        for p in xrange(repeat):
            problem = dataset(fraction=x)
            temp_store.append(problem.test_data())
        scores.append(data_container(x, sum(temp_store)/len(temp_store)))

    draw([x.fraction for x in scores], [x.value for x in scores], problem.name)

def draw(listx, listy, name):
    import pylab as pl
    pl.plot(listx, listy)
    pl.xlim(min(listx) * 0.9, max(listx) * 1.1)
    pl.ylim(min(listy) * 0.9, max(listy) * 1.1)
    pl.xlabel('Training set range')
    pl.ylabel('MRE variation over 10 repeats')
    pl.title(name)
    pl.savefig("./figures/" + name + ".png")

# This is a function that would help to generate numbers to compare the elbow (trade off between amount of training
# and accuracy)
if __name__ == "__main__":
    problems = [cpm_SQL_4553, cpm_apache, cpm_BDBC, cpm_BDBJ, cpm_LLVM, cpm_SQL_100, cpm_SQL_4553, cpm_X264]
    for problem in problems:
        print problem
        performance_test(problem)
