"""
CorpusBuilder: module for constructing our personal corpus

Alex Berg and Nikki Kyllonen
"""

import json
import os
import re
import requests


# Merriam Webster API
DICTIONARY_API_KEY = "" 
THESAURUS_API_KEY = ""
DICTIONARY_BASE_URL = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
THESAURUS_BASE_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"

# Paths and data file names
DATA_DIRECTORY = "./data/"
DEFINITION_DATA_FILE_NAME = "definition_data.json"
SYNONYM_DATA_FILE_NAME = "synonym_data.json"
WORDS_LIST_FILE_NAME = "3000_most_common_words.txt"


# Driver functions for getting either definitions or synonyms from the APIs
def setup_keys():
    """Driver function to set global API keys."""
    global DICTIONARY_API_KEY, THESAURUS_API_KEY
    DICTIONARY_API_KEY = os.environ["MERRIAM_WEBSTER_DICTIONARY_API_KEY"]
    THESAURUS_API_KEY = os.environ["MERRIAM_WEBSTER_THESAURUS_API_KEY"]


def collect_dictionary_data():
    """Driver function to collect and add definitions to the corpus. Select which words from
       the words list file you would like to include."""
    # Specify which words you want to find the definitions for (inclusive on both ends)
    start_index = 2000
    end_index = 2999

    # Get words to find the definition of
    words = get_words(DATA_DIRECTORY + WORDS_LIST_FILE_NAME, start_index, end_index)

    # Get old and new data to form combined dataset
    old_definitions = load_data_from_data_file(DATA_DIRECTORY + DEFINITION_DATA_FILE_NAME)
    new_definitions = get_new_definitions(words)
    data = {**old_definitions, **new_definitions}

    # Save all data to file
    write_data_to_data_file(DATA_DIRECTORY + DEFINITION_DATA_FILE_NAME, json.dumps(data))


def collect_thesaurus_data():
    """Driver function to collect and add synonyms to the corpus. Select which words from
           the words list file you would like to include."""
    # Specify which words you want to find the synonyms for (inclusive on both ends)
    start_index = 1000
    end_index = 1999

    # Get words to find synonyms for
    words = get_words(DATA_DIRECTORY + WORDS_LIST_FILE_NAME, start_index, end_index)
    old_synonyms = load_data_from_data_file(DATA_DIRECTORY + SYNONYM_DATA_FILE_NAME)
    new_synonyms = get_new_synonyms(words)
    data = {**old_synonyms, **new_synonyms}

    # Save all data to synonym file
    write_data_to_data_file(DATA_DIRECTORY + SYNONYM_DATA_FILE_NAME, json.dumps(data))


# Functions specific for getting definition data from a dictionary

def get_new_definitions(words):
    """Create a dictionary of maps of a word to a list of its definitions."""
    definitions = {}
    for word in words:
        definition = get_word_data_from_api(word, DICTIONARY_BASE_URL, DICTIONARY_API_KEY)  # get entire API JSON
        definition = reformat_definition_json(word, definition)  # format the JSON nicely
        definitions = {**definitions, **definition}  # merge new definition into definitions dictionary
    return definitions


def reformat_definition_json(word, old_json):
    """Clean up JSON from dictionary API to only map a word to a list of its definitions."""
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


# Functions specific for getting synonym data from a thesaurus

def get_new_synonyms(words):
    """Create a dictionary of maps of a word to a list of its synonyms."""
    synonyms = {}
    for word in words:
        synonym = get_word_data_from_api(word, THESAURUS_BASE_URL, THESAURUS_API_KEY)  # get entire API JSON
        synonym = reformat_thesaurus_json(word, synonym)  # reformat the JSON to our specification
        synonyms = {**synonyms, **synonym}  # merge new synonym into synonyms dictionary
    return synonyms


def reformat_thesaurus_json(word, old_json):
    """Clean up JSON from thesaurus API to only map a word to a list of its synonyms
       and related words."""
    synonyms = []  # list of synonyms and related words coming from the big API JSON
    for syn_list in json_iterator(old_json, "syn_list"):  # iterate through synonyms
        for wd in json_iterator(syn_list, "wd"):
            synonyms.append(wd)
    for rel_list in json_iterator(old_json, "rel_list"):  # iterate through related words
        for wd in json_iterator(rel_list, "wd"):
            synonyms.append(wd)
    return {word: synonyms}


# Utility functions - used for both definitions and synonyms

def get_word_data_from_api(word, base_url, key):
    """Get JSON data of word from Merriam Webster API."""
    url = base_url + word + "?key=" + key
    response = requests.get(url)
    return response.json()


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


def load_data_from_data_file(filename):
    """Read JSON data from file. If the file is empty or does not exist, load an
       empty JSON."""
    try:
        with open(filename, "r") as f:
            data = f.read()
        if data == "":  # check if file was empty or nonexistent
            data = "{}"
    except OSError:  # file could not be opened (possibly does not exist)
        data = "{}"
    return json.loads(data)


def write_data_to_data_file(filename, data):
    """Write data to file."""
    with open(filename, "w") as f:
        f.write(data)


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
