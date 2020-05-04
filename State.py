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
# TODO: flesh out help menu output
HELP_MENU = """ Help Menu... """

# Default Metrics
METRIC = Metric.JACCARD

# Default Evaluation
EVAL = False
SAMPLES = 10
LOOPS = 1

# Default Corpora
DICT_FILE = "data/definition_data.json"
THESA_FILE = "data/synonym_data.json"
GOLDEN_FILE = "data/answer_clue_data_backup_pretty.json"
CORPORA = Corpora.DICTIONARY
BUILD_GOLD = False

def processCommands(args):
    """ Set up program according to command line arguments """
    global DEBUG, METRIC, SAMPLES, LOOPS, EVAL, CORPORA, BUILD_GOLD
    index = 0

    # Set up current state
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
            elif index > 0 and args[index-1].isnumeric():
                LOOPS = int(arg)
        elif(arg == "--dictionary"):
            CORPORA = CORPORA.DICTIONARY
        elif(arg == "--thesaurus"):
            CORPORA = CORPORA.THESAURUS
        elif(arg == "--golden"):
            CORPORA = CORPORA.GOLDEN
        elif(arg == "--buildgold"):
            BUILD_GOLD = True
            print(LABEL , "ADDING TO GOLDEN STANDARD CORPUS")
        elif(arg == "--help"):
            print(HELP_MENU)
            exit()

        index += 1

    # Output current state
    if not BUILD_GOLD:
        print(LABEL , "USING {} METRIC".format(METRIC.name))
        print(LABEL , "USING {} CORPORA".format(CORPORA.name))
        if EVAL:
            print(LABEL , "EVALUATING USING {0} SAMPLES and {1} LOOPS".format(SAMPLES, LOOPS))
