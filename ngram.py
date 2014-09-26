# -*- coding: utf-8 -*-
import re
import operator

class Ngrams(object):
    """Stolen from https://github.com/muatik/ngram-example  and little bit modified :) """
        
    ngrams = []
    length = 10

    def __init__(self, arg):
        super(Histogram, self).__init__()
    
    @classmethod
    def insert(cls, text):
        tokens = cls.tokenize(text)
        for i in range(len(tokens) - cls.length):
            cls.ngrams.append(tokens[i:i+cls.length])

    @classmethod
    def tokenize(cls, text):
        return re.split('[ \';:,.?!\n\r"-]+', text.strip().lower())

    @classmethod
    def find(cls, words):
        results = []
        for ngram in cls.ngrams:
            if ngram[:len(words)] == words:
                results.append(ngram)

        return results
    @classmethod
    def find_before(cls, words):
        results = []
        for ngram in cls.ngrams:
            if ngram[len(words):] == words:
                results.append(ngram)
        return results
    
    @classmethod
    def findNext(cls, tokens):
        ngrams = cls.find(tokens)
        possibleWords = {}
        for ngram in ngrams:
            token = "".join(ngram[len(tokens):len(tokens)+1])
            possibleWords[token] = possibleWords.get(token, 0) + 1

        return possibleWords
    @classmethod
    def find_previous(cls, tokens):
        ngrams = cls.find_before(tokens)
        possibleWords = {}
        for ngram in ngrams:
            token = "".join(ngram[len(tokens)-1:len(tokens)])
            possibleWords[token] = possibleWords.get(token, 0) + 1

        return possibleWords

    @classmethod
    def complete(cls, text, removeLast=True):
        tokens = cls.tokenize(text)
        possibleWords = cls.findNext(tokens)
        
        if len(possibleWords) == 0:
            # assuming the last word is not typed completly
            lastToken = tokens[-1]
            possibleWords = cls.findNext(tokens[:-1])
            #print 'last', lastToken
            possibleWords = {token:frequency for token, frequency in possibleWords.iteritems() if lastToken in token}


        return sorted(
                      possibleWords.iteritems(), 
                      key=operator.itemgetter(1),
                      reverse=True)

    @classmethod
    def before(cls, text, removeLast=True):
        tokens = cls.tokenize(text)

        possibleWords = cls.find_previous(tokens)
        
        if len(possibleWords) == 0:
            # assuming the last word is not typed completly
            lastToken = tokens[-1]
            possibleWords = cls.findNext(tokens[:-1])
            #print 'last', lastToken
            possibleWords = {token:frequency for token, frequency in possibleWords.iteritems() if lastToken in token}


        return sorted(
                      possibleWords.iteritems(), 
                      key=operator.itemgetter(1),
                      reverse=True)

