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
HELP_MENU = """
    DEBUGGIN:
    --debug
        verbose terminal output to help with debugging

    CORPUS OPTIONS:
    --dictionary
        generate or evaluate suggestions using the dictionary corpus
    --thesaurus
        generate or evaluate suggestions using the thesaurus corpus
    --golden
        generate or evaluate suggestions using the golden corpus

    METRIC OPTIONS:
    --jaccard
        generate or evaluate suggestions using the jaccard metric
    --cosine
        generate or evaluate suggestions using cosine simularity

    EXPANDING GOLDEN CORPUS:
    --buildgolden
        will negate any other options given except for --help

    EVALUATION OPTIONS:
    --eval <opt: number of samples> <opt: number of loops>
        default to 10 samples and 1 loop when evaluating suggestions
"""

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
    global DEBUG, METRIC, SAMPLES, LOOPS, EVAL, CORPORA, BUILD_GOLD, GOLDEN_FILE
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
        elif(arg == "--works" and CORPORA == Corpora.DICTIONARY):
            GOLDEN_FILE = "data/answer_clue_data_dict_works.json"
            print(LABEL, "USING GOLDEN CORPUS CONTAINING DICTIONARY HITS")

        index += 1

    # Output current state
    if not BUILD_GOLD:
        print(LABEL , "USING {} METRIC".format(METRIC.name))
        print(LABEL , "USING {} CORPUS".format(CORPORA.name))
        if EVAL:
            print(LABEL , "EVALUATING USING {0} SAMPLES and {1} LOOP(S)".format(SAMPLES, LOOPS))