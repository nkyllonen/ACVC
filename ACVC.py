'''
ACVC: central module for the ACVC application

Alex Berg and Nikki Kyllonen
'''
from __future__ import print_function

import CorpusBuilder, DecisionMaker, State
import os, sys

from textwrap import wrap
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
            
            if len(possibleWords) > 0:
                print("\nPossible words:")
                for word in possibleWords:
                    print(word)
            else:
                print("\nNo possible words found")

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
 
        distances = 0
        MATCH_DATA = ("Word" , "Jaccard Value" , "Matching Corpus Value" , "Hint", "Max Jaccard Value", "Jaccard Distance")
        data = []
        correctTable = AsciiTable([MATCH_DATA, []])
        maxValWidth = correctTable.column_max_width(2)
        maxHintWidth = correctTable.column_max_width(3)
        
        for i in range(len(results[0])):
            result = results[0][i]

            # Calculate jaccard distance
            r = list(result)
            d = float(result[4]) - float(result[1])
            distances += d
            r.append(d)

            # Format text to wrap
            wrappedVal = '\n'.join(wrap(r[2], maxValWidth))
            wrappedHint = '\n'.join(wrap(r[3], maxHintWidth))
            r[2] = wrappedVal
            r[3] = wrappedHint

            if State.DEBUG:
                print(r)

            data.append(r)

        #correctTable.table_data[0][1] = data
        correctTable = AsciiTable(tuple([MATCH_DATA] + data), "Correct Matches Results")
        print("\n" + correctTable.table)

        if (State.SAMPLES != results[2]):
            STATS_DATA = (
                ("Percentage Within Correct" , "Percentage Within Incorrect", "Percentage Within", "Average Jaccard Distance"),
                (len(results[0]) / (State.SAMPLES - results[2]),
                 len(results[1]) / (State.SAMPLES - results[2]),
                 1.0 - (results[2] / State.SAMPLES),
                 distances / len(results[0]) if len(results[0]) > 0 else "NA")
            )
        else:
            STATS_DATA = (
                ("Percentage Within Correct" , "Percentage Within Incorrect", "Percentage Within"),
                (0,0,0)
            )

        statsTable = AsciiTable(STATS_DATA, "Statistics")
        print("\n" + statsTable.table)
