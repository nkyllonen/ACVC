'''
DecisionMaker: module for deciding potential answers

Alex Berg and Nikki Kyllonen
'''
import State
import string, nltk, random

from nltk.corpus import stopwords
nltk.download("stopwords")


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
        #if answer in [ possible[0] for possible in possibleWords ]:
        check = list(filter( lambda x : x[0] == answer , possibleWords ))
        if len(check) > 0:
            withinCorrectWords.append(check[0])
            if State.DEBUG:
                print("[DEBUG]" , answer , "CORRECT")
        else:
            # Check if answer is in corpus
            if answer in corpus.keys():
                withinIncorrectWords.append(answer)
            else:
                withoutNum += 1
            if State.DEBUG:
                print("[DEBUG]", answer , "INCORRECT")

    return (withinCorrectWords, withinIncorrectWords, withoutNum)
