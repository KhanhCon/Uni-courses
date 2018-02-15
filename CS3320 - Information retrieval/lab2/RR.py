import re
import os
import numpy
from math import log
from BR import indextextfiles_BR, query_BR
import math, heapq


def readfile(path, docid):
    files = sorted(os.listdir(path))
    f = open(os.path.join(path, files[docid]), 'r', encoding='latin-1')
    s = f.read()
    f.close()
    return s


def tokenize(text):
    DELIM = '[ \n\t0123456789;:.,/\(\)\"\'-]+'
    return re.split(DELIM, text.lower())


def document_frequencies(path):
    N = len(sorted(os.listdir(path)))
    docFrequencies = {}
    for docID in range(N):
        s = readfile(path, docID)
        words = tokenize(s)
        for w in words:
            if w != '':
                if w not in docFrequencies:
                    docFrequencies[w] = {docID}
                else:
                    docFrequencies[w].add(docID)

    for w in docFrequencies:
        docFrequencies[w] = len(docFrequencies[w])

    return docFrequencies


def vector_query(query, docFrequencies):
    words = tokenize(query)
    vectorQueryIDF = {}
    for w in words:
        if w != '':
            if w not in vectorQueryIDF:
                # postings[w] = numpy.zeros(N)
                vectorQueryIDF[w] = 1.0
            else:
                vectorQueryIDF[w] += 1.0
    N = len(docFrequencies)
    for term in vectorQueryIDF:
        if term in docFrequencies:
            vectorQueryIDF[term] = (1.0 + log(vectorQueryIDF[term], 10))*log(N/docFrequencies[term], 10)
        else:
            vectorQueryIDF[term] = 0
    return vectorQueryIDF

def vector_doctf(path):
    N = len(sorted(os.listdir(path)))
    postings = {}
    for docID in range(N):
        s = readfile(path, docID)
        words = tokenize(s)
        postings[docID] = {}
        for w in words:
            if w != '':
                if w not in postings[docID]:
                    # postings[w] = numpy.zeros(N)
                    postings[docID][w] = 1.0
                else:
                    postings[docID][w] += 1.0

    return postings


def vector_doclf(path):
    vectorDoctf = vector_doctf(path)
    for docID in range(len(vectorDoctf)):
        for term in vectorDoctf[docID]:
            vectorDoctf[docID][term] = 1.0 + log(vectorDoctf[docID][term], 10)
    return vectorDoctf


def vector_doc_normalized(path):
    vectorDoclf = vector_doclf(path)
    for docID in range(len(vectorDoclf)):
        coef = math.sqrt(sum(map(lambda x: x * x, vectorDoclf[docID].values())))
        for term in vectorDoclf[docID]:
            vectorDoclf[docID][term] = vectorDoclf[docID][term] / coef
    return vectorDoclf

def query_RR(query, normalizedDoc, documentFrequencies):

    vectorQuery = vector_query(query, documentFrequencies)
    vectorQueryMagnitude = math.sqrt(sum(map(lambda x: x * x, vectorQuery.values())))
    rank = []
    for docID in normalizedDoc:
        dotProduct = 0
        for term in vectorQuery:
            if term in normalizedDoc[docID]:
                dotProduct += vectorQuery[term] * normalizedDoc[docID][term]
        vectorDocMagnitude = math.sqrt(sum(map(lambda x: x * x, normalizedDoc[docID].values())))
        if vectorQueryMagnitude != 0:
            cosineSimilarity = dotProduct/(vectorQueryMagnitude*vectorDocMagnitude)
        else:
            cosineSimilarity = 0.0
        rank.append((cosineSimilarity, docID))

    return heapq.nlargest(10, rank)

def indextextfiles_RR(path):
    N = len(sorted(os.listdir(path)))
    postings = {}
    for docID in range(N):
        s = readfile(path, docID)
        words = tokenize(s)
        for w in words:
            if w != '':
                if w not in postings:
                    # postings[w] = numpy.zeros(N)
                    postings[w] = {}
                    postings[w][docID] = 1.0
                else:
                    if docID in postings[w]:
                        postings[w][docID] += 1.0
                    else:
                        postings[w][docID] = 1.0
    return postings

############# ABOVE IS THE FINAL VERSION


# def idf(term, postings):
#     # numberOfDocuments = len(sorted(os.listdir(path)))
#     # documentFrequency = 0
#     # for docID in range(numberOfDocuments):
#     #     if term.lower() in tokenize(readfile(path, docID)):
#     #         documentFrequency = documentFrequency + 1
#     #
#     # if documentFrequency > 0:
#     #     return 1.0 + log(float(numberOfDocuments) / documentFrequency)
#     # else:
#     #     return 1.0
#
#     if term not in postings:
#         return 1.0
#     else:
#         # documentFrequency = numpy.count_nonzero(postings[term])  # find items that are not 0
#         # print(numpy.nonzero(postings[term]))
#         documentFrequency = len(postings[term])
#         numberOfDocuments = len(postings)
#         return log(float(numberOfDocuments) / documentFrequency, 10)
# def tf_doc(term, postings, docID):
#     # if postings[term][docID] == 0.0:
#     if term not in postings:
#         return 0.0
#     elif docID not in postings[term]:
#         return 0.0
#     else:
#         return 1.0 + log(postings[term][docID], 10)
# def tf_query(term, text):
#     words = tokenize(text)
#     if term.lower() not in words:
#         return 0.0
#     else:
#         tf_raw = 0.0
#         for w in words:
#             if w != '':
#                 if term == w:
#                     tf_raw += 1
#         return 1.0 + log(tf_raw, 10)
# def df_idf(term, query, postings):
#     return tf_query(term, query) * idf(term, postings)
# def query_RR1(postings, query):
#     N = len(sorted(os.listdir('docs')))  # number of documents
#     words = tokenize(query)
#     query_weight = {}
#     for w in words:
#         query_weight[w] = df_idf(w, query, postings)
#
#     rank = []
#     for docID in range(N):
#         doc_weights = {}
#         for w in words:
#             doc_weights[w] = tf_doc(w, postings, docID)
#         coef = math.sqrt(sum(map(lambda x: x * x, doc_weights.values())))
#         if coef != 0:
#             for w in doc_weights:
#                 doc_weights[w] = doc_weights[w] / coef
#         score = 0
#         for w in words:
#             score += query_weight[w] * doc_weights[w]
#         rank.append((score, docID))
#     return heapq.nlargest(10, rank)


if __name__ == "__main__":
    # print(1 + log(2,10)) #tf
    # print(1.0+log((float(1000000)/1000),10))    #idf
    # print(numpy.zeros(2))

    # print(postings['defeat'][610])
    # print(idf('defeat', postings))
    # print(tf_query('football', 'football is football'))
    # postings = indextextfiles_RR('docs')
    # print(query_RR(postings,'football england defeat') == query_RR(postings,'football england defeat vietnam'))
    # documentFrequencies = document_frequencies('docs')
    # print(documentFrequencies['defeat'])

    normalizedDOCs = vector_doc_normalized('docs')
    documentFrequencies = document_frequencies('docs')
    print(query_RR('Blackburn ', normalizedDOCs, documentFrequencies))
    #
    # print('going' in s)