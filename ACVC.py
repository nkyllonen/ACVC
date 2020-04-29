'''
ACVC: central module for the ACVC application

Alex Berg and Nikki Kyllonen
'''

import CorpusBuilder, DecisionMaker
import os, sys

# Requires python-dotenv to be installed
from dotenv import load_dotenv

# Python3 only
from pathlib import Path

## GLOBAL VARIABLES ##
DEBUG = False
JACCARD = True
LABEL = "[ACVC]"

## HELPER FUNCTIONS ##
def processCommands(args):
    """ Set up program according to command line arguments """
    global DEBUG, JACCARD

    for arg in args:
        if (arg == "--debug"):
            DEBUG = True
            print(LABEL , "USING DEBUG MODE")
        elif(arg == "--jaccard"):
            JACCARD = True
            print(LABEL , "USING JACCARD METRIC")

## MAIN FUNCTION ##
if __name__ == "__main__":
    """ Main function driving program """
    # Process command line input
    processCommands(sys.argv)

    # Load local .env file if it exists
    env_path = Path(".") / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

        if DEBUG:
            print("[DEBUG] MERRIAM_WEBSTER_API_KEY:" ,
                    os.getenv("MERRIAM_WEBSTER_API_KEY"))
    else:
        print("NO .env FILE FOUND.")

    # Load corpus
    corpus = CorpusBuilder.load_defs_from_data_file("data/data.json")

    # User input + Get possible words
    prompting = True

    while (prompting):
        wordLen = int(input("\nLength of mystery word: "))
        wordHint = str(input("Hint for mystery word: "))

        if DEBUG:
            print("[DEBUG]" , DecisionMaker.cleanString(wordHint))

        possibleWords = DecisionMaker.getPossibleWords(corpus, wordLen, wordHint)
        
        print("\nPossible words:")
        for word in possibleWords:
            # only output non-zero similarity values
            if word[1] > 0:
                print(word)

        prompting = True if str(input("\nContinue? (y/n) ")) == "y" else False
