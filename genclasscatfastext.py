import sys,os,json

f = open('cocofastexttrain.txt')

for line in f.readlines():
    line = line.strip()
    d = json.loads(line)
    fileid = d['image_id']
    filename = "ClassCategories_caption_fastext_debayan/COCO_train2014_"+'0'*(12 - len(str(fileid)))+str(fileid)+'.txt'
    f1 = open(filename,'w')
    s = set()
    for noun in d['nouns_cocolabels_top3']:
        toplabelid = noun[0]['cocolabelindex']
        if noun[0]['fastextscore'] > 0.3:
            s.add(toplabelid)
    for cocolabelid in s:
        f1.write(str(cocolabelid)+'\n')
    f1.close()
f.close()
