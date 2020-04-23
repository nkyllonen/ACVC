'''
ACVC: central module for the ACVC application

Alex Berg and Nikki Kyllonen
'''

import CorpusBuilder, DecisionMaker
import os

# Requires python-dotenv to be installed
from dotenv import load_dotenv

# Python3 only
from pathlib import Path

# Global Flags
DEBUG = True

if __name__ == "__main__":
    """ Load local .env file if it exists """
    env_path = Path(".") / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

        if DEBUG:
            print(os.getenv("MERRIAM_WEBSTER_API_KEY"))
            #print(os.environ["MERRIAM_WEBSTER_API_KEY"])
    else:
        print("NO .env FILE FOUND.")

    CorpusBuilder.collect_dictionary_data()
