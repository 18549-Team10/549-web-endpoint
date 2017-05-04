#!/usr/bin/python

# given: single sample's peaks from container with unknown amount of liquid, map created from training data
# goal: classify sample with best guess of amount of liquid in container

import math

def bestMatch(freq, mag, mapPeaks):
    # currently, matches only based on frequencies, but can be changed to 
    # match based on magnitude as well
    minDist = None
    bestFreq, bestMag = None, None
    firstIteration = True
    for (mapFreq, mapMag) in mapPeaks:
        if mapFreq == None: continue
        freqDist = abs(mapFreq - freq)
        magDist = abs(mapMag - mag)
        dist = math.sqrt(pow(freqDist, 2) + pow(magDist, 2))
        print("MapFreq = " + str(mapFreq) + "|| MapMag = " + str(mapMag))
        print("Dist = " + str(dist))
        if firstIteration or dist < minDist:
            minDist = dist
            bestFreq, bestMag = mapFreq, mapMag
            firstIteration = False
        print("Best Freq = " + str(bestFreq) + "|| Best Mag = " + str(bestMag))
    return bestFreq, bestMag

def score(samplePeaks, mapPeaks, ratio, debug):
    # currently, only adds to score based on closeness of frequencies, but can
    # be modified to score based on similarity of magnitude as wells
    # TODO: Make this recursive, find the best match and make that pairing. Take them out of 
    # the options array when you've made a match
    peakScores = []
    for (freq,mag) in samplePeaks:
        print("----------------------------------------")
        print("Trying a new frequency and mag from my sample...")
        matchFreq,matchMag = bestMatch(freq,mag, mapPeaks)
        freqDiff = abs(freq - matchFreq)
        magDiff = abs(mag - matchMag)
        magDiff *= ratio
        if debug: print freqDiff, magDiff
        peakScores.append(math.sqrt(magDiff**2 + freqDiff**2))
    peakScores.pop(peakScores.index(max(peakScores)))
    return sum(peakScores) / len(peakScores)

def classify(samplePeaks, trainingDataMap, ratio = 100, debug = False):
    if debug: print samplePeaks
    bestScore = None
    bestMatch = []
    for fillLevel in trainingDataMap.keys():
        currScore = score(samplePeaks, trainingDataMap[fillLevel], ratio, debug)
        if debug: print fillLevel, currScore
        if bestScore == None or currScore < bestScore:
            bestScore = currScore
            bestMatch = [fillLevel]
        elif currScore == bestScore:
            bestMatch.append(fillLevel)
    return bestMatch

# Add in a call to classify that can happen when a page loads
