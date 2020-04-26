'''
DecisionMaker: module for deciding potential answers

Alex Berg and Nikki Kyllonen
'''
import string

## GLOBAL VARIABLES ##
punc = set(string.punctuation)

## HELPER FUNCTIONS ##
def cleanString(s):
    return "".join( ch.lower() for ch in s if ch not in punc )

## MODULE FUNCTIONS ##
def getPossibleWords(corpus, wordLen, wordHint):
    """ Construct list of possible word matches """
    possible = []

    for word in list(corpus.keys()):
        if len(word) == wordLen:
            #print(word , ":" , corpus[word])

            maxJaccard = 0
            maxVal = ""
            for val in corpus[word]:
                m = max(maxJaccard, jaccard(wordHint, val))
                if (m != maxJaccard):
                    maxVal = val
                    maxJaccard = m
            possible.append((word, maxJaccard, maxVal))

    # sort and only keep the top 5 possible words
    possible = sorted(possible, key = lambda x : x[1], reverse=True)[:10]

    return possible

def jaccard(query1, query2):
    """ Calculate the jaccard value between two inputs """
    q1 = set(cleanString(query1).split(" "))
    q2 = set(cleanString(query2).split(" "))

    return len(q1.intersection(q2)) / len(q1.union(q2))
