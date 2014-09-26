# -*- coding: utf-8 -*-
from ngram import Ngrams
import pymongo
import re
import operator




class Synonyms(Ngrams):
    """docstring for Synonyms"""
    def __init__(self):
        "Data should be in here and append it to ngrams list"
        lim = 1000000
        self.data = pymongo.MongoClient()["conversations_data"]["conversations"]    
        for record in self.data.find().limit(lim):
            if self.find_token_size(record["text"])[0] > 1:
                self.ngrams.append(self.find_token_size(record["text"])[1])             
            else:
                continue


    def find_token_size(self, text):
        text_list = re.split('[ \';:,.?!\n\r"-]+', text.strip().lower())
        return len(text_list), text_list


    def user_questions_average(self):
        s = 0
        n = 0
        for record in self.data.find():
            s += self.find_token_size(record["text"])        
            n = n + 1

        average = s / n
        return average

    def guess_what_i_ll_write(self, string):    
        guess = Ngrams.complete(string)               
        word_list = [ word[0] for word in guess[:3]]
        return word_list
    

    def what_can_i_use(self, string_list):
        print string_list   
        guess_list = []
        for string in string_list:
            guess = Ngrams.before(string)
            guess_list.append(guess[0:2])

        return guess_list
    

sy = Synonyms().guess_what_i_ll_write("hat")
print Synonyms().what_can_i_use(sy)