#!/usr/bin/python

import gensim
import numpy as np
import traceback
from flask import request
from flask import Flask
import json,sys
from elasticsearch import Elasticsearch
from gevent.wsgi import WSGIServer


app = Flask(__name__)

model = gensim.models.KeyedVectors.load_word2vec_format('wiki.en.vec')

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

@app.route('/fastextsimilarity/<phrase1>/<phrase2>', methods=['GET'])
def similarity(phrase1, phrase2):
    print phrase1
    print phrase2
    score = phrase_similarity(phrase1, phrase2)
    print score
    return json.dumps({"result": float(score)})

@app.route('/fastexttopk/<phrase1>/<topk>', methods=['GET'])
def closest(phrase1, topk=1):
    print phrase1
    result = model.most_similar(phrase1, topn=int(topk))
    print result
    return json.dumps(result)

if __name__ == '__main__':
    http_server = WSGIServer(('', 5002), app)
    http_server.serve_forever()
