import sys,os,json
import nltk

f = open(sys.argv[1])

for line in f.readlines():
    line = line.strip()
    #print line
    d = json.loads(line)
    sentence = d['caption']
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(sentence)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    #print nouns
    d['nouns'] = nouns
    print json.dumps(d)
