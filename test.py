data = [

[["A","B","C"],["F"]],
[["R"],["A","B"],["F"]],
[["M"],["A","C"],["R"]],
[["M"],["A","B"],["K"]],
[["R"],["A","B","C"],["M"],["K"]],
[["M"],["A"],["R"],["K"]],
[["K"],["R","L"]]
]


def find_pgs(word, phrase):    
    if not word in phrase:
        return False
    else:
        return True

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


print find_relative_words("M","F")







