import re
import os
from math import log
import math, heapq


def readfile(path, docid):
    files = sorted(os.listdir(path))
    f = open(os.path.join(path, files[docid]), 'r')
    s = f.read()
    f.close()
    return s


def tokenize(text):
    DELIM = '[ \n\t0123456789;:.,/\(\)\"\'-]+'
    return re.split(DELIM, text.lower())



def document_frequencies(path):
    """
    Store document frequency in a dictionary.

    dictionary[term] returns document frequency of a term

    :param path: the path to the directory
    :return: a dictionary that contains term-document frequency
    """

    N = len(sorted(os.listdir(path)))
    docFrequencies = {}  # Store document frequencies in a dictionary
    # The same as how we create a posting dictionary for BR
    for docID in range(N):
        s = readfile(path, docID)
        words = tokenize(s)
        for w in words:
            if w != '':
                if w not in docFrequencies:
                    docFrequencies[w] = {docID}
                else:
                    docFrequencies[w].add(docID)

    # Go through the dictionary and change the values from 'set' to 'len(set)'
    for w in docFrequencies:
        docFrequencies[w] = len(docFrequencies[w])

    return docFrequencies

def vectorise_doctf(doc):
    """
    :param doc: document to be vectorised
    :return: vectorised document represented witha  dictionary
    """
    words = tokenize(doc)  # Split the document in to words
    vectorised_doc = {}  # Vector is represented with a dictionary where the key-value pair is word-termFrequency
    # Go through the document
    for w in words:
        if w != '':
            if w not in vectorised_doc:
                vectorised_doc[w] = 1.0  # term frequency is 1 if the word is not already in the dictionary
            else:
                vectorised_doc[w] += 1.0  # Add 1 to term frequency if the word is already in the dicitonary
    return vectorised_doc


def normalise_vector(vector):
    """
    This function normalise a vector then return it

    :param vector: a document vector
    :return: normalised vector
    """
    magnitude = math.sqrt(sum(map(lambda x: x * x, vector.values())))  # Calculate vector's magnitude (length)
    # Go through the dictionary any divide the weight (term frequency) by the vector's length
    for term in vector:
        vector[term] = vector[term] / magnitude  # tf/length
    return vector


def indextextfiles_RR(path):
    """
    Index text files and return a dictionary
    dictionary[docID] returns the corresponding document's normalised vector

    :param path: path to the directory
    :return: dictionary of documents and their normalised vector
    """
    N = len(os.listdir(path))
    normalised_documents = {}  # dictionary to store all the normalised documents
    # Go through the directory
    for docID in range(N):
        doc = readfile(path, docID)  # Get document with the ID
        vectorised_doc = vectorise_doctf(doc)  # Doc -> vector
        normalised_documents[docID] = normalise_vector(
            vectorised_doc)  # normalise the vector then put it into the dictionary
    return normalised_documents


def vectorise_query(query, docFrequencies, numberOfDocuments):
    """
    This function turns a query into a vector

    :param query: the query string
    :param docFrequencies: document frequency dictionary
    :param numberOfDocuments: total number of documents
    :return:
    """
    vectorQueryIDF = vectorise_doctf(query)  # Turn the query into a vector with raw term frequency as weight
    # Go through the vector then apply the IDF formula to calculate the weight
    for term in vectorQueryIDF:
        if term in docFrequencies:  # if the term is found in any of the documents
            vectorQueryIDF[term] = vectorQueryIDF[term] * log(numberOfDocuments / docFrequencies[term], 10)
        else:  # if the term is NOT found in any of the documents, set its weight to 0.0
            vectorQueryIDF[term] = 0.0
    return vectorQueryIDF


def cosine_similarity(vector_query, normalised_doc):
    """
    Calculate the cosine similarity between a query and a document

    :param vector_query: vectorised query
    :param normalised_doc: normalised document
    :return:
    """
    dotProduct = 0  # Since the document is normalised, the cosine similarity is the dot product
    for term in vector_query:
        if term in normalised_doc:  # if the term is found in this document
            dotProduct += vector_query[term] * normalised_doc[term]  # Calculate the dot product
    return dotProduct


def query_RR(query, normalisedDocs, documentFrequencies):
    """
    :param query: query string
    :param normalisedDocs: dictionary of normalised documents vector
    :param documentFrequencies: dictionary of document frequency of terms
    :return:
    """
    vectorised_query = vectorise_query(query, documentFrequencies, len(normalisedDocs))  # vectorise the query
    rank = []  # A list to store all the ranked documents
    for docID in normalisedDocs:
        cosineSimilarity = cosine_similarity(vectorised_query, normalisedDocs[docID]) # calculate cosine similarity
        rank.append((cosineSimilarity, docID))  # append tuple with the cosine similarity (dot product) and the docID to the list

    return [x[1] for x in heapq.nlargest(10, rank)]  # Return the top 10 tuples with the largest cosine similarity


if __name__ == "__main__":
    documentFrequencies = document_frequencies('docs')
    normalizedDOCs = indextextfiles_RR('docs')

    print(query_RR('England played very well', normalizedDOCs, documentFrequencies))
    print(query_RR('federer australian wimbledon', normalizedDOCs, documentFrequencies))
	

