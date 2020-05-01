'''
ACVC: central module for the ACVC application

Alex Berg and Nikki Kyllonen
'''

import CorpusBuilder, DecisionMaker, State
import os, sys

# Requires python-dotenv to be installed
from dotenv import load_dotenv

# Python3 only
from pathlib import Path

## GLOBAL VARIABLES ##

## MAIN FUNCTION ##
if __name__ == "__main__":
    """ Main function driving program """
    # Process command line input
    State.processCommands(sys.argv)

    # Load local .env file if it exists
    env_path = Path(".") / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

        if State.DEBUG:
            print("[DEBUG] MERRIAM_WEBSTER_DICTIONARY_API_KEY:",
                  os.getenv("MERRIAM_WEBSTER_DICTIONARY_API_KEY"))
            print("[DEBUG] MERRIAM_WEBSTER_THESAURUS_API_KEY:",
                  os.getenv("MERRIAM_WEBSTER_THESAURUS_API_KEY"))
    else:
        print("NO .env FILE FOUND.")

    # Load corpus
    corpus = CorpusBuilder.load_data_from_data_file("data/definition_data.json")

    # User input + Get possible words
    prompting = True

    while (prompting):
        wordLen = int(input("\nLength of mystery word: "))
        wordHint = str(input("Hint for mystery word: "))

        if State.DEBUG:
            print("[DEBUG]" , DecisionMaker.cleanString(wordHint))

        possibleWords = DecisionMaker.getPossibleWords(corpus, wordLen, wordHint)
        
        print("\nPossible words:")
        for word in possibleWords:
            # only output non-zero similarity values
            if word[1] > 0:
                print(word)

        prompting = True if str(input("\nContinue? (y/n) ")) == "y" else False
