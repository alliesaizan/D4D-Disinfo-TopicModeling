#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 20:13:23 2018

@author: alliesaizan
"""

# Import packages
import os
import time
import tweepy as tp
from tweepy import OAuthHandler
import pandas as pd
import pickle

############################
# WORKSPACE SET-UP

# Import data
currentdir = os.getcwd()
#os.chdir("/Users/alliesaizan/Documents/Python-Tinkering/Disinfo-tweets-LDA")

ids = pd.read_csv("../data/UnitetheRight_tweet_IDs.tsv", sep = "/t", dtype = str, header = None)[0].tolist()


############################
# TWITTER PULL

# Set the parameters for the API account
consumer_key = "Qy9anUGZgFWBGC3Bm26VvqWpd"
consumer_secret = "wdhPWbRBTx8JANWsbYApClf10PCYHB7JwaWvWVzluOWAoBMWYZ"
access_token = "876066893844631552-5zloAgKe17l1K8AD7xJ4JO7VtdtaxN2"
access_secret = "FZIqfdGqBdGYQQjhTgSAbrhiE72anfUBmgt2njvQ47lBo"

# Verify and initialize the API account
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tp.API(auth, wait_on_rate_limit = True)

#new_tweets = api.get_status(id =  ids[4], tweet_mode='extended')
#new_tweets = api.statuses_lookup(id_ = ids[0:100], include_entities=False, tweet_mode='extended')
#new_tweets[0]._json.get('retweeted_status')['full_text']


# New version
final_tweets = []

def retrieve_ids(ids):
    
    global final_tweets  
    counter = 0
    for i in range(0, len(ids), 100):
        start = i
        stop  = i + 100
        try:
            tweets = api.statuses_lookup(id_ = ids[start:stop], include_entities=False, tweet_mode='extended')
            counter +=1
            for j in range(0, len(tweets)):                
                try:
                    final_tweets.append(tweets[j]._json.get("retweeted_status")['full_text'])
                except:
                    final_tweets.append(tweets[j].full_text)   
            print("Pull #" + counter)
        except tp.TweepError:
            print("I completed pull #" + str(i))
            time.sleep(60 * 15)
            continue

retrieve_ids(ids)

pickle.dump(final_tweets, open("../data/id_tweets.pkl", "wb"))



#tweets = []
#i = 0
#for item in ids:
#    try:
#        test_tweet = api.get_status(id =  item, tweet_mode='extended')
#        if "RT" in test_tweet.full_text:
#            tweets.append(test_tweet._json.get("retweeted_status")['full_text'])
#        else:
#            tweets.append(test_tweet.full_text)
#    except tp.TweepError:
#        i +=1
#        print("I completed pull #" + str(i))
#        time.sleep(60 * 15)
#        continue




