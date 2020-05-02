'''
State: module for maintaining the program state

Alex Berg and Nikki Kyllonen
'''

## GLOBAL VARIABLES ##
LABEL = "[ACVC]"
DEBUG = False
JACCARD = True
COSINE = False
METRIC = "JACCARD"

# Evaluation Variables
EVAL = False
SAMPLES = 10

def processCommands(args):
    """ Set up program according to command line arguments """
    global DEBUG, JACCARD, WORD2VEC, METRIC, SAMPLES, EVAL
    index = 0

    for arg in args: 
        if (arg == "--debug"):
            DEBUG = True
            print(LABEL , "USING DEBUG MODE")
        elif(arg == "--jaccard"):
            JACCARD = True
            METRIC = "JACCARD"
            print(LABEL , "USING JACCARD METRIC")
        elif(arg == "--cosine"):
            JACCARD = False
            COSINE = True
            METRIC = "COSINE"
            print(LABEL , "USING COSINE SIMULARITY METRIC")
        elif(arg == "--eval"):
            EVAL = True
        elif(arg.isnumeric()):
            if index > 0 and args[index-1] == "--eval":
                SAMPLES = int(arg)
                print(LABEL , "EVALUATING {0} METRIC USING {1} SAMPLES".format(
                                METRIC, SAMPLES))
        index += 1
