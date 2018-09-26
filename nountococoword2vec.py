#!/usr/bin/python

import sys,os,json,requests,time
import gensim
import numpy as np
import inflection

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
cache = {}


def ConvertVectorSetToVecAverageBased(vectorSet, ignore = []):
                if len(ignore) == 0:
                        return np.mean(vectorSet, axis = 0)
                else:
                        return np.dot(np.transpose(vectorSet),ignore)/sum(ignore)


def phrase_similarity(_phrase_1, _phrase_2):
    phrase_1 = _phrase_1.split(" ")
    phrase_2 = _phrase_2.split(" ")
    vw_phrase_1 = []
    vw_phrase_2 = []
    for phrase in phrase_1:
        try:
            # print phrase
            vw_phrase_1.append(model.word_vec(phrase.lower()))
        except:
            # print traceback.print_exc()
            continue
    for phrase in phrase_2:
        try:
            vw_phrase_2.append(model.word_vec(phrase.lower()))
        except:
            continue
    if len(vw_phrase_1) == 0 or len(vw_phrase_2) == 0:
        return 0
    v_phrase_1 = ConvertVectorSetToVecAverageBased(vw_phrase_1)
    v_phrase_2 = ConvertVectorSetToVecAverageBased(vw_phrase_2)
    cosine_similarity = np.dot(v_phrase_1, v_phrase_2) / (np.linalg.norm(v_phrase_1) * np.linalg.norm(v_phrase_2))
    return cosine_similarity

def similarity(phrase1, phrase2):
    score = phrase_similarity(phrase1, phrase2)
    return float(score)

cocolabels = []
f = open('cocolabels.txt')
for line in f.readlines():
    line = line.strip()
    cocolabels.append(line)
f.close()

cache = {}

f = open('cococaptionnouns.txt')

for line in f.readlines():
    line = line.strip()
    d = json.loads(line)
    d['nouns_cocolabels_top3'] = []
    for noun in d['nouns']:
        replies = []
        for cocolabel in cocolabels:
            s = "%s:%s"%(noun,cocolabel)
            if s not in cache:
                singularnoun = inflection.singularize(noun)
                score = similarity(singularnoun,cocolabel)
                cache[s] = score
            else:
                score = cache[s]
            replies.append((cocolabel,score))
        replies.sort(key=lambda tup: tup[1], reverse=True)
        replies = replies[:3]
        t = []
        for reply in replies:
            t.append({'singularnoun': inflection.singularize(noun), 'cocolabel':reply[0], 'cocolabelindex': cocolabels.index(reply[0])+1, 'word2vecscore':reply[1]})
        d['nouns_cocolabels_top3'].append(t)

    print json.dumps(d)
