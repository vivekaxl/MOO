import jmoo_preprocessor
import xml.etree.cElementTree as ET
from jmoo_properties import *


def parse_version_XML( xml_file):
    """
    Parse XML with ElementTree
    """
    def parseResult(junk):
        lst = ""
        for i in junk:
            num = []
            if i.tag == "Result":
                res = i.text
            if i.tag == "List":
                for l in i:
                    num.append(float(l.text))
        lst += res + ",("
        for n in num:
            lst += str(int(ngit ))+","
        lst += ")|"
        return lst

    from collections import defaultdict

    tree = ET.ElementTree(file=xml_file)
    experiment = tree.getroot()
    result = "Experiment: \n"
    import os
    try:
        os.remove(VERSION_SPACE_PREFIX + "version_space_chart.txt")
    except: pass

    for algorithm in experiment:
        result += "Algorithm Name: " + str(algorithm.attrib["name"])+"\n"
        for problem in algorithm:
            result += str(problem.attrib['name']) + "|"
            for junk in problem:
                if junk.tag == "jmoo_preprocessor.PD":
                    result += parseResult(junk)
                if junk.tag == "jmoo_preprocessor.PF":
                    result += parseResult(junk)
                if junk.tag == "jmoo_preprocessor.PREC":
                    result += parseResult(junk)
                if junk.tag == "jmoo_preprocessor.PDPF":
                    result += parseResult(junk)
                if junk.tag == "jmoo_preprocessor.PFPREC":
                    result += parseResult(junk)
                if junk.tag == "jmoo_preprocessor.PDPREC":
                    result += parseResult(junk)
                if junk.tag == "jmoo_preprocessor.PDPFPREC":
                    result += parseResult(junk)
            result += "\n"
    f = open(VERSION_SPACE_PREFIX + "version_space_chart.txt", "w")
    f.write(result)
    print "FILE written into ", VERSION_SPACE_PREFIX, "version_space_chart.txt"

    #     if problem.tag == "Problem":
    #         scores_pd = defaultdict(list)
    #         scores_pf = defaultdict(list)
    #         scores_prec = defaultdict(list)
    #         scores_eval = defaultdict(list)
    #         ranking = defaultdict(list)
    #         dpd = []
    #         dpf =[]
    #         dprec = []
    #         for algorithm in problem:
    #             result +="Algorithm: "+ str(algorithm.attrib["name"])+"\n"
    #             numeval = []
    #             runtime = []
    #             pd = []
    #             pf =[]
    #             prec = []
    #             for run in algorithm:
    #                 for summary in run:
    #                     for junk in summary:
    #                         if junk.tag == "NumEvals":
    #                             numeval.append(float(junk.text))
    #                         elif junk.tag == "RunTime":
    #                             runtime.append(float(junk.text))
    #                         elif junk.tag == "Testing":
    #                             for i in junk:
    #                                 if i.tag == "pd":
    #                                     pd.append(float(i.text))
    #                                 elif i.tag == "pf":
    #                                     pf.append(float(i.text))
    #                                 elif i.tag == "prec":
    #                                     prec.append(float(i.text))
    #                         elif junk.tag == "Default":
    #                             for i in junk:
    #                                 if i.tag == "pd":
    #                                     dpd.append(float(i.text))
    #                                 elif i.tag == "pf":
    #                                     dpf.append(float(i.text))
    #                                 elif i.tag == "prec":
    #                                     dprec.append(float(i.text))
    #
    #             if tag == "stats":
    #                 result += "NumEval: "+ str(stat(numeval))+"\n"
    #                 result += "RunTime: "+ str(stat(runtime))+"\n"
    #                 result += "pd: "+ str(stat(pd))+"\n"
    #                 result += "pf: "+ str(stat(pf))+"\n"
    #                 result += "prec: "+ str(stat(prec))+"\n"
    #                 result += "Default pd: "+ str(stat(dpd))+"\n"
    #                 result += "Default pf: "+ str(stat(dpf))+"\n"
    #                 result += "Default prec: "+ str(stat(dprec))+"\n\n\n"
    #
    #             if tag == "ranking":
    #                 alg = algorithm.attrib["name"]
    #                 ranking[alg] = [float(median(pd)), float(median(pf)), float(median(prec))]
    #
    #
    #             if tag == "charts":
    #                 scores_pd[str(algorithm.attrib["name"])] = []
    #                 scores_pf[str(algorithm.attrib["name"])] = []
    #                 scores_prec[str(algorithm.attrib["name"])] = []
    #                 scores_eval[str(algorithm.attrib["name"])] = []
    #                 scores_pd[str(algorithm.attrib["name"])] = pd
    #                 scores_pf[str(algorithm.attrib["name"])] = pf
    #                 scores_prec[str(algorithm.attrib["name"])] = prec
    #                 scores_eval[str(algorithm.attrib["name"])] = numeval
    #
    #         if tag == "ranking":
    #             ranking["default"] = [median(dpd), median(dpf), median(dprec)]
    #
    #         if tag == "charts":
    #             scores_pd["default"] = []
    #             scores_pf["default"] = []
    #             scores_prec["default"] = []
    #             scores_pd["default"] = dpd
    #             scores_pf["default"] = dpf
    #             scores_prec["default"] = dprec
    #             import sys
    #             f = open(DEFECT_PREDICT_PREFIX + "DefectPredict_chart.txt", 'a+')
    #             sys.stdout = f
    #             print "Problem Name: ", str(problem.attrib["name"])
    #             print "Algorithm: ", str(algorithm.attrib["name"])
    #             names = ["PD", "PF", "PREC", "EVALS"]
    #             for i,x in enumerate([scores_pd, scores_pf, scores_prec, scores_eval]):
    #                 print "Features: ", names[i]
    #                 callrdivdemo(x)
    #             sys.stdout = sys.__stdout__
    #             f.close()
    #
    #         if tag == "ranking":
    #             print problem.attrib["name"] + " : ",
    #             weights = []
    #             for obj in tests.problems[0].objectives:
    #                 # w is negative when we are maximizing that objective
    #                 if obj.lismore:
    #                     weights.append(+1)
    #                 else:
    #                     weights.append(-1)
    #             if problem.attrib["name"] == "default":
    #                 cdom_ranking(tests.problems[0], weights, ranking)
    #             else:
    #                 cdom_ranking([x for x in tests.problems if x.name == problem.attrib["name"]][-1], weights, ranking)
    #
    #
    #
    # if tag == "stats":
    #     f = open(DEFECT_PREDICT_PREFIX + "DefectPredict_report.txt", "w")
    #     f.write(result)
    #     f.close()
    #     print result
    # print "Report saved at : ", DEFECT_PREDICT_PREFIX



    # ----------------------------------------------------------------------

def build_version_space_chart():
    defect_p = open(DEFECT_PREDICT_PREFIX + "version_space.xml", "r")
    parse_version_XML(defect_p)


def aim(problem, lst1, lst2):
    assert(len(problem.objectives) == len(lst1) == len(lst2)), "Objectives are wrong"
    print "# aim -------------> List1: ", lst1
    print "# aim -------------> List2: ", lst2
    ret = True
    for o, i, j in zip(problem.objectives, lst1, lst2):
        print "# aim -------------> o: ", o.lismore
        print "# aim -------------> i: ", lst1
        print "# aim -------------> j: ", lst2
        if o.lismore is False:
            if i > j:
                ret = False
                break
        else:
            if i < j:
                ret = False
                break

    return ret

def returnlist(lst, str):
    for l in lst:
        if l[0] == str.split(".")[-1]:
            return l[1]
    assert(True is False), "Something is wrong"

def version_space_search(jmoo):
    """
    :param problem: Problem that is going to be used
    :param JMOO: JMOO object
    :return: NONE
    """
    def assign(a, b):
        exec("%s = %s" % (a.split(".")[-1], b))
    def dPDPFPREC():
        return PDPF and PFPREC and PDPREC
    def dPDPF():
        return PD and PF
    def dPFPREC():
        return PF and PREC
    def dPDPREC():
        return PD and PREC

    PD = False
    PF = False
    PREC = False
    PDPF = False
    PFPREC = False
    PDPREC = False
    PDPFPREC = False

    defect_p = open(DEFECT_PREDICT_PREFIX + "version_space.xml", "w")
    v_out = ""
    v_out = "<Experiment>\n"
    for algorithm in jmoo.tests.algorithms:
        v_out += "<Algorithm name = \"" + str(algorithm.name) + "\">\n"
        for problem in jmoo.tests.problems:
            v_out += "<Problem name = \"" + str(problem.name) + "\">\n"

            levels = [["jmoo_preprocessor.PD", "jmoo_preprocessor.PF", "jmoo_preprocessor.PREC"],
                       ["jmoo_preprocessor.PDPF", "jmoo_preprocessor.PFPREC", "jmoo_preprocessor.PDPREC"],
                       ["jmoo_preprocessor.PDPFPREC"]]

            dreams = [
                ("PD", [66]), ("PF", [33]), ("PREC", [66]),
                ("PDPF",[66,33]), ("PFPREC", [0,66]), ("PDPREC", [66, 66]),
                ("PDPFPREC", [66, 0, 66])

            ]

            vector_space = [
                ("PDPFPREC",[("PDPF", False), ("PFPREC", False), ("PDPREC", False)]),
                ("PDPF", [("PD", False), ("PF", False)]),
                ("PFPREC", [("PF", False), ("PREC", False)]),
                ("PDPREC", [("PD", False), ("PREC", False)]),
                ("PD", []),
                ("PF", []),
                ("PREC", [])

            ]



            for i, level in enumerate(levels):
                for hypothesis in level:

                        if i != 0:
                            if hypothesis.split(".")[-1] == "PDPF":
                                temp = dPDPF()
                            elif hypothesis.split(".")[-1] == "PDPREC":
                                temp = dPDPREC()
                            elif hypothesis.split(".")[-1] == "PFPREC":
                                temp = dPFPREC()
                            elif hypothesis.split(".")[-1] == "PDPFPREC":
                                temp = dPDPFPREC()
                        else:
                            temp = True

                        if temp is True:
                            if hypothesis.split(".")[-1] == "PD":
                                jmoo_preprocessor.PD = True
                            elif hypothesis.split(".")[-1] == "PF":
                                jmoo_preprocessor.PF = True
                            elif hypothesis.split(".")[-1] == "PREC":
                                jmoo_preprocessor.PREC = True
                            elif hypothesis.split(".")[-1] == "PDPF":
                                jmoo_preprocessor.PDPF = True
                            elif hypothesis.split(".")[-1] == "PDPREC":
                                jmoo_preprocessor.PDPREC = True
                            elif hypothesis.split(".")[-1] == "PFPREC":
                                jmoo_preprocessor.PFPREC = True
                            elif hypothesis.split(".")[-1] == "PDPFPREC":
                                jmoo_preprocessor.PDPFPREC = True
                            problem.change_objective()

                            lst = jmoo.defect_prediction(problem, hypothesis, [algorithm])


                            result = aim(problem, returnlist(dreams, hypothesis), lst)
                            print " # version_space_search -------------> Result: ", result
                            if result is False:
                                print " # version_space_search -------------> Hypothesis: ", hypothesis.split(".")[-1], " did not work", lst
                            else:
                                print " # version_space_search -------------> Hypothesis: ", hypothesis.split(".")[-1], " works!!", lst

                            if hypothesis.split(".")[-1] == "PD":
                                PD = result
                                jmoo_preprocessor.PD = False
                            elif hypothesis.split(".")[-1] == "PF":
                                PF = result
                                jmoo_preprocessor.PF = False
                            elif hypothesis.split(".")[-1] == "PREC":
                                PREC = result
                                jmoo_preprocessor.PREC = False
                            elif hypothesis.split(".")[-1] == "PDPF":
                                PDPF = result
                                jmoo_preprocessor.PDPF = False
                            elif hypothesis.split(".")[-1] == "PDPREC":
                                PDPREC = result
                                jmoo_preprocessor.PDPREC = False
                            elif hypothesis.split(".")[-1] == "PFPREC":
                                PFPREC = result
                                jmoo_preprocessor.PFPREC = False
                            elif hypothesis.split(".")[-1] == "PDPFPREC":
                                PDPFPREC = result
                                jmoo_preprocessor.PDPFPREC = False


                            v_out += "<" + str(hypothesis) + ">\n"
                            v_out += "<Result>" + str(result) + "</Result>\n"
                            v_out += "<List>\n"
                            for i,l in enumerate(lst):
                                v_out += "<p" + str(i) +">" + str(l) + "</p" + str(i) +">\n"
                            v_out += "</List>\n"
                            v_out += "</" + str(hypothesis) + ">\n"


                            print " # version_space_search -------------> ", PD, PF, PREC, PDPF, PFPREC, PDPREC, PDPFPREC

                        else:
                            print " #! version_space_search -------------> Hypothesis: ", hypothesis.split(".")[-1],\
                                " cannot be processed"
                            v_out += "<" + str(hypothesis) + ">\n"
                            v_out += "<Result>False</Result\n>"
                            v_out += "</" + str(hypothesis) + ">\n"

            v_out += "</Problem>\n"

        v_out += "</Algorithm> \n"
    v_out += "</Experiment>\n"

    print v_out
    defect_p.write(v_out)
    print "FILE WRITTEN!"
