#!/usr/bin/python

import sys
import os

print  sys.argv[1:]

dataDir = sys.argv[1]
dataFiles = []
if os.path.isdir(dataDir):
    dataFiles.extend(os.listdir(dataDir))

print dataFiles

lines = 1
head = []
for fname in dataFiles:
    with open(dataDir + os.path.sep + fname) as myfile:
        head.extend([next(myfile).strip() for x in xrange(lines)])

print head
print map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096 , head)
