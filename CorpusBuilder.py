"""
CorpusBuilder: module for constructing our personal corpus

Alex Berg and Nikki Kyllonen
"""

import json
import os
import re
import requests

# Merriam Webster API
API_KEY = os.environ['MERRIAM_WEBSTER_API_KEY']
DICTIONARY_BASE_URL = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"

# Paths and data file names
DATA_DIRECTORY = "./data/"
DATA_FILE_NAME = "data.json"
WORDS_LIST_FILE_NAME = "3000_most_common_words.txt"


def collect_dictionary_data():
    """Driver function to collect and add data to the corpus. Select which words from
       the words list file you would like to include."""
    # Specify which words you want to find the definitions for (inclusive on both ends)
    start_index = 500
    end_index = 999

    # Get words to find the definition of
    words = get_words(DATA_DIRECTORY + WORDS_LIST_FILE_NAME, start_index, end_index)

    # Get old and new data to form combined dataset
    old_definitions = load_defs_from_data_file(DATA_DIRECTORY + DATA_FILE_NAME)
    new_definitions = get_new_definitions(words)
    data = {**old_definitions, **new_definitions}

    # Save all data to file
    write_defs_to_data_file(DATA_DIRECTORY + DATA_FILE_NAME, json.dumps(data))


def get_words(filename, start, end):
    """Get a subset of the words in the file from lines start to end."""
    words = []
    line_number = 0
    try:
        with open(filename, "r") as f:
            for word in f:
                if start <= line_number <= end:
                    words.append(word.strip())
                line_number += 1
    except OSError:
        print("Word file '{0}' could not be opened".format(filename))
        return []
    return words


def load_defs_from_data_file(filename):
    """Read JSON definition data from file. If the file is empty or does not exist,
       load an empty JSON."""
    try:
        with open(filename, "r") as f:
            data = f.read()
        if data == "":  # check if file was empty or nonexistent
            data = "{}"
    except OSError:  # file could not be opened (possibly does not exist)
        data = "{}"
    return json.loads(data)


def write_defs_to_data_file(filename, data):
    """Write data to file."""
    with open(filename, "w") as f:
        f.write(data)


def get_new_definitions(words):
    """Create a dictionary of maps of a word to a list of its definitions."""
    definitions = {}
    for word in words:
        definition = get_definition_from_api(word)  # get entire API JSON
        definition = reformat_definition_json(word, definition)  # format the JSON nicely
        definitions = {**definitions, **definition}  # merge new definition into definitions dictionary
    return definitions


def get_definition_from_api(word):
    """Get JSON definition of work from Merriam Webster API."""
    url = DICTIONARY_BASE_URL + word + "?key=" + API_KEY
    response = requests.get(url)
    return response.json()


def json_iterator(json_input, lookup_key):
    """Returns an iterator to get all items from a JSON object with a given key.
       Source: https://stackoverflow.com/a/39016088"""
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from json_iterator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from json_iterator(item, lookup_key)


def reformat_definition_json(word, old_json):
    """Clean up JSON from API to only map a word to a list of its definitions."""
    definitions = []  # list of definitions for the word coming from the big API JSON
    for dt in json_iterator(old_json, "dt"):  # iterate through all "defining text" terms
        # if this is a definition, clean it up and append it (if not empty)
        if isinstance(dt[0][1], str):
            definition = clean_definition(dt[0][1])
            if definition != "":
                definitions.append(definition)
    return {word: definitions}


def clean_definition(definition):
    """Remove curly brace extras, punctuation, and whitespace from definitions."""
    result = re.sub(r"{[|\w\s]*\}", "", definition)  # remove curly brace info
    result = re.sub(r"[^-\w\s]", "", result)  # remove punctuation (except dashes)
    return result.strip()  # trim whitespace from ends
