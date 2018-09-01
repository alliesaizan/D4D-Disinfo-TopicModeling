#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 20:47:24 2018

@author: alliesaizan
"""

import pickle
from nltk.stem import PorterStemmer
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Import files
tweets = pickle.load(open("../data/id_tweets",'rb'))

# Define global variables
tweets_lower = []
tweets_stemmed = []
tweets_dict = dict()
tofile = []

# Text cleaning
def tweet_cleaner(tweets):
    
    global tweets_lower, tweets_stemmed

    # Lower tweets and remove stopwords    
    for tweet in tweets:
        if "http" in tweet:
            tweet = tweet.split("http")[0]
        tweet = " ".join([x for x in tweet.split() if x != "\n" and x not in  set(stopwords.words('english'))])
        tweets_lower.append(tweet.lower())
    
    # Stem Tweets    
    stemmer = PorterStemmer()
    
    for tweet in tweets_lower:
        tweets_stemmed.append([stemmer.stem(x) for x in tweet.split()])
        
    # Tokenize tweets
    #tweets_tokenized = [word_tokenize(tweet) for tweet in tweets_stemmed]
    
    return tweets_lower, tweets_stemmed


# TF-IDF
def run_tfidf(tweets_stemmed):
    
    global tweets_dict, corpus_tfidf
    
    # Generate a dictionary of terms and frequencies
    tweets_dict = corpora.Dictionary(tweets_stemmed)
    
    # Create a bag-of-words corpus
    corpus = [tweets_dict.doc2bow(doc) for doc in tweets_stemmed]
    
    # Run TF-IDF model
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    
    return corpus_tfidf, tweets_dict
  
# Topic modeling
def run_lda(corpus_tfidf, tweets_dict):
    
    # Run the LDA model on 2 of my 4 cores
    lda_model_tfidf = models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=tweets_dict, passes=2, workers=4)
    
    # Print topics and words
    for idx, topic in lda_model_tfidf.print_topics(-1):
        print('Topic: {} Word: {}'.format(idx, topic))
        tofile.append(['Topic: {} Word: {}'.format(idx, topic)])
    pickle.dump(tofile, open("../results/topics2words", "wb"))
    
    
if __name__ == "__main__":
    tweet_cleaner(tweets)
    run_tfidf(tweets_stemmed)
    run_lda(corpus_tfidf, tweets_dict)
    

    
