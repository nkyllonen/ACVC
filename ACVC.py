'''
ACVC: central module for the ACVC application

Alex Berg and Nikki Kyllonen
'''
import CorpusBuilder, DecisionMaker, State, GoldStandardBuilder
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
    #CorpusBuilder.setup_keys()  
    corpus = {}
    if State.CORPORA == State.CORPORA.DICTIONARY:
        corpus = CorpusBuilder.load_data_from_data_file(State.DICT_FILE)
    elif State.CORPORA == State.CORPORA.THESAURUS:
        corpus = CorpusBuilder.load_data_from_data_file(State.THESA_FILE)
    elif State.CORPORA == State.CORPORA.GOLDEN:
        corpus = CorpusBuilder.load_data_from_data_file(State.GOLDEN_FILE)
        
    if State.BUILD_GOLD:
        GoldStandardBuilder.build_gold_standard()
        exit()
     
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
        wordsTable, correctTable, statsTable = DecisionMaker.run_evaluation(corpus, golden)
        print("\n" + wordsTable.table) if wordsTable != None else print()
        print("\n" + correctTable.table) if correctTable != None else print()
        print("\n" + statsTable.table) if statsTable != None else print()

