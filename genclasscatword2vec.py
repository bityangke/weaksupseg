import sys,os,json

f = open('cocoword2vectrain.txt')

for line in f.readlines():
    line = line.strip()
    d = json.loads(line)
    fileid = d['image_id']
    filename = "ClassCategories_caption_w2v_debayan/COCO_train2014_"+'0'*(12 - len(str(fileid)))+str(fileid)+'.txt'
    f1 = open(filename,'w')
    s = set()
    for noun in d['nouns_cocolabels_top3']:
        toplabelid = noun[0]['cocolabelindex']
        if noun[0]['word2vecscore'] > 0.3:
            s.add(toplabelid)
    for cocolabelid in s:
        f1.write(str(cocolabelid)+'\n')
    f1.close()
f.close()
