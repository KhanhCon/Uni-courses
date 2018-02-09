import re
import os

def readfile(path, docid):
    files = sorted(os.listdir(path))
    f = open(os.path.join(path, files[docid]), 'r', encoding='latin-1')
    s = f.read()
    f.close()
    return s

def tokenize(text):
    DELIM = '[ \n\t0123456789;:.,/\(\)\"\'-]+'
    return re.split(DELIM, text.lower())

def indextextfiles_BR(path):
    N = len(sorted(os.listdir(path)))
    postings={}
    for docID in range(N):
        s = readfile(path, docID)
        words = tokenize(s)
        for w in words:
            if w!='':
                if w not in postings:
                    postings[w] = {docID}
                else:
                    postings[w].add(docID)
    return postings

def query_BR(postings, qtext):
    words = tokenize(qtext)
    res = None
    for w in words:
        try:
            res = postings[w] if res==None else res & postings[w]
        except KeyError:
            return {}
    return res

def query_BR(postings, qtext):
    words = tokenize(qtext)
    allpostings = [postings[w] for w in words]
    res = set.intersection(*allpostings)
    return res

postings = indextextfiles_BR('docs')
print(query_BR(postings,'england football defeat vietnam'))
