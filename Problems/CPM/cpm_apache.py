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

class cpm_apache(jmoo_problem):
    def __init__(self, requirements=9):
        self.name = "CPM_APACHE"
        self.filename = "./data/Apache_AllMeasurements.csv"
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", False)]
        self.data = read_csv(self.filename, cpm_apache_data_frame)
        self.testing_independent, self.testing_dependent = [], []
        self.training_independent, self.training_dependent = self.get_training_data()
        self.CART = tree.DecisionTreeRegressor().fit(self.training_dependent, self.training_independent)

    def get_training_data(self, percentage = 0.5):
        from random import sample
        random_selection = sample(self.data, int(len(self.data) * percentage))
        self.get_testing_data([x.id for x in random_selection])
        return [row[:-1] for row in random_selection], [row[-1] for row in random_selection]

    def get_testing_data(self, list):
        testing_data = []
        for row in self.data:
            if row.id not in list:
                testing_data.append(row)
        self.testing_independent = [row[:-1] for row in testing_data]
        self.testing_dependent = [row[-1] for row in testing_data]

    def test_data(self):
        prediction = self.CART(self.testing_independent)
        print len(prediction), len(self.testing_dependent)



    def print_data(self):
        print len(self.data)



if __name__ == "__main__":
    problem = cpm_apache()
    problem.test_data()