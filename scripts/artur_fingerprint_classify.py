#!/usr/bin/python

import os
import matplotlib.pyplot as plt
import numpy as np
import copy

HIGHPASS_FREQ = 25000 # Hz
LOWPASS_FREQ  = 50000
MIN_NUM_PEAKS = 2
MAX_NUM_PEAKS = 3
SAMPLING_RATE = 62500 # 62.5 kHz
SAMPLE_SIZE = 8196

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, text):
    with open(path, "wt") as f:
        f.write(text)

def avg(l):
    if (len(l) > 0):
        return (sum(l)/len(l))
    else:
        print "empty list"
        return None

def topX(l, x):
    newL = copy.deepcopy(l)
    output = []
    for i in range(x):
        if len(l) > 0: output.append(newL.pop(newL.index(max(newL))))
    return output

def weightedAvg(l):
    # requires: l is a list of tuples, each of the form (value, weight)
    totalWeight = sum(map(lambda (x,y) : y, l))
    return sum(map(lambda (x,y) : x*y, l)) / totalWeight

def condenseData(data, debug = False):
    n = len(data)
    SAMPLE_SIZE = n
    if debug: print "n", n
    frq = [1.0 * i * SAMPLING_RATE / (SAMPLE_SIZE/2) for i in range(SAMPLE_SIZE/2)]
    freqResponse = np.fft.fft(data[i:i + SAMPLE_SIZE]) # [range(n/2)]
    freqResponseCut = freqResponse[:len(freqResponse)/2]
    freqResponseCut[:int(1.0*HIGHPASS_FREQ/SAMPLING_RATE*(SAMPLE_SIZE/2))] = [0 for i in range(int(1.0*HIGHPASS_FREQ/SAMPLING_RATE*(SAMPLE_SIZE/2)))] # this is mostly noise
    peaks = [(abs(freqResponseCut[i]), frq[i]) for i in range(len(freqResponseCut))]
    topPeaks = sorted([(f,m) for (m,f) in sorted(peaks)[len(peaks) - 4:]])
    return [f for (f,m) in topPeaks] + [m for (f,m) in topPeaks]

def convertToDict(locationDir, trainingData, debug = False):
    for fname in os.listdir(locationDir):
        data = []
        dataString = readFile(locationDir + os.sep + fname)
        print locationDir + os.sep + fname
        for row in dataString.splitlines():
            if row.isdigit():
                data.append(float(((int(row) >> 2) & 0xFFF)) * 1.4 / 4096)
        trainingData.append([locationDir, fname] + condenseData(data, debug))
    return trainingData

def writeFingerprints(trainingData, path):
    stringToWrite = "\n".join([",".join([str(x) for x in dataLine]) for dataLine in trainingData])
    # for fill in trainingData:
    #     for file in trainingData[fill]:
    #         stringToWrite += ",".join([fill,file] + [",".join([str(f),str(m)]) for (f,m) in trainingData[fill][file]]) +"\n"
    writeFile(path, stringToWrite)

def readFingerprints(path):
    rawString = readFile(path)
    fingerprints = []
    for line in rawString.splitlines():
        if len(line) == 0: continue
        fill, file = line[0], line[1]
        data = [float(x) for x in line[2:]]
        fingerprints.append([fill,file] + data)
    return fingerprints

def artur_fingerprint(fillLevelNames, path, debug = False):
    print "fingerprinting.."
    trainingData = []
    for location in os.listdir("../data/"):
        convertToDict("../data/" + location, trainingData, debug)
        print "done with " + location
    print trainingData
    writeFingerprints(trainingData, path)

artur_fingerprint(['UNKNOWN'], "../fingerprintData/unknown.csv")
