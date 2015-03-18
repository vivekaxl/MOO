import os,sys,inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"Problems/tera")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)




from tera_datasets import *

a = ant()

input = []
for i,arg in enumerate(sys.argv):

    if arg is not None and i > 0:
        input.append(arg)
# <mss>8.8641246794</mss>
# <msl>14.9794761475</msl>
# <mxf>0.929123322772</mxf>
# <threshold>0.915820856764</threshold>


if len(input) == 0:
    input = [8.8641246794, 14.9794761475, 0.929123322772, 0.915820856764]
    input_wei = [8, 16, 1, 0.5]

    mss = int(round(input[0]))
    msl  = int(round(input[1]))
    mxf = float(input[2])
    thres = float(input[3])
    #cri = "mse"

    output = a.test(input=input)
    default = a.default()
    output = [float(str("%.2f" % out)) for out in output]

    output2 = a.test(input=input_wei)
    #print [mss, msl, mxf, thres], output
    print "Vivek: ", output
    print "Default: ", default
    print "Wei: ", output2
else:
    print "invalid input"