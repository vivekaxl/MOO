
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

"Brief notes"
"Property File.  Defines default settings."

from jmoo_algorithms import *
from jmoo_problems import *
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"Problems/tera")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from tera_dataset import *
from tera_datasets_WHERE import *
from tera_dataset_RF import *



# JMOO Experimental Definitions
algorithms = [
              jmoo_GALE(),
               jmoo_NSGAII(),
              # #
              jmoo_SPEA2(),
              jmoo_DE()

              ]

#problems = [defect_prediction([ant14()], [ant15()], [ant16()])]#srinivas(), fonseca(3)]


problems =[
       camel(), ant(),  forrest(), ivy(), jedit(), lucene(), poi(), synapse(), velocity(), xerces(),
     #antRF()  , camelRF(),  forrestRF(), ivyRF(), jeditRF(), luceneRF(), poiRF(), synapseRF(), velocityRF(), xercesRF(),
     #antW()  , camelW(),  forrestW(), ivyW(), jeditW(), luceneW(), poiW(), synapseW(), velocityW(), xercesW()


]


build_new_pop = False                                       # Whether or not to rebuild the initial population


# JMOO Universal Properties
repeats = 1     #Repeats of each MOEA
MU      = 100   #Population Size
PSI     = 20    #Maximum number of generations

# Properties of GALE
GAMMA   = 0.15  #Constrained Mutation Parameter
EPSILON = 1.00  #Continuous Domination Parameter
LAMBDA =  3     #Number of lives for bstop

# Propoerties of DE
F = 0.75 # extrapolate amount
CF = 0.3 # prob of cross over

# Properties of Culling
CULLING_PD = 66
CULLING_PF = 33



# File Names
DATA_PREFIX        = "data/"
DEFECT_PREDICT_PREFIX = "defect_prediction/"

"decision bin tables are a list of decisions and objective scores for a certain model"
DECISION_BIN_TABLE = "decision_bin_table"

"result scores are the per-generation list of IBD, IBS, numeval,scores and change percents for each objective - for a certain model"
RESULT_SCORES      = "result_"

SUMMARY_RESULTS    = "summary_"

RRS_TABLE = "RRS_TABLE_"
DATA_SUFFIX        = ".datatable"


