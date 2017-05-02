#!/usr/bin/python

import os
import numpy as np
import copy

FINGERPRINT_FILE_PATH = "../fingerprintData/fingerprints.csv"

HIGHPASS_FREQ = 1000 # Hz
NUM_PEAKS = 2
SAMPLING_RATE = 62500 # 62.5 kHz

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
    totalWeight = sum(map(lambda (x,y) : y, l)) * len(l)
    return sum(map(lambda (x,y) : x*y, l)) / totalWeight

def condensePeaks(peaks):

    dists = []
    for i in range(1, len(peaks)):
        dist = abs(peaks[i][0] - peaks[i - 1][0])
        dists.append((dist,i))

    indicesToSplit = sorted([i for (dist,i) in sorted(dists)[len(dists) - NUM_PEAKS + 1:]])

    groups = []
    j  = 0
    for i in indicesToSplit:
        groups.append(peaks[:i-j])
        peaks = peaks[i-j:]
        j = i
    groups.append(peaks)
    # print groups
    output = []
    maxMag = None
    for g in groups:
        avgFreq, avgMag = avg([f for (f,m) in g]), avg([m for (f,m) in g])
        if maxMag == None or avgMag > maxMag: maxMag = avgMag
        output.append((avgFreq, avgMag))

    return sorted(output)

def convertToDict(folderName):
    data = []
    for file in os.listdir(folderName):
        dataString = readFile(folderName + os.sep + file)
        for row in dataString.splitlines():
            if row.isdigit():
                data.append(float(((int(row) >> 2) & 0xFFF)) * 1.4 / 4096)

    n = len(data)
    frq = [1.0 * i * SAMPLING_RATE / (n/2) for i in range(n/2)]
    freqResponse = np.fft.fft(data) # [range(n/2)]
    freqResponseCut = freqResponse[:len(freqResponse)/2]
    freqResponseCut[:int(1.0*HIGHPASS_FREQ/SAMPLING_RATE*(n/2))] = [0 for i in range(int(1.0*HIGHPASS_FREQ/SAMPLING_RATE*(n/2)))] # this is mostly noise
    peaks = [(abs(freqResponseCut[i]), frq[i]) for i in range(len(freqResponseCut))]

    # return [(f,m) for (m,f) in sorted(peaks)[len(peaks) - NUM_PEAKS - 1:]]

    return condensePeaks(sorted([(f,m) for (m,f) in sorted(peaks)[n/2 - 100:]]))

def writeFingerprints(trainingData):
    stringToWrite = "\n".join([key + "," + ",".join([str(freq) + "," + str(mag) for (freq,mag) in val]) for (key,val) in trainingData.items()])
    writeFile(FINGERPRINT_FILE_PATH, stringToWrite)

def readFingerprints():
    rawString = readFile(FINGERPRINT_FILE_PATH)
    fingerprints = dict()
    for line in rawString.splitlines():
        line = line.split(",")
        fingerprints[line[0]] = [(float(line[i]), float(line[i+1])) for i in range(1,len(line),2)]
    return fingerprints

def fingerprint(fillLevelNames):
    trainingData = dict()
    for level in fillLevelNames:
        trainingData[level] = convertToDict("../data/" + level)
        print "done with " + level
    print trainingData
    writeFingerprints(trainingData)