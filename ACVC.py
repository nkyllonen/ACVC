'''
ACVC: central module for the ACVC application

Alex Berg and Nikki Kyllonen
'''
from __future__ import print_function

import CorpusBuilder, DecisionMaker, State
import os, sys

from tabulate import tabulate

from terminaltables import AsciiTable

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
    corpus = {}
    if State.CORPORA == State.CORPORA.DICTIONARY:
        corpus = CorpusBuilder.load_data_from_data_file(State.DICT_FILE)
    elif State.CORPORA == State.CORPORA.THESAURUS:
        corpus = CorpusBuilder.load_data_from_data_file(State.THESA_FILE)
    elif State.CORPORA == State.CORPORA.GOLDEN:
        corpus = CorpusBuilder.load_data_from_data_file(State.GOLDEN_FILE)

    # User input + Get possible words
    if not State.EVAL:
        prompting = True

        while (prompting):
            wordLen = int(input("\nLength of mystery word: "))
            wordHint = str(input("Hint for mystery word: "))

            if State.DEBUG:
                print("[DEBUG] Cleaned hint:" , DecisionMaker.clean_string(wordHint))

            possibleWords = DecisionMaker.get_possible_words(corpus, wordLen, wordHint)
            
            print("\nPossible words:")
            for word in possibleWords:
                # only output non-zero similarity values
                if word[1] > 0:
                    print(word)

            prompting = True if str(input("\nContinue? (y/n) ")) == "y" else False

    # Evaluate
    else:
        golden = CorpusBuilder.load_data_from_data_file(State.GOLDEN_FILE)
        results = DecisionMaker.evaluate_corpus(corpus, golden)
        
        if State.DEBUG:
            # TODO: format this output with labels and a table?
            print("[DEBUG]" , results)
        
        # Format output into tables
        WORDS_DATA = (
            ("Within Correct", "Within Incorrect", "Without Number"),
            ("\n".join([ val[0] for val in results[0] ]) ,
             "\n".join(results[1]),
             results[2])
        )
        wordsTable = AsciiTable(WORDS_DATA, "Word Results")
        print("\n" + wordsTable.table)
 
        results[0].insert(0, ("Word" , "Jaccard Value" , "Matching Corpus Value" , "Hint"))
        correctTable = AsciiTable(tuple(results[0]), "Correct Matches Results")
        print("\n" + correctTable.table)

