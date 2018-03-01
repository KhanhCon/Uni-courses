
# coding: utf-8

# In[106]:


import re
import os
from math import log
import math, heapq


# ## tokenization and readfile
# 

# In[107]:


def tokenize(text):
    DELIM = '[ \n\t0123456789;:.,/\(\)\"\'-]+'
    return re.split(DELIM, text.lower())


# In[108]:


def readfile(path, docid):
    files = sorted(os.listdir(path))
    f = open(os.path.join(path, files[docid]), 'r', encoding='latin-1')
    s = f.read()
    f.close()
    return s


# # Document frequencies

# Document frequency of terms are stored in a dictionary. I've made used of the indextextfiles_BR() function with a little tweak.

# In[109]:


docFrequencies = {}
for word in docFrequencies:
    docFrequencies[word] = len(docFrequencies[word])
                


# We go through whole collection of documents to get document frequency of words, then we put then in a dictionary:

# In[110]:


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

    for word in docFrequencies:
        docFrequencies[word] = len(docFrequencies[word])

    return docFrequencies


# So to process the entire directory and generate the complete docfrequency dictionary we can execute:

# In[111]:


documentFrequencies = document_frequencies('docs')


# To get how many document does the word <code>'ferguson'</code> appears in, we execute:

# In[112]:


print(documentFrequencies['ferguson'])


# # Ranked retrieval - indexing

# ### Vectorise a document

# To present a document as a vector, I've used a dictionary where the value-key pair is term-term_frequency.

# In[113]:


def vectorise_doctf(doc):
    words = tokenize(doc)
    vectorised_doc = {}
    for w in words:
        if w != '':
            if w not in vectorised_doc:
                vectorised_doc[w] = 1.0
            else:
                vectorised_doc[w] += 1.0
    return vectorised_doc


# To present <code>document 101</code> as a vector we can execute:

# In[114]:


doc101 = readfile('docs', 101)
vectorised_doc = vectorise_doctf(doc101)


# Let's now use this datastructure to find out the termfrequency of the word <code>'the'</code>  in this document. We just need to execute:

# In[115]:


print(vectorised_doc['the'])


# ### Normalise a document

# To calculate the magnitude of the vector, we take the sum of the square of each component then take the square root of it:

# In[116]:


coef = math.sqrt(sum(map(lambda x: x * x, vectorised_doc.values())))


# In[117]:


def normalise_vector(vector):
    coef = math.sqrt(sum(map(lambda x: x * x, vector.values())))
    for term in vector:
        vector[term] = vector[term] / coef
    return vector


# To normalise a vector, we pass the vector to the function as an agrument

# In[120]:


normalisedDoc = normalise_vector(vectorised_doc)


# The weight of the word <code>'the'</code> in the normalised document would be:

# In[121]:


print(normalisedDoc['the'])


# ### Index text files

# We go through the directory to normalise all the document then put them in a dictionary

# In[122]:


def indextextfiles_RR(path, docFrequencies):
    N = len(sorted(os.listdir(path)))
    normalised_documents = {}
    for docID in range(N):#
        doc = readfile(path, docID)
        vectorised_doc = vectorise_doctf(doc)
        normalised_documents[docID] = normalise_vector(vectorised_doc)
    return normalised_documents


# So to process the entire directory and generate a dictionary of normalised docuemnts, we execute:

# In[126]:


normalisedDocuments = indextextfiles_RR('docs', documentFrequencies)


# the normalised weight of the word <code>'the'</code> in document ID <code>101</code> is:

# In[127]:


print(normalised_documents[101]["the"])


# # Vectorise the query

# Firstly, we make use of the <code>vectorise_doctf()</code> to vectorise the query. Then we go over the vector to recalculate with the IDF formula

# In[ ]:


def vectorise_query(query, docFrequencies, numberOfDocuments):
    words = tokenize(query)
    vectorQueryIDF = vectorise_doctf(query)
    for term in vectorQueryIDF:
        if term in docFrequencies:
            vectorQueryIDF[term] = vectorQueryIDF[term]*log(numberOfDocuments/docFrequencies[term], 10)
        else:
            vectorQueryIDF[term] = 0.0
    return vectorQueryIDF


# turn the query <code>'England played very well'</code> into a vector:

# In[155]:


vectorisedQuery = vectorise_query('England played very well', documentFrequencies, len(normalisedDocuments))


# the weight of the word <code>'played'</code> in the query is:

# In[142]:


print(vectorisedQuery["played"])


# # QueryRR

# With query <code>'England played very well'</code> and document ID <code>47</code>, we can calculate their <code>cosine similarity</code> by calculate their <code>dot product</code> since our documents are normalised.

# In[154]:


docID = 47
dotProduct = 0
for term in vectorisedQuery:
    if term in normalisedDocuments[docID]:
        dotProduct += vectorised_query[term] * normalisedDocuments[docID][term]
print(dotProduct)


# Go through all the documents they calculate the cosine similarity between each document and the query, then return the top 10 documents

# In[136]:


def query_RR(query, normalisedDocs, documentFrequencies):
    vectorised_query = vectorise_query(query, documentFrequencies, len(normalisedDocs))
    rank = []
    for docID in normalisedDocs:
        dotProduct = 0
        for term in vectorised_query:
            if term in normalisedDocs[docID]:
                dotProduct += vectorised_query[term] * normalisedDocs[docID][term]

        rank.append((dotProduct, docID))
    return [x[1] for x in heapq.nlargest(10, rank)]


# In[ ]:


Example queries:


# In[137]:


print(query_RR('England played very well', normalisedDocuments, documentFrequencies))
print(query_RR('federer australian wimbledon', normalisedDocuments, documentFrequencies))

