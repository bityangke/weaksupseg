#!?usr/bin/python

import sys,os,json

f = open(sys.argv[1])

s = f.read()

d = json.loads(s)

for an in d['annotations']:
    print json.dumps(an)
