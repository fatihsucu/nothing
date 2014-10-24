#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import itertools

data = [
[["A","B","C"],["F"]],
[["R"],["A","B"],["F"]],
[["M"],["A","C"],["R"]],
[["M"],["A","B"],["K"]],
[["R"],["A","B","C"],["M"],["K"]],
[["M"],["A"],["R"],["K"]],
[["K"],["R","L"], ["P"]],
[["M"],["B"],["O"]],
[["R"],["F"],["B"]],
[["K","P"],["F","O"]],
[["A"],["D"]],
[["B","Q"],["T"]],
[["A","C"],["D"],["O"]],
[["Q","W"],["Y"],["U","I"]],
[["Y","R"],["H"]],
[["H","J","A"],["R","K"],["L"]]
]

def find_overall_syns(word):
    """
    Eğer aynı phrase'de geçmeyen çiftler varsa her biri için tek tek kontrol yapar. Ve çogunlugunda 
    geçerli olan eş anlamlıları kabul eder.
    """
    phrase_list = []
    n = 0
    for pg in data:
        for phrase in pg:
            if word in phrase:
                n = n + 1
                phrase_list.append(phrase)
            else:
                continue
    syns_freq = {}
    for phrase in phrase_list:
        for a in phrase:
            try:
                syns_freq[a] += 1
            except:
                syns_freq[a] = 1

    print syns_freq
    syns = []
    for key in syns_freq.keys():
        value = syns_freq[key] 
        if value/n > 0.5:
            syns.append(key)

    if not syns:
        syns.append(word)
    return syns



def find_pgs(word, phrase_group):
    """
    Phrase grubunun icerisinde aranan kelimenin olup olmadigi kontrolunu yapar
    """
    for phrase in phrase_group:
        if not word in phrase:
            continue
        else:
            return True
    return False

def pull_other_words(wordlist, word):
    """
    Verilen kelimenin grup icinden cıkartılarak mukerrer olmasini engeller.
    """
    try:
        wordlist.remove(word)
        return wordlist
    except:
        return None

def get_phrase_group_id(word):
    """
    Phrase gruplara ait data icinde nerede bulunduklarini kontol eder ve cıktı olarak bu id leri verir.
    """
    pg_ids = []
    n = 0
    for phraseGroups in data:        
        for phrase in phraseGroups:
            if find_pgs(word, phrase):
                pg_ids.append(n)
        n = n + 1
    return pg_ids

def find_indexes(word1, word2):
    """
    Verilmis olan kelimelerin data icerisindeki konumlarini dondurur.
    """

    word1_pgs = get_phrase_group_id(word1)
    word2_pgs = get_phrase_group_id(word2)
    return set(word1_pgs + word2_pgs)

def find_relative_words(word1, word2):
    """
    Verilmis kelimelerin data icerisinde bulunan iliskili kullanımlarını gruplar ve cıktı olarak verir.
    """
    word1_syns = []
    word2_syns = []
    indexes = find_indexes(word1, word2)
    
    for i in indexes:
        phrase_group = data[i]
        for phrase in phrase_group:
            if word1 in phrase and list(word2) in [p for p in phrase_group]:
                word1_syns += phrase            
            if word2 in phrase and list(word1) in [p for p in phrase_group]:
                word2_syns += phrase
    
    if not word1_syns or not word2_syns:
        for i in indexes:
            phrase_group = data[i]
            for phrase in phrase_group:
                if not word1_syns:
                    if word1 in phrase:
                        word1_syns += phrase            
                if not word2_syns:
                    if word2 in phrase:
                        word2_syns += phrase
    return set(word1_syns), set(word2_syns)

def find_query_styles(phrase_group_list):
    """
    Verilen phrase grouplar icin farklı sorus sekillerini cıkarır.
    """
    qs = []
    main_tags = phrase_group_list    
    for phrase in phrase_group_list:        
        if len(phrase) > 1:
           for word in phrase:
                new = []                
                for i in main_tags:
                    if i == phrase:
                        new.append([word])
                    else:
                        new.append(i)
                qs.append(new)
    if not qs:
        qs = phrase_group_list                
    return qs

def check_similarity_ratio(question_list, data_list):
    """
    Datadaki sorular ile verilmis sorunun benzerliklerini kontrol eder.
    """
    ratio = 0
    for i in question_list:
        if not isinstance(i, list):
            i = list(i) 
        if i in [ phrase for phrase in data_list ]:
            phrase_weight = 1/len(data_list)
            ratio += phrase_weight
    return ratio

def check_all_words(sentece, data):
    """
    Cümle içerisindeki kelimelerin data icerisinde bulunup bulunmadıklarını kontrol eder
    Eger biri bile bulunmuyorsa False dondurur.
    """
    for word in sentence:
        if not find_pgs(word, data):
            return False
    return True

def tag_for_me(sentence):
    """
    Yukarıdaki fonksiyonlara gore es anlamlılarını ayıklar ve bu kalıba en uygun phrase groubunu olusturur.
    Eger data icerisinde bu cumleye uygun kombinasyon bulunmuyorsa bunu default olarak alır ve ilk kayıdı gerçekleştir.
    Etiketler oldugu gibi kaydedilir.
    """
    word_freqs = {}
    n =  0
    for d in data:        
        if not check_all_words(sentence, d):            
            continue            
        n = n + 1
        for phrase in d:
            for elem in phrase:
                try:
                    word_freqs[elem] += 1
                except:
                    word_freqs[elem] = 1

    combines = []
    print "{} is the sentence".format(sentence)
    print "{} are combinations which looking for relative words".format([each for each in itertools.combinations(sentence, 2)])
    
    for com in itertools.combinations(sentence, 2):
        combines += [ list(each) for each in list(find_relative_words(com[0],com[1]))]
    
    tags= []
    print "There is words usage dict {}".format(word_freqs)
    print "Detected in {} phrase groups".format(n)
    print "This sentences combines are {}".format(combines)

    if not word_freqs:
        tags = []
        for i in [word for word in sentence]:
            tags.append(find_overall_syns(i))
        return tags
    
    for w in combines:
        tg= []
        for i in w:
            try:
                weight = word_freqs[i]/n
            except:
                continue
            if weight > 0.5:
                tg.append(i)
       
        if tg in tags:
            continue

        tags.append(tg)
    return tags
    
sentence = ["C","F"]
print tag_for_me(sentence)

