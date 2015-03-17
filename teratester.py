import os,sys,inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"Problems/tera")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)


from tera_datasets import *

a = ant14()

input = []
for i,arg in enumerate(sys.argv):

    if arg is not None and i > 0:
        input.append(arg)

if len(input) == 0:
    input = [2,2,0.01,0]

    mss = int(round(input[0]))
    msl  = int(round(input[1]))
    mxf = int(round(input[2]))
    thres = int(round(input[3]))
    #cri = "mse"

    output = a.evaluate(input=input)
    output = [float(str("%.2f" % out)) for out in output]
    print [mss, msl, mxf, thres], output
else:
    print "invalid input"