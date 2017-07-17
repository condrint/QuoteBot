# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 15:40:25 2017

@author: T
"""

import requests
import html
import markovify
import tweepy

def main():
     getquotes(100)
     tweet()
     
def tweet():
    #authenticate twitter account
    CONSUMER_KEY = '-'
    CONSUMER_SECRET = '-'
    ACCESS_KEY = '-'
    ACCESS_SECRET = '-'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    with open("C:\\path\\to\\text\\file.txt") as f:
        text = f.read()

    text_model = markovify.Text(text)
    api.update_status(text_model.make_short_sentence(140))
    print('tweeted')

def cleaner(messy): 
    """
    spaghetti method to parse out quote from request
    """
    start, stop, startfound = -1, -1, 0
    
    for i in range(len(messy)-4):    
        if messy[i] + messy[i+1] + messy[i+2] == '<p>' and not startfound:
            start = i + 3
            startfound = 1
            
        if startfound and messy[i] + messy[i+1] + messy[i+2] + messy[i+3] + messy[i+4] == '<\/p>':
            stop = i
            break 
        
    return html.unescape(messy[start:stop])


def getquotes(n):
    """
    retrives quotes and parses out useless text
    n is number of quotes markov chain will sample from
    """
    quotes = []
    for i in range(n):
        r = requests.get('http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1')
        messy = r.text
        
        clean = cleaner(messy)
        quotes.append(clean)
        
        print('quote got')
    
    with open("C:\\path\\to\\text\\file.txt", 'w') as f:
        for quote in quotes:
            f.write(quote + ' ')
    
    
if __name__ == "__main__":
    main()

