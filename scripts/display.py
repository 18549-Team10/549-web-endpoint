#!/usr/bin/python

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import fingerprinter as fp

def getDataAndVisualize(dataDir = "../data", graphDir = "../graphs"):
    print("starting up pulling from " + dataDir)
    dataFiles = []
    if os.path.isdir(dataDir):
        dataFiles.extend(os.listdir(dataDir))
    print(dataFiles)
    dataLabels = []
    data = []
    head = []

    #One directory at a time
    for fname in dataFiles:
        if os.path.isfile(dataDir + os.path.sep + fname) and fname.startswith("output"):
            base, ext = os.path.splitext(fname)
            nextHead =[]
            if ext == "" or ext == "txt":
                with open(dataDir + os.path.sep + fname) as myfile:
                    nextHead = myfile.read().splitlines()
            voltageData = map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, nextHead)
            print "fname: " + str(voltageData[:10])

    print("visualizing in " + graphDir)
    if not os.path.isdir(graphDir):
        os.mkdir(graphDir)

    print("done!")

if len(sys.argv) > 1:
    print(sys.argv)
    scriptPath = sys.argv[0]
    extension = sys.argv[1]
    dataDir = os.path.dirname(scriptPath) + os.path.sep + ".." + os.path.sep + "data" + os.path.sep + extension
    graphDir = os.path.dirname(scriptPath) + os.path.sep + ".." + os.path.sep + "graphs" + os.path.sep + extension
    getDataAndVisualize(dataDir, graphDir)
else:
    graphDir = "../graphs"
    scriptDir = "."
#     # getDataAndVisualize()
#     fingerprintVisualize()
