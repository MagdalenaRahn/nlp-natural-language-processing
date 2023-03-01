# imports
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
    mots = re.sub(r"[^a-z0-9'\s/\n]",' ',mots)

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




# lemmatising function

def lemmatize(mots):
    
    '''this function takes in a string
    and lemmatises it'''
    
    # lemmatiser obj
    wln = nltk.stem.WordNetLemmatizer()
    
    # join the lemmatised words

    lemmas = [wln.lemmatize(mot) for mot in mots]
    ' '.join(lemmas)
    
    return lemmas




## function to remove stopwords

# appending to stopword list ; leave empty blank if none
extra_words = []
# list of words to keep in stopwords list ; leave list empty if none
keep_words = []

def remove_stopwords(mots, extra_words, keep_words):
    
    '''
    this function takes in a string of lemmatised 
    or stemmed words after normalisation and
    returns the string with stopwords removed
    '''
    
    # establish stopwords
    arret = stopwords.words('english')
    
    # appending via extending the extra_words list
    arret.extend(extra_words)

    # indicating words to keep in the original text
    exclude_words = set(stopwords.words('english')) - set(keep_words)
    
    # all the words w/o stopwords, joined as phrase
    mots_w_stopwords_removed = [mot for mot in mots if mot not in exclude_words]
    ' '.join(mots_w_stopwords_removed)
    
    return mots_w_stopwords_removed





# function to clean, tokenise, stem, lem and remove stopwords

# appending to stopword list ; leave empty blank if none
extra_words = []

# list of words to keep in stopwords list ; leave list empty if none
keep_words = []

def clean_stem_lem_stop(df, extra_words, keep_words):
    
    '''
    this function takes in the Codeup blog df
    and cleans, tokenises, stems and lemmatises
    the dataframe, creating a new column for 
    each action to the dataframe
    '''
    
    # renaming & dropping 'content' column
    df['original'] = df['content'] 
    df.drop(columns = 'content', inplace = True)

    # cleaning function
    df['cleaned'] = df['original'].apply(basic_clean)

    # tokenising function
    df['cleaned'] = df['cleaned'].apply(tokenise)

    # Stemming function
    df['stemmed'] = df['cleaned'].apply(stem)

    # lemmatising function
    df['lemmatised'] = df['cleaned'].apply(lemmatize)
    
    # removing stopwords from stemmed column
    df['sans_stopwords'] = df['stemmed'].apply(remove_stopwords, extra_words, keep_words)
    
    return df
