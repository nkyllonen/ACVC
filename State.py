'''
State: module for maintaining the program state

Alex Berg and Nikki Kyllonen
'''

## GLOBAL VARIABLES ##
LABEL = "[ACVC]"
DEBUG = False
JACCARD = True
WORD2VEC = False

def processCommands(args):
    """ Set up program according to command line arguments """
    global DEBUG, JACCARD, WORD2VEC

    for arg in args:
        if (arg == "--debug"):
            DEBUG = True
            print(LABEL , "USING DEBUG MODE")
        elif(arg == "--jaccard"):
            JACCARD = True
            print(LABEL , "USING JACCARD METRIC")
        elif(arg == "--word2vec"):
            JACCARD = False
            WORD2VEC = True
            print(LABEL , "USING COSINE SIMULARITY WITH AVERAGE SENTENCE VECTORS")
