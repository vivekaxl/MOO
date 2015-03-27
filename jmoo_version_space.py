import jmoo_preprocessor
from jmoo_properties import *

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
        v_out += "<Algorithm name =" + str(algorithm.name) + ">\n"
        for problem in jmoo.tests.problems:
            v_out += "<Problem name =" + str(problem.name) + ">\n"

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
                                v_out += "<" + str(i) +">" + str(l) + "</" + str(i) +">\n"
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
