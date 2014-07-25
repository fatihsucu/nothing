 #!/usr/bin/python
          # -*- coding: utf8 -*-

import pymongo
import re, collections

db_dic = pymongo.MongoClient()["dictionary"]
coll_dic = db_dic["wordlist"]
db = pymongo.MongoClient()["bigdugong_dev"]
coll = db["stream"]


#data = list(coll.find().limit(100))


#contents =  [item["text"] for item in data]

#dictionary = {}


def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#NWORDS = train(words(file('words_tr.txt').read()))

#alphabet = 'abcçdefgğhıijklmnoöpqrsştuüvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word)
    return max(candidates, key=NWORDS.get)



def find_unique_words(content_list):
    word_list = []
    for content in content_list:
        words = content.split()
        for word in words:
            word = word.replace("@","").replace("#","")
            if not word in word_list:
                word_list.append(word)

    return word_list



def found_noun_species(text):
    tamlama_ekleri =  ["in","un","ın","ün"]
    tamlanan_ekleri = ["i","u","ü","ı"]
    
    tokens = text.split()

    n = 0
    while n < len(tokens) - 1:
        if tokens[n].endswith(tuple(unicode(ek.decode('utf8')) for ek in tamlama_ekleri)) and not len(tokens[n]) == 2:
            tamlayan = tokens[n]
            if n == len(tokens):
                break
            if tokens[n+1].endswith(tuple(unicode(ek.decode('utf8')) for ek in tamlanan_ekleri)) and not len(tokens[n+1]) < 3:
                tamlanan = tokens[n+1]
                try:
                    dictionary[tamlayan][tamlanan] += 1
                except:
                    dictionary[tamlayan] = {}
                    dictionary[tamlayan][tamlanan] = 1
                n = n + 2
            n = n + 1
        n = n + 1

def levenshtein(word1, word2):
    distances = {}
    for i in range(-1, (len(word1) + 1)):
        distances[(i, -1)] = i + 1
    for j in range(-1, (len(word2) + 1)):
        distances[(-1, j)] = j + 1

    for i in range(len(word1)):
        for j in range(len(word2)):
            if word1[i] == word2[j]:
                distance_total = 0
            else:
                distance_total = 1
            distances[(i, j)] = min(
                distances[(i - 1, j)] + 1,
                distances[(i, j - 1)] + 1,
                distances[(i - 1, j - 1)] + distance_total
                )
            if i and j and word1[i] == word2[j - 1] and word1[i - 1] == word2[j]:
                distances[(i, j)] = min(distances[(i, j)], distances[i - 2, j - 2] + distance_total)

    return distances[len(word1) - 1, len(word2) - 1]


record = coll_dic.find_one({"letter":"a"})
words = record["words"]
ekler = []
for i in words:    
    for word in words:
        if i in word:
            if word == i:
                continue
            ek_length =  len(word) - len(i)
            print ek_length
            print i
            print word
            
