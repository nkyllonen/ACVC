'''
State: module for maintaining the program state

Alex Berg and Nikki Kyllonen
'''
from enum import Enum

class Metric(Enum):
    """ Enum for ACVC metrics """
    JACCARD = 1
    COSINE = 2

class Corpora(Enum):
    """ Enum for ACVC corpora """
    DICTIONARY = 1
    THESAURUS = 2
    GOLDEN = 3

## GLOBAL VARIABLES ##
LABEL = "[ACVC]"
DEBUG = False

# Metrics
METRIC = Metric.JACCARD

# Evaluation
EVAL = False
SAMPLES = 10

# Corpora
CORPORA = Corpora.DICTIONARY

def processCommands(args):
    """ Set up program according to command line arguments """
    global DEBUG, METRIC, SAMPLES, EVAL, CORPORA
    index = 0

    for arg in args: 
        if (arg == "--debug"):
            DEBUG = True
            print(LABEL , "USING DEBUG MODE")
        elif(arg == "--jaccard"):
            METRIC = Metric.JACCARD
        elif(arg == "--cosine"):
            METRIC = Metric.COSINE
        elif(arg == "--eval"):
            EVAL = True
        elif(arg.isnumeric()):
            if index > 0 and args[index-1] == "--eval":
                SAMPLES = int(arg)
                print(LABEL , "EVALUATING USING {} SAMPLES".format(SAMPLES))
        elif(arg == "--dictionary"):
            CORPORA = CORPORA.DICTIONARY
        elif(arg == "--thesaurus"):
            CORPORA = CORPORA.THESAURUS
        elif(arg == "--golden"):
            CORPORA = CORPORA.GOLDEN

        index += 1
    
    print(LABEL , "USING {} METRIC".format(METRIC.name))
    print(LABEL , "USING {} CORPORA".format(CORPORA.name))


