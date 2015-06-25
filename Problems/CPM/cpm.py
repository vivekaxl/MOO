from __future__ import division
import sys, os, inspect
parentdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)
from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem
from Problems.CPM.utilities.csv_utilities import read_csv
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

class cpm(jmoo_problem):
    def get_training_data(self, percentage = 0.6):
        from random import sample
        random_selection = sample(self.data, int(len(self.data) * percentage))
        self.get_testing_data([x[0] for x in random_selection])
        return [row[1:-1] for row in random_selection], [row[-1] for row in random_selection]

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
        print len(input), len(self.decisions)
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

class cpm_apache(cpm):
    def __init__(self, requirements=9, fraction=0.5, name="CPM_APACHE", filename="./Problems/CPM/data/Apache_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", False)]
        self.data = read_csv(self.filename)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_BDBC(cpm):
    def __init__(self, requirements=9, fraction=0.5, name="CPM_BDBC", filename="./Problems/CPM/data/BDBC_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", False)]
        self.data = read_csv(self.filename)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)


class cpm_BDBJ(cpm):
    def __init__(self, requirements=9, fraction=0.5, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", False)]
        self.data = read_csv(self.filename)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_LLVM(cpm):
    def __init__(self, requirements=9, fraction=0.5, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", False)]
        self.data = read_csv(self.filename)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_SQL_100(cpm):
    def __init__(self, requirements=9, fraction=0.5, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", False)]
        self.data = read_csv(self.filename)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_SQL_4553(cpm):
    def __init__(self, requirements=9, fraction=0.5, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", False)]
        self.data = read_csv(self.filename)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

class cpm_X264(cpm):
    def __init__(self, requirements=9, fraction=0.5, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", False)]
        self.data = read_csv(self.filename)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data(fraction)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

def performance_test():
    repeat = 10
    for x in [i * 0.01 for i in xrange(50,100)]:
        print x,
        temp_store = []
        for p in xrange(repeat):
            problem = cpm_X264(fraction=x)
            temp_store.append(problem.test_data())
        print sum(temp_store)/len(temp_store)

if __name__ == "__main__":
    performance_test()
