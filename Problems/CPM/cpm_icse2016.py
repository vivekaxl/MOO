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
    print wrapper_createTbl(filename)._rows[0]
    import pdb
    pdb.set_trace()
    exit()
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

testing_percent = 0
training_percent = 0



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
    def get_training_data(self, method=base_line):
        global testing_percent, training_percent
        from copy import deepcopy
        transformed_data = deepcopy(self.data)
        random_selection = self.get_testing_data(transformed_data, testing_percent)

        temp_file_generation(self.header, random_selection)
        training = method(temp_file_name)
        temp_file_removal()

        #
        # print "Length of training set: ", len(training),
        # print "Length of testing set: ", len(self.testing_dependent)

        return [row[:-1] for row in training], [row[-1] for row in training]

    def get_testing_data(self, data, testing_perc):
        # print "testing_percent: ", testing_percent
        from random import shuffle
        shuffle(data)
        testing_data = data[:int(testing_perc * len(data))]
        self.testing_independent = [row[1:-1] for row in testing_data]
        self.testing_dependent = [float(row[-1]) for row in testing_data]

        # This makes sure that the training and testing doesn't overlap
        return data[int(testing_perc * len(data)):]

    def test_data(self):
        prediction = [float(x) for x in self.CART.predict(self.testing_independent)]
        mre = []
        for i, j in zip(self.testing_dependent, prediction):
            mre.append(abs(i - j)/float(i))
        return sum(mre)/len(mre)

    def print_data(self):
        print len(self.data)

    def evaluate(self, input = None):
        print "This needs to be changed"
        exit()
        if input:
            for i,decision in enumerate(self.decisions):
                decision.value = input[i]
            input = [round(decision.value, 1) for decision in self.decisions]
            # print "Input: ", input
            assert(len(input) == len(self.decisions)), "Something's wrong"
            prediction = self.CART.predict(input)
            return prediction
        else:
            assert(False), "BOOM"
            exit()


    def evalConstraints(prob,input = None):
        return False

    def find_total_time(self):
        return sum([d[-1] for d in self.data])


class cpm_apache_training_reduction(cpm_reduction):
    def __init__(self, treatment, requirements=9, name="CPM_APACHE", filename="./data/Apache_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=9, name="CPM_APACHE", filename="./Problems/CPM/data/Apache_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read data
        self.header, self.data = read_csv(self.filename, header=True)

        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

class cpm_BDBC(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=18, name="CPM_BDBC", filename="./data/BDBC_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=18, name="CPM_BDBC", filename="./Problems/CPM//data/BDBC_AllMeasurements.csv"):

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

        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

class cpm_BDBJ(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=26, name="CPM_BDBJ", filename="./data/BDBJ_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=26, name="CPM_BDBJ", filename="./Problems/CPM/data/BDBJ_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read data
        self.header, self.data = read_csv(self.filename, header=True)



        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

class cpm_LLVM(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=11, fraction=0.5, name="CPM_LLVM", filename="./data/LLVM_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=11, name="CPM_LLVM", filename="./Problems/CPM/data/LLVM_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read data
        self.header, self.data = read_csv(self.filename, header=True)



        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

class cpm_SQL(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=39, fraction=0.5, name="CPM_SQL", filename="./data/SQL_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=39, name="CPM_SQL", filename="./Problems/CPM/data/SQL_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read data
        self.header, self.data = read_csv(self.filename, header=True)

        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4


class cpm_X264(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=16, fraction=0.5, name="cpm_X264", filename="./data/X264_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=16, fraction=0.5, name="cpm_X264", filename="./Problems/CPM/data/X264_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read data
        self.header, self.data = read_csv(self.filename, header=True)



        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4


class data_container:
    def __init__(self, fraction, value, saved_time):
        self.fraction = fraction
        self.value = value
        self.saved_times = saved_time

    def __str__(self):
        return str(self.fraction) + str(self.value) + str(self.saved_times) + "\n"

def performance_test(dataset, treatment):
    repeats = 20
    scores = []
    saved_times = []

    temp_store = []
    for repeat in xrange(repeats):
        # print repeat, " ",
        # print "Dataset: ", dataset.__name__, " Repeats: ", repeats,
        # print " Treatment: ", treatment.__name__, "Training Percent: ", training_percent,
        p = dataset(treatment=treatment)
        saved_times.append(p.saved_time)
        temp_store.append(p.test_data())

    scores.append(data_container(training_percent, temp_store, sum(saved_times)/len(saved_times)))
    return scores
    #draw([x.fraction for x in scores], [x.value for x in scores], problem.name)

def draw(data, name):
    import pylab as pl
    filename = "./Logs/" + name + ".txt"
    fdesc = open(filename, "w")
    fdesc.write("training_percent, mean, iqr, saved_time,technique \n")
    scores1 = []
    import numpy as np
    for row in data:
        scores = []
        for d in row:
            temp = []
            temp.append(d[0])
            temp.append(np.percentile(d[1], 50))
            temp.append(np.percentile(d[1], 75) - np.percentile(d[1], 25))
            temp.append(d[2])
            temp_string = str(d[0][-1]) + "," + str(np.percentile(d[1], 50)) + "," + str(np.percentile(d[1], 75) -
                                                    np.percentile(d[1], 25)) + "," + str(d[3][-1]) + "," + str(d[2]) + "\n"
            print temp_string
            fdesc.write(temp_string)
            scores.append(temp)
        scores1.append(scores)
    fdesc.close()


    for score in scores1:
        x_coordinates = [s[0] for s in score]
        y_coordinates = [s[1] for s in score]
        y_error = [s[2] for s in score]
        pl.errorbar(x_coordinates, y_coordinates, yerr=y_error, linestyle="-", label=score[-1][-1])

    pl.xlim(0.4, 1.2)
    # pl.ylim(min([min(s1[1]) for s1 in scores1]) * 0.9, max([max(s1[1]) for s1 in scores1]) * 1.4)
    pl.ylim(0, 1.0)
    pl.xlabel('Training Data (% of data)')
    pl.ylabel('MRE variation over 20 repeats')
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
    global training_percent, testing_percent
    percents = [50, 60, 70, 80, 90]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent/100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)

def test_BDBJ():
    problems = [cpm_BDBJ]
    treatments = [base_line, exemplar_where, east_west_where]
    global training_percent, testing_percent
    percents = [50, 60, 70, 80, 90]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent/100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)

def test_BDBC():
    problems = [cpm_BDBC]
    treatments = [base_line, exemplar_where, east_west_where]
    global training_percent, testing_percent
    percents = [50, 60, 70, 80, 90]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent/100
                testing_percent = 1 - training_percent
                print "1 training_percent: ", training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_SQL():
    problems = [cpm_SQL]
    treatments = [base_line, exemplar_where, east_west_where]
    global training_percent, testing_percent
    percents = [50, 60, 70, 80, 90]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent/100
                testing_percent = 1 - training_percent
                print "1 training_percent: ", training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_x264():
    problems = [cpm_X264]
    treatments = [base_line, exemplar_where, east_west_where]
    global training_percent, testing_percent
    percents = [50, 60, 70, 80, 90]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent/100
                testing_percent = 1 - training_percent
                print "1 training_percent: ", training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)

def test_LLVM():
    problems = [cpm_LLVM]
    treatments = [base_line, exemplar_where, east_west_where]
    global training_percent, testing_percent
    percents = [50, 60, 70, 80, 90]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent/100
                testing_percent = 1 - training_percent
                # print "1 training_percent: ", training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def start_test():
    # test_cpm_apache()
    # test_BDBC()
    # test_BDBJ()
    # test_SQL()
    # test_x264()
    test_LLVM()


def offline_draw( name):
    from collections import defaultdict
    import pylab as pl
    filename = "./Logs/" + name + ".txt"
    fdesc = open(filename, "r")
    scores = defaultdict(list)
    for i, line in enumerate(fdesc):
        if i == 0: continue
        line_split = line.split(",")
        # print ">> ", line_split
        if line_split[-1] not in scores.keys():  scores[line_split[-1]] = []
        scores[line_split[-1]].append([float(xx) for xx in line_split[:-2]])


    ymin = 1e10
    ymax = -1e10
    for key in scores.keys():
        score = scores[key]
        # for score in score_temp:
        #     print score
        #     raw_input()
        # print score
        x_coordinates = [s[0] for s in score]
        y_coordinates = [s[1]*100 for s in score]
        y_error = [s[2]*100 for s in score]
        ymin = min(min(y_coordinates), ymin)
        ymax = max(max(y_coordinates), ymax)
        # print x_coordinates
        print y_coordinates
        # print y_error
        # print key
        pl.errorbar(x_coordinates, y_coordinates, yerr=y_error, linestyle="-", label=key)


    print ymin
    print ymax
    pl.xlim(0.4, 1.2)
    pl.ylim(ymin * 0.9, ymax * 1.4)
    # pl.ylim(0, 1.0)
    pl.xlabel('Training Data (% of data)')
    pl.ylabel('MRE variation over 20 repeats')
    pl.legend(loc='upper right')
    pl.title(name)
    pl.savefig("./figures/" + name + "1.png")

    pl.close()

    #
    #
    # for score in scores1:
    #     x_coordinates = [s[0] for s in score]
    #     y_coordinates = [s[1] for s in score]
    #     y_error = [s[2] for s in score]
    #     pl.errorbar(x_coordinates, y_coordinates, yerr=y_error, linestyle="-", label=score[-1][-1])
    #
    # pl.xlim(0.4, 1.2)
    # # pl.ylim(min([min(s1[1]) for s1 in scores1]) * 0.9, max([max(s1[1]) for s1 in scores1]) * 1.4)
    # pl.ylim(0, 1.0)
    # pl.xlabel('Training Data (% of data)')
    # pl.ylabel('MRE variation over 20 repeats')
    # pl.legend(loc='upper right')
    # pl.title(name)
    # pl.savefig("./figures/" + name + ".png")
    # pl.close()
    #
    # print "#" * 20, "END", "#" * 20


def start_drawing():
    problems = [ "cpm_X264"]
    for problem in problems:
        offline_draw(problem)

if __name__ == "__main__":
    # start_drawing()
    start_test()