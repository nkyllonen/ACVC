'''
DecisionMaker: module for deciding potential answers

Alex Berg and Nikki Kyllonen
'''
from __future__ import print_function

import State
import string, nltk, random

from nltk.corpus import stopwords
nltk.download("stopwords")

from textwrap import wrap
from terminaltables import AsciiTable

## GLOBAL VARIABLES ##
punc = set(string.punctuation)
engStopWords = set(stopwords.words('english'))


## HELPER FUNCTIONS ##
def clean_string(s):
    """ Remove stopwords and all punctuation """
    words = [ w for w in s.split(" ") if w not in engStopWords ]
    s = " ".join(words)
    return "".join( ch.lower() for ch in s if ch not in punc )


## MODULE FUNCTIONS ##
def get_possible_words(corpus, wordLen, wordHint):
    """ Construct list of possible word matches """

    if State.METRIC == State.Metric.JACCARD:
        possible = use_jaccard_metric(corpus, wordLen, wordHint)
    elif State.METRIC == State.Metric.COSINE:
        # TODO: cosine similarity metric
        possible = [("example", 0.5, "some def")]

    # sort and only keep the top 10 possible words
    possible = sorted(possible, key = lambda x : x[1], reverse=True)[:10]

    return possible


def use_jaccard_metric(corpus, wordLen, wordHint):
    """ Use brute force with jaccard similarity metric """ 
    possible = []
    for word in list(corpus.keys()):
        if len(word) == wordLen:
            maxJaccard = 0
            maxJaccardString = ""
            for val in corpus[word]:
                m = max(maxJaccard, jaccard(wordHint, val))
                if (m != maxJaccard):
                    maxJaccardString = val
                    maxJaccard = m
            if maxJaccard > 0:
                possible.append((word, maxJaccard, maxJaccardString, wordHint))
    return possible


def jaccard(query1, query2):
    """ Calculate the jaccard value between two inputs """
    q1 = set(clean_string(query1).split(" "))
    q2 = set(clean_string(query2).split(" "))

    return len(q1.intersection(q2)) / len(q1.union(q2))


def average_sentence_vec(words):
    """  """
    # TODO: calc sentence feature vector
    return ""


def evaluate_corpus(corpus, golden):
    """ Evaluate the given corpus against given golden standard """
    withinCorrectWords = []
    withinIncorrectWords = []
    withoutNum = 0

    # Randomly sample golden corpus
    sampleWords = random.sample(golden.keys(), State.SAMPLES)
    if State.DEBUG:
        print("[DEBUG] Using sample words:" , sampleWords)

    for answer in sampleWords:
        possibleWords = get_possible_words(corpus, len(answer), random.choice(golden[answer]))

        # Check if possible words contains correct answer
        check = list(filter( lambda x : x[0] == answer , possibleWords ))
        if len(check) > 0:
            # Store corresponding result values + max jaccard of all results
            result = list(check[0])
            result.append(possibleWords[0][1])
            withinCorrectWords.append(result)
            if State.DEBUG:
                print("[DEBUG]" , answer , "CORRECT" , result)
        else:
            # Check if answer is in corpus
            if answer in corpus.keys():
                withinIncorrectWords.append(answer)
            else:
                withoutNum += 1
            if State.DEBUG:
                print("[DEBUG]", answer , "INCORRECT")

    return {"withinCor" : withinCorrectWords, "withinIncor" : withinIncorrectWords, "withoutN" : withoutNum}

def run_evaluation(corpus, golden):
    """ Generate tables containing evaluation data """
    wordsTable, correctTable, statsTable = None, None, None

    results = []
    
    for i in range(State.LOOPS):
        results.append(evaluate_corpus(corpus, golden))
    
    if State.DEBUG:
        # TODO: format this output with labels and a table?
        print("[DEBUG]" , results)
    
    # Only output word result tables if NOT looping --minimize output
    if State.LOOPS == 1:
        # Format output into tables
        WORDS_DATA = (
            ("Within Correct", "Within Incorrect", "Without Number"),
            ("\n".join([ val[0] for val in results[0]["withinCor"] ]) ,
             "\n".join(results[0]["withinIncor"]),
             results[0]["withoutN"])
        )
        wordsTable = AsciiTable(WORDS_DATA, "Word Results")
 
        distances = 0
        MATCH_DATA = ("Word" , "Jaccard Value" , "Matching Corpus Value" , "Hint", "Max Jaccard Value", "Jaccard Distance")
        data = []
        correctTable = AsciiTable([MATCH_DATA, []])
        maxValWidth = correctTable.column_max_width(2)
        maxHintWidth = correctTable.column_max_width(3)
        
        for i in range(len(results[0]["withinCor"])):
            result = results[0]["withinCor"][i]

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

        correctTable = AsciiTable(tuple([MATCH_DATA] + data), "Correct Matches Results")

    # Check if we had any hits at all, otherwise output zeroes
    if (State.SAMPLES != results[0]["withoutN"]):
        STATS_DATA = (
            ("Average Percentage Within Correct" , "Average Percentage Within Incorrect", "Average Percentage Within", "Average Jaccard Distance"),
            (len(results[0]["withinCor"]) / (State.SAMPLES - results[0]["withoutN"]),
             len(results[0]["withinIncor"]) / (State.SAMPLES - results[0]["withoutN"]),
             1.0 - (results[0]["withoutN"] / State.SAMPLES),
             # Calculate if we had any correct hits --avoid div by zero
             distances / len(results[0]["withinCor"]) if len(results[0]["withinCor"]) > 0 else "NA")
        )
    else:
        STATS_DATA = (
            ("Percentage Within Correct" , "Percentage Within Incorrect", "Percentage Within"),
            (0,0,0)
        )

    statsTable = AsciiTable(STATS_DATA, "Statistics")
    return(wordsTable , correctTable ,  statsTable)
