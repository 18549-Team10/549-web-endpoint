#!/usr/bin/python

# given: single sample's peaks from container with unknown amount of liquid, map created from training data
# goal: classify sample with best guess of amount of liquid in container

import math

def bestMatch(freq, mag, peaks, debug = False):
    # currently, matches only based on frequencies, but can be changed to 
    # match based on magnitude as well
    minDist = None
    bestFreq, bestMag = None, None
    secondBestFreq, secondBestMag = None, None
    firstIteration = True
    for (mapFreq, mapMag) in peaks:
        if mapFreq == None: continue
        freqDist = abs(mapFreq - freq)
        magDist = abs(mapMag - mag)
        dist = math.sqrt(pow(freqDist, 2) + pow(magDist, 2))
        if firstIteration or dist < minDist:
            minDist = dist
            bestFreq, bestMag = mapFreq, mapMag
            firstIteration = False
    return bestFreq, bestMag

# def score(samplePeaks, mapPeaks, ratio, debug = False):
#     # currently, only adds to score based on closeness of frequencies, but can
#     # be modified to score based on similarity of magnitude as wells
#     # TODO: Make this recursive, find the best match and make that pairing. Take them out of 
#     # the options array when you've made a match
#     peakScores = []
#     for (freq,mag) in samplePeaks:
#         matchFreq,matchMag = bestMatch(freq,mag, mapPeaks, debug)
#         freqDiff = abs(freq - matchFreq)
#         magDiff = abs(mag - matchMag)
#         magDiff *= ratio
#         if debug: print freqDiff, magDiff
#         peakScores.append(math.sqrt(magDiff**2 + freqDiff**2))
#     peakScores.pop(peakScores.index(max(peakScores)))
#     return sum(peakScores) / len(peakScores)

def bestMatchJustFreq(freq, mag, peaks, debug = False):
    minDist = None
    bestFreq, bestMag = None, None
    for (pFreq, pMag) in peaks:
        freqDist = abs(pFreq - freq)
        magDist = abs(pFreq - mag)
        dist = freqDist # can be changed to find distance based on other things
        if minDist == None or dist < minDist:
            minDist = dist
            bestFreq, bestMag = pFreq, pMag
    return bestFreq, bestMag

def score(samplePeaks, mapPeaks, ratio = 1, debug = False):
    # todo: revert to matching peaks and scoring on each peak
    # if debug: print sampleMag, mapMag
    # return abs(sampleMag*ratio - mapMag)
    peakScores = []
    for (freq,mag) in samplePeaks:
        matchFreq,matchMag = bestMatch(freq,mag, mapPeaks, debug)
        freqDiff = abs(freq - matchFreq)
        magDiff = abs(ratio*mag - matchMag)
        if debug: print freqDiff, magDiff
        peakScores.append(magDiff)
    # peakScores.pop(peakScores.index(max(peakScores)))
    if len(peakScores) == 0: 
        print "no peak Scores!"
        return 0
    return sum(peakScores) / len(peakScores)

def classify(sampleMag, trainingDataMap, sampleMagMult = 1, sampleMagAdd = 0, ratio = .23, debug = False, halfDiff = 7500):
    # samplePeaks = map(lambda (f,m) : (f,m*sampleMagMult + sampleMagAdd), samplePeaks)
    if debug: print "sample mag", sampleMag
    bestScore = None
    bestMatch = []
    # if abs(samplePeaks[1][0] - samplePeaks[0][0]) < halfDiff:
    #     return ["HALF"]
    for fillLevel in trainingDataMap.keys():
        # if fillLevel == "HALF": continue
        currScore = score(sampleMag, trainingDataMap[fillLevel], ratio, debug)
        if debug: print fillLevel, currScore
        if bestScore == None or currScore < bestScore:
            bestScore = currScore
            bestMatch = [fillLevel]
        elif currScore == bestScore:
            bestMatch.append(fillLevel)
    return bestMatch

# Add in a call to classify that can happen when a page loads
