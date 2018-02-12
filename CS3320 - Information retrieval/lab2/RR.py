import re
import os
import numpy
from math import log
from BR import indextextfiles_BR, query_BR


def readfile(path, docid):
    files = sorted(os.listdir(path))
    f = open(os.path.join(path, files[docid]), 'r', encoding='latin-1')
    s = f.read()
    f.close()
    return s


def tokenize(text):
    DELIM = '[ \n\t0123456789;:.,/\(\)\"\'-]+'
    return re.split(DELIM, text.lower())


def indextextfiles_RR(path):
    N = len(sorted(os.listdir(path)))
    postings = {}
    for docID in range(N):
        s = readfile(path, docID)
        words = tokenize(s)
        for w in words:
            if w != '':
                if w not in postings:
                    postings[w] = numpy.zeros(N)
                    postings[w][docID] = 1
                else:
                    postings[w][docID] += 1
    return postings


def query_RR(posting, query):
    return 0


def idf(term, postings):
    # numberOfDocuments = len(sorted(os.listdir(path)))
    # documentFrequency = 0
    # for docID in range(numberOfDocuments):
    #     if term.lower() in tokenize(readfile(path, docID)):
    #         documentFrequency = documentFrequency + 1
    #
    # if documentFrequency > 0:
    #     return 1.0 + log(float(numberOfDocuments) / documentFrequency)
    # else:
    #     return 1.0

    if term not in postings:
        return 1.0
    else:
        documentFrequency = numpy.count_nonzero(postings[term])  # find items that are not 0
        numberOfDocuments = len(postings)
        return log(float(numberOfDocuments) / documentFrequency, 10)


def tf_doc(term, postings, docID):
    if postings[term][docID] == 0.0:
        return 0.0
    else:
        return 1.0 + log(postings[term][docID], 10)

def tf_query(term, query):
    words = tokenize(query)
    if term.lower() not in words:
        return 0.0
    else:
        tf_raw = 0.0
        for w in words:
            if w != '':
                if term == w:
                    tf_raw += 1
        return 1.0 + log(tf_raw, 10)

def df_idf(term, query, postings):
    return tf_query(term, query)*idf(term, postings)

if __name__ == "__main__":
    # print(1 + log(2,10)) #tf
    # print(1.0+log((float(1000000)/1000),10))    #idf
    # print(numpy.zeros(2))
    postings = indextextfiles_RR('docs')
    print(postings['defeat'][610])
    print(idf('defeat', postings))
    print(tf_query('football', 'football is football'))
    #
    # print('going' in s)
