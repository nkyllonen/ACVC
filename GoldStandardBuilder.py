"""
GoldStandardBuilder: module for building a dataset of actual crossword clues and answers

Alex Berg and Nikki Kyllonen
"""

import json
import re
import requests
import threading


# Website with clues and answers
SOLVER_BASE_URL = "https://www.crosswordsolver.org"

# File paths
DATA_DIRECTORY = "./data/"
ANSWER_CLUE_DATA_FILE_NAME = "answer_clue_data.json"

# List of (answer, clue) tuples (will be modified)
answer_clue_pairs = []


# Driver function for building the gold standard

def build_gold_standard():
    """Build a JSON mapping words to a list of their definitions and save it to a file.
       Do this for clues starting with each letter in the alphabet for a specified number
       per letter. Also specify the number of threads to use when getting the answers
       for each clue."""
    clue_letters = "abcdefghijklmnopqrstuvwxyz"  # letters for the start of the clues
    num_clues_per_letter = 2000  # number of clues to get per letter
    num_threads = 16  # num threads to use when getting the answers during each letter (letters are done sequentially)

    for letter in clue_letters:
        print("On letter " + letter)
        get_answer_clue_pairs_for_letter(letter, num_clues_per_letter, num_threads)
    dictionary = build_dictionary()
    write_data_to_data_file(DATA_DIRECTORY + ANSWER_CLUE_DATA_FILE_NAME, json.dumps(dictionary))


# Helper functions

def get_clue_url_pairs_for_letter(letter):
    """Returns a list of tuples with a clue and url to the site with the answer."""
    # Get HTML of site with table of clues
    url = SOLVER_BASE_URL + "/clues/" + letter
    html_data = requests.get(url)

    # Pull out HTML segments with clues and link to answer
    pattern = r"<a href=\"/clues/{}/.*?</a>".format(letter)
    html_clues = re.findall(pattern, html_data.text)

    # Build a list of (clue, answer url) tuples
    pairs = []
    for html_clue in html_clues:
        clue = re.search(r">.*?<", html_clue).group(0)[1:-1]  # extract clue
        path_params = re.search(r"\".*?\"", html_clue).group(0)[1:-1]  # extract path parameters for url
        pairs.append((clue, SOLVER_BASE_URL + path_params))

    return pairs


def get_answer(url):
    """Returns the answer to a clue from the url (from www.crosswordsolver.org)."""
    try:
        html_data = requests.get(url)  # get the site HTML
    except Exception as ex:
        print("Exception of type " + str(type(ex)))
        print("Problem with url " + url)
        return None

    # Extract the word from the HTML fragment and return it
    pattern = r"<div class='word'>.*?</div>"
    answer = re.search(pattern, html_data.text).group(0)[18:-6]
    return answer.lower()


def add_answer_clue_pair(clue, url):
    """Add an (answer, clue) pair to the global list of such pairs."""
    global answer_clue_pairs
    answer = get_answer(url)
    if answer is not None:
        answer_clue_pairs.append((answer, clue))


def get_answer_clue_pairs_for_letter(letter, num_pairs=10, num_threads=2):
    """For a given letter, add num_pairs number of (answer, clue) pairs to the global list
       of such pairs. Do this with num_threads number of threads."""
    pairs = get_clue_url_pairs_for_letter(letter)
    total_num_pairs = len(pairs)

    num_pairs = min(num_pairs, total_num_pairs)  # we cannot get more pairs than there are

    i = 0  # index we are on
    while i < total_num_pairs:
        threads = []
        threads_used = 0
        while threads_used < num_threads and i < total_num_pairs:
            clue, url = pairs[i]
            threads.append(threading.Thread(target=add_answer_clue_pair, args=(clue, url)))
            num_threads += 1
            i += total_num_pairs // num_pairs
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


def build_dictionary():
    """Build a dictionary of words to a list of clues that had them as the answer. The
       words and clues come from the global list of pairs."""
    # Get existing answers and clues
    dictionary = load_data_from_data_file(DATA_DIRECTORY + ANSWER_CLUE_DATA_FILE_NAME)

    # Add new answers and clues to data
    for answer, clue in answer_clue_pairs:
        if answer not in dictionary:
            dictionary[answer] = []
        if clue not in dictionary[answer]:
            dictionary[answer].append(clue)

    return dictionary


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
