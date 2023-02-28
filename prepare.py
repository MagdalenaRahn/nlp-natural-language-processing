#imports
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd




# function to clean a string

def basic_clean(mots):
    
    '''
    this function takes in a string, then 
    prepares it for parsing by lowercasing, 
    normalising and removing special characters
    '''
    
    # lowercasing
    mots = mots.lower()
    
    # removing accents, etc : normalisation
    mots = unicodedata.normalize('NFKD', mots).encode('ascii', 'ignore').decode('utf-8')
    
    # remove special characters (punctuation)
    mots = re.sub(r'[^a-z0-9\s]',' ',mots)

    return mots





# tokeniser function

def tokenise(mots):
    
    '''this function takes in a cleaned
    string and breaks it down into tokens
    for nlp stemming and lemmatising
    '''
    #tokeniser object
    tok = nltk.tokenize.ToktokTokenizer()
    
    # each token
    mots = tok.tokenize(mots)
    
    return mots





# function to stem a string

def stem(mots):
    '''
    this function takes in a string, and 
    stems it using the Porter Stemmer
    '''
    # create the stemmer obj
    ps = nltk.porter.PorterStemmer()

    # stemming each word
    stems = [ps.stem(mot) for mot in mots]

    # joining stems into a clump of text
    stems = [ps.stem(word) for word in mots]
    ' '.join(stems)
    
    return stems