
"""
##########################################################
### @Author Joe Krall      ###############################
### @copyright see below   ###############################

    This file is part of JMOO,
    Copyright Joe Krall, 2014.

    JMOO is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    JMOO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with JMOO.  If not, see <http://www.gnu.org/licenses/>.
    
###                        ###############################
##########################################################
"""


"""

Random Stuff
------------

"""

import random
any = random.uniform
normal= random.gauss
seed  = random.seed

def sometimes(p) :
  "Returns True at probability 'p;"
  return p > any(0,1)

def one(lst):
  "Returns one item in a list, selected at random"
  return lst[  int(any(0,len(lst) - 1)) ]

def chosen_one(problem, lst):
    def sum(ll):
        l = ll.fitness.fitness
        # print "l: ", l
        assert len(problem.objectives) == len(l), "Something is wrong here"
        new = []
        for i, o in enumerate(problem.objectives):
            if o.lismore is False:
                new.append(l[i])
            else:
                new.append(100 - l[i])
        # print "New: ", min(new)
        return min(new)

    # print "Length of frontier: ", len(lst)
    chosen = lst[0]
    print "================================================"
    print "Start: ", lst[0]

    for element in lst:
        score = problem.evaluate(element.decisionValues)
        # print element.fitness.fitness
        if sum(chosen) < sum(element):
            chosen = element
        # print "There: ", chosen

    print "Chosen: ", chosen

    return chosen



"Brief notes"
"Core Part of JMOO accessed by jmoo_interface."

from jmoo_problems import *
from jmoo_algorithms import *
from jmoo_jmoea import *
from jmoo_properties import *
from jmoo_core import *
from joes_stats_suite import *
from joes_moo_charter import *
from joes_decision_binner import *
from jmoo_defect_chart import *
import time,sys

class jmoo_stats_report:
    def __init__(self,tests):
        self.tests = tests
    def doit(self,tagnote=""):
        joes_stats_reporter(self.tests.problems, self.tests.algorithms, tag=tagnote)
        
class jmoo_decision_report:
    def __init__(self,tests):
        self.tests = tests
    def doit(self,tagnote=""):
        joes_decision_reporter(self.tests.problems, self.tests.algorithms, tag=tagnote)

class jmoo_chart_report:
    def __init__(self,tests):
        self.tests = tests
    def doit(self,tagnote=""):
        joes_charter_reporter(self.tests.problems, self.tests.algorithms, tag=tagnote)

class jmoo_df_report:
    def __init__(self, tag="stats"):
        self.filename = DEFECT_PREDICT_PREFIX + "DefectPredict.xml"
        self.tag = tag
    def doit(self, tagnote=""):
        if self.tag == "stats":
            self.doStatistics()
        elif self.tag == "charts":
            self.doCharts()
    def doStatistics(self):
        parseXML(self.filename,self.tag)
    def doCharts(self):
        parseXML(self.filename,self.tag)

        
class jmoo_test:
    def __init__(self,problems,algorithms):
        self.problems = problems
        self.algorithms = algorithms
    def __str__(self):
        return str(self.problems) + str(self.algorithms)
        
class JMOO:
    def __init__(self,tests,reports):
        self.tests = tests
        self.reports = reports
        
    def doTests(self):
        
        sc2 = open(DATA_PREFIX + SUMMARY_RESULTS + DATA_SUFFIX, 'w')

        # Main control loop
        representatives = []                        # List of resulting final generations (stat boxe datatype)
        zOut = "<Experiment>\n"
        for problem in self.tests.problems:
              
            zOut += "<Problem name = '" + problem.name + "'>\n"
            
            for algorithm in self.tests.algorithms:
                
                
                zOut += "<Algorithm name = '" + algorithm.name + "'>\n"
                
                print "#<------- " + problem.name + " + " + algorithm.name + " ------->#"
                
                # Initialize data file for recording summary information [for just this problem + algorithm]
                backend = problem.name + "_" + algorithm.name + ".txt"
                
                # Decision Data
                filename = problem.name + "-p" + str(MU) + "-d" + str(len(problem.decisions)) + "-o" + str(len(problem.objectives))+"_"+algorithm.name+DATA_SUFFIX
                dbt = open(DATA_PREFIX + DECISION_BIN_TABLE + "_" + filename, 'w')
                sr = open(DATA_PREFIX + SUMMARY_RESULTS + filename, 'w')
                rrs = open(DATA_PREFIX + RRS_TABLE + "_" + filename, 'w')
                
                
                # Results Record:
                # # # Every generation
                # # # Decisions + Objectives
                
                # Summary Record
                # - Best Generation Only
                # - Number of Evaluations + Aggregated Objective Score
                # - 
                
                fa = open("data/results_"+filename, 'w')
                strings = ["NumEval"] + [obj.name + "_median,(%chg)," + obj.name + "_spread" for obj in problem.objectives] + ["IBD,(%chg), IBS"]
                for s in strings: fa.write(s + ",")
                fa.write("\n")
                fa.close()
                
                # Repeat Core
                for repeat in range(repeats):
                    
                    # Run 
                    
                    zOut += "<Run id = '" + str(repeat+1) + "'>\n"
                    
                    
                    start = time.time()
                    statBox = jmoo_evo(problem, algorithm)
                    end = time.time()

                    print "Bests actuals: ",statBox.bests_actuals

                    
                    # Record
                    
                    # Find best generation
                    representative = statBox.box[0]
                    for r,rep in enumerate(statBox.box):
                        # for indi in rep.population:
                        #     print indi
                        if rep.IBD < representative.IBD: 
                            representative = statBox.box[r]
                    representatives.append(representative)
                    
                    
                    
                    
                        
                    # Decision Bin Data
                    s = ""
                    for row in representative.population: 
                        for dec in row.decisionValues:
                            s += str("%10.2f" % dec) + ","
                        if row.valid:
                            for obj in row.fitness.fitness:
                                s += str("%10.2f" % obj) + "," 
                        else:
                            for obj in problem.objectives:
                                s += "?" + ","
                            
                        s += str(representative.numEval) + ","
                        s += "\n"

                    print "S: ", s
                    dbt.write(s)
                        
                    baseline = problem.referencePoint
                    s = ""
                    for row in representative.population:
                        #if not row.valid:
                        #    row.evaluate()
                        if row.valid:
                            for o,base,obj in zip(row.fitness.fitness, baseline, problem.objectives ):
                                c = percentChange(o, base, obj.lismore, obj.low, obj.up)
                                s += c + ","
                            s += str(representative.numEval) + "," 
                            for o,base,obj in zip(row.fitness.fitness, baseline, problem.objectives ):
                                c = str("%12.2f" % o)
                                s += c + ","
                            s += "\n"
                    rrs.write(s)
                        
                    #output every generation
                    for box in [representative]:
                        s_out = ""
                        s_out += str(MU) + ","
                        s_out += problem.name + "-p" + str(MU) + "-d"  + str(len(problem.decisions)) + "-o" + str(len(problem.objectives)) + ","
                        s_out += algorithm.name + ","
                        s_out += str(box.numEval) + ","
                        for low in representative.fitnessMedians:
                            s_out += str("%10.2f" % low) + ","
                        s_out += str("%10.2f" % box.IBD) + "," + str("%10.2f" % box.IBS) + "," + str((end-start))
                        sr.write(s_out + "\n")
                        sc2.write(s_out + "\n")


                    zOut += "<Summary>\n"
                    zOut += "<NumEvals>" + str(representative.numEval) + "</NumEvals>\n"
                    zOut += "<RunTime>" + str((end-start)) + "</RunTime>\n"
                    zOut += "<IBD>" + str(box.IBD) + "</IBD>\n"
                    zOut += "<IBS>" + str(box.IBS) + "</IBS>\n"
                    for i in range(len(problem.objectives)):
                        zOut += "<" + problem.objectives[i].name + ">" + str(representative.fitnessMedians[i]) + "</" + problem.objectives[i].name + ">\n" 
                    zOut += "</Summary>"
                        
                        
                    
                    
                    # Finish
                    zOut += "</Run>\n"
                    print " # Finished: Celebrate! # " + " Time taken: " + str("%10.5f" % (end-start)) + " seconds."
                    
                zOut += "</Algorithm>\n"
            zOut += "</Problem>\n"
        zOut += "</Experiment>\n"

        zOutFile = open("ExperimentRecords.xml", 'w')
        zOutFile.write(zOut)


    def remove_dominated_solution(self, problem, final_generation):
        # change format from jmoo_individula to deap_structure
        deap_final_generation = deap_format(problem, final_generation)
        front = ParetoFront()
        front.update(deap_final_generation)
        # Copy from DEAP structure to JMOO structure
        population = []
        for i,dIndividual in enumerate(front):
            cells = []
            for j in range(len(dIndividual)):
                cells.append(dIndividual[j])
            population.append(jmoo_individual(problem, cells, dIndividual.fitness.values))
        return population

    def doDefectPrediction(self):

        sc2 = open(DATA_PREFIX + SUMMARY_RESULTS + DATA_SUFFIX, 'w')
        defect_p = open(DEFECT_PREDICT_PREFIX + "DefectPredict.xml", "w")
        # Main control loop
        representatives = []                        # List of resulting final generations (stat boxe datatype)
        #zOut = "<Experiment>\n"
        vOut = "<Experiment>\n"

        for problem in self.tests.problems:



            #zOut += "<Problem name = '" + problem.name + "'>\n"
            vOut += "<Problem name = '" + problem.name + "'>\n"

            for algorithm in self.tests.algorithms:


                #zOut += "<Algorithm name = '" + algorithm.name + "'>\n"
                vOut += "<Algorithm name = '" + algorithm.name + "'>\n"

                print "#<------- " + problem.name + " + " + algorithm.name + " ------->#"

                # Initialize data file for recording summary information [for just this problem + algorithm]
                backend = problem.name + "_" + algorithm.name + ".txt"

                # Decision Data
                filename = problem.name + "-p" + str(MU) + "-d" + str(len(problem.decisions)) + "-o" + str(len(problem.objectives))+"_"+algorithm.name+DATA_SUFFIX
                dbt = open(DATA_PREFIX + DECISION_BIN_TABLE + "_" + filename, 'w')
                sr = open(DATA_PREFIX + SUMMARY_RESULTS + filename, 'w')
                rrs = open(DATA_PREFIX + RRS_TABLE + "_" + filename, 'w')


                # Results Record:
                # # # Every generation
                # # # Decisions + Objectives

                # Summary Record
                # - Best Generation Only
                # - Number of Evaluations + Aggregated Objective Score
                # -

                fa = open("data/results_"+filename, 'w')
                strings = ["NumEval"] + [obj.name + "_median,(%chg)," + obj.name + "_spread" for obj in problem.objectives] + ["IBD,(%chg), IBS"]
                for s in strings: fa.write(s + ",")
                fa.write("\n")
                fa.close()

                # Repeat Core
                for repeat in range(repeats):
                    objectives = ["pd", "pf", "prec"]

                    # Run
                    #zOut += "<Run id = '" + str(repeat+1) + "'>\n"
                    vOut += "<Run id = '" + str(repeat+1) + "'>\n"



                    start = time.time()
                    statBox = jmoo_evo(problem, algorithm)
                    end = time.time()
                    #  Vivek: Final

                    population = self.remove_dominated_solution(problem, statBox.box [-1].population)
                    any = chosen_one(problem, population)
                    vOut += "<Summary>\n"
                    vOut += "<NumEvals>" + str(statBox.numEval) + "</NumEvals>\n"
                    vOut += "<RunTime>" + str((end-start)) + "</RunTime>\n"
                    vOut += "<Training>" + str(problem.training) + "</Training>\n"
                    vOut += "<Tuning>" + str(problem.tuning) + "</Tuning>\n"
                    vOut += "<Testing>" + str(problem.testing) + "</Testing>\n"
                    vOut += "<Training_Tuning>\n"
                    for i,a in enumerate(any.fitness.fitness):
                        vOut += "\t<parameters" + str(i) + "> " + str(any.fitness.fitness[i]) + "</parameters" + str(i) + "> \n" # de
                    vOut += "</Training_Tuning>\n"
                    result = problem.test(any.decisionValues)
                    vOut += "<Parameters>\n"
                    #arguments = ["mss", "msl", "mxf", "threshold"]
                    for i,a in enumerate(any.decisionValues):
                        vOut += "<param"  +str(i) + ">" + str(a) + "</param" + str(i) + "> \n"
                    vOut += "</Parameters>\n"
                    vOut += "<Testing>\n"
                    for i,a in enumerate(result):
                        vOut += "\t<" + objectives[i] + "> " + str(result[i]) + "</" + objectives[i] + "> \n"
                    vOut += "</Testing>\n"
                    vOut += "<Default>\n"
                    result = problem.default()
                    for i,a in enumerate(result):
                        vOut += "\t<" + objectives[i] + "> " + str(result[i]) + "</" + objectives[i] + "> \n"
                    vOut += "</Default>\n"
                    vOut += "</Summary\n>"



                    # Record

                    # Find best generation
                    representative = statBox.box[0]
                    for r,rep in enumerate(statBox.box):
                        # for indi in rep.population:
                        #     print indi
                        if rep.IBD < representative.IBD:
                            representative = statBox.box[r]
                    representatives.append(representative)




                    # Decision Bin Data
                    s = ""
                    for row in representative.population:
                        for dec in row.decisionValues:
                            s += str("%10.2f" % dec) + ","
                        if row.valid:
                            for obj in row.fitness.fitness:
                                s += str("%10.2f" % obj) + ","
                        else:
                            for obj in problem.objectives:
                                s += "?" + ","

                        s += str(representative.numEval) + ","
                        s += "\n"

                    dbt.write(s)

                    baseline = problem.referencePoint
                    s = ""
                    for row in representative.population:
                        #if not row.valid:
                        #    row.evaluate()
                        if row.valid:
                            for o,base,obj in zip(row.fitness.fitness, baseline, problem.objectives ):
                                c = percentChange(o, base, obj.lismore, obj.low, obj.up)
                                s += c + ","
                            s += str(representative.numEval) + ","
                            for o,base,obj in zip(row.fitness.fitness, baseline, problem.objectives ):
                                c = str("%12.2f" % o)
                                s += c + ","
                            s += "\n"
                    rrs.write(s)

                    #output every generation
                    for box in [representative]:
                        s_out = ""
                        s_out += str(MU) + ","
                        s_out += problem.name + "-p" + str(MU) + "-d"  + str(len(problem.decisions)) + "-o" + str(len(problem.objectives)) + ","
                        s_out += algorithm.name + ","
                        s_out += str(box.numEval) + ","
                        for low in representative.fitnessMedians:
                            s_out += str("%10.2f" % low) + ","
                        s_out += str("%10.2f" % box.IBD) + "," + str("%10.2f" % box.IBS) + "," + str((end-start))
                        sr.write(s_out + "\n")
                        sc2.write(s_out + "\n")


                    # zOut += "<Summary>\n"
                    # zOut += "<NumEvals>" + str(representative.numEval) + "</NumEvals>\n"
                    # zOut += "<RunTime>" + str((end-start)) + "</RunTime>\n"
                    # zOut += "<IBD>" + str(box.IBD) + "</IBD>\n"
                    # zOut += "<IBS>" + str(box.IBS) + "</IBS>\n"
                    # for i in range(len(problem.objectives)):
                    #     zOut += "<" + problem.objectives[i].name + ">" + str(representative.fitnessMedians[i]) + "</" + problem.objectives[i].name + ">\n"
                    # zOut += "</Summary\n>"




                    # Finish
                    #zOut += "</Run>\n"
                    vOut += "</Run>\n"
                    print " # Finished: Celebrate! # " + " Time taken: " + str("%10.5f" % (end-start)) + " seconds."

                # zOut += "</Algorithm>\n"
                vOut += "</Algorithm>\n"
            # zOut += "</Problem>\n"
            vOut += "</Problem>\n"

        vOut += "</Experiment>\n"
        vOutFile = open("DefectPrediction.xml", 'w')
        vOutFile.write(vOut)

        #zOut += "</Experiment>\n"
        defect_p.write(vOut)
                    
                    
                    
    def doReports(self,thing=""):
        for report in self.reports:
            report.doit(tagnote = thing)
        
        
        