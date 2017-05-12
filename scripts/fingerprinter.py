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
SAMPLE_SIZE = 6500

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
    allPeaks = []
    for i in range(0,len(data),SAMPLE_SIZE):
        if i + SAMPLE_SIZE > len(data):
            continue # do not include, since not a complete sample
        freqResponse = np.fft.fft(data[i:i + SAMPLE_SIZE]) # [range(n/2)]
        freqResponseCut = freqResponse[:len(freqResponse)/2]
        freqResponseCut[:int(1.0*HIGHPASS_FREQ/SAMPLING_RATE*(SAMPLE_SIZE/2))] = [0 for i in range(int(1.0*HIGHPASS_FREQ/SAMPLING_RATE*(SAMPLE_SIZE/2)))] # this is mostly noise
        peaks = [(abs(freqResponseCut[i]), frq[i]) for i in range(len(freqResponseCut))]
        topPeaks = sorted([(f,m) for (m,f) in sorted(peaks)[len(peaks) - 3:]])
        return topPeaks
        print "topPeaks:", topPeaks
        allPeaks.extend(peaks)
    # allPeaks = sorted([(f,m) for (m,f) in sorted(allPeaks)[len(allPeaks) - 1 - NUM_PEAKS:]])
    # allPeaks.sort()

    # return avg([m for (m,f) in allPeaks])

    allPeaks = sorted([(f,m) for (m,f) in allPeaks])
    lowpassIndex = 0
    while lowpassIndex < len(allPeaks) and allPeaks[lowpassIndex][0] < LOWPASS_FREQ:
        lowpassIndex += 1
    allPeaks = allPeaks[:lowpassIndex]

    # peaks = copy.copy(allPeaks)
    if len(allPeaks) == 0: return []
    allPeaks = sorted([(m,f) for (f,m) in allPeaks])
    cutoffMag = allPeaks[len(allPeaks) - 1][0] *.60
    cutoffI = 0
    while cutoffI < len(allPeaks) and allPeaks[cutoffI][0] < cutoffMag:
        cutoffI += 1
    if cutoffI >= len(allPeaks) - MIN_NUM_PEAKS + 1: cutoffI = len(allPeaks) - MIN_NUM_PEAKS # must have at least min num peaks many peaks 
    allPeaks = sorted([(f,m) for (m,f) in allPeaks[cutoffI:]])
    if debug:
        plt.clf()
        plt.plot([f for (f,m) in allPeaks], [m for (f,m) in allPeaks])
        plt.show()
    # return allPeaks



    dists = []
    for i in range(1, len(allPeaks)):
        dist = abs(allPeaks[i][0] - allPeaks[i - 1][0])
        dists.append((dist,i))

    indicesToSplit = sorted([j for (d,j) in sorted(dists)[len(dists) - MAX_NUM_PEAKS + 1:]])
    if debug: print sorted(dists)#[len(dists) - MAX_NUM_PEAKS + 1:]
    if debug: print indicesToSplit, [(allPeaks[i-1], allPeaks[i]) for i in indicesToSplit]

    groups = []
    j  = 0
    for i in indicesToSplit:
        groups.append(allPeaks[:i-j])
        allPeaks = allPeaks[i-j:]
        j = i
    groups.append(allPeaks)

    # margin = 100 # Hz
    # for allPeaksI in range(len(allPeaks)):
    #     (f,m) = allPeaks[allPeaksI]
    #     currGroup = []
    #     minF, maxF = f - margin, f + margin
    #     peakI = 0
    #     while peakI < len(peaks) and peaks[peakI][0] < minF: peakI += 1
    #     while peakI < len(peaks) and peaks[peakI][0] < maxF:
    #         currGroup.append(peaks[peakI])
    #         peakI += 1
    #     if len(indicesToSplit) > 0 and allPeaksI == indicesToSplit[0]:
    #         groups.append(currGroup) # TODO: fix this
    #         indicesToSplit.pop(0)
    # groups.append(currGroup)

    output = []
    maxMag = None
    for g in groups:
        avgFreq, avgMag = weightedAvg(g), avg([m for (f,m) in g]) # avg([f for (f,m) in g])
        if maxMag == None or avgMag > maxMag: maxMag = avgMag
        output.append((avgFreq, avgMag))

    return sorted(output)

def convertToDict(folderName, debug = False):
    folderDict = dict()
    for file in os.listdir(folderName):
        print "file", file
        data = []
        dataString = readFile(folderName + os.sep + file)
        for row in dataString.splitlines():
            if row.isdigit():
                data.append(float(((int(row) >> 2) & 0xFFF)) * 1.4 / 4096)
        folderDict[file] = condenseData(data, debug)
    return folderDict

def writeFingerprints(trainingData, path):
    stringToWrite = ""
    for fill in trainingData:
        for file in trainingData[fill]:
            stringToWrite += ",".join([fill,file] + [",".join([str(f),str(m)]) for (f,m) in trainingData[fill][file]]) +"\n"
    writeFile(path, stringToWrite.strip())

def readFingerprints(path):
    rawString = readFile(path)
    fingerprints = dict()
    for line in rawString.splitlines():
        line = line.split(",")
        fill = line[0]
        file = line[1]
        if fill not in fingerprints: fingerprints[fill] = dict()
        fingerprints[fill][file] = [(float(line[i]), float(line[i+1])) for i in range(2, len(line), 2)]
    return fingerprints

def fingerprint(fillLevelNames, path, debug = False):
    print "fingerprinting.."
    trainingData = dict()
    for level in fillLevelNames:
        trainingData[level] = convertToDict("../data/" + level, debug)
        print "done with " + level
    print trainingData
    writeFingerprints(trainingData, path)