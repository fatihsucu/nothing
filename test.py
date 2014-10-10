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
[["R"],["F"],["B"]]
]


def find_pgs(word, phrase_group):
    for phrase in phrase_group:
        if not word in phrase:
            continue
        else:
            return True
    return False

def pull_other_words(wordlist, word):
    try:
        wordlist.remove(word)
        return wordlist
    except:
        return None

def get_phrase_group_id(word):
    pg_ids = []
    n = 0
    for phraseGroups in data:        
        for phrase in phraseGroups:
            if find_pgs(word, phrase):
                pg_ids.append(n)
        n = n + 1
    return pg_ids

def find_indexes(word1, word2):
    word1_pgs = get_phrase_group_id(word1)
    word2_pgs = get_phrase_group_id(word2)
    return set(word1_pgs + word2_pgs)


def find_relative_words(word1, word2):
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
    ratio = 0
    for i in question_list:
        if not isinstance(i, list):
            i = list(i) 
        if i in [ phrase for phrase in data_list ]:
            phrase_weight = 1/len(data_list)
            ratio += phrase_weight
    return ratio

def check_all_words(sentece, data):
    for word in sentence:
        if not find_pgs(word, data):
            return False
    return True



def tag_for_me(sentence):        
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

    sum_of_words = []
    for com in itertools.combinations(sentence, 2):
        sum_of_words += [ list(each) for each in list(find_relative_words(com[0],com[1]))]
    
    tags = []
    
    if not word_freqs:
        tags = sentence
        return tags
    
    for w in sum_of_words:
        tg = []
        for i in w:
            try:
                weight = word_freqs[i] / n
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

    