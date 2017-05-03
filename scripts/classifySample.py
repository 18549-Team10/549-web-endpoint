#!/usr/bin/python

# given: single sample's peaks from container with unknown amount of liquid, map created from training data
# goal: classify sample with best guess of amount of liquid in container

def bestMatch(freq, mag, mapPeaks, prevPeaksMatched):
    # currently, matches only based on frequencies, but can be changed to 
    # match based on magnitude as well
    minDist = None
    bestFreq, bestMag = None, None
    secondBestFreq, secondBestMag = None, None
    print("Map Peaks = " + str(mapPeaks))
    for (mapFreq, mapMag) in mapPeaks:
        if mapFreq == None: continue
        dist = abs(mapFreq - freq)
        if (minDist == None or dist < minDist) and dist not in prevPeaksMatched:
            minDist = dist
            if (bestFreq != None and bestMag != None):
                secondBestFreq = bestFreq
                secondBestMag = bestMag
            bestFreq, bestMag = mapFreq, mapMag
            prevPeaksMatched.append(bestFreq)
    if dist in prevPeaksMatched:
        bestFreq, bestMag = secondBestFreq, secondBestMag
    print("Best Freq = " + str(bestFreq))
    print("Best Mag = " + str(bestMag))
    return bestFreq, bestMag

def score(samplePeaks, mapPeaks, ratio, debug):
    # currently, only adds to score based on closeness of frequencies, but can
    # be modified to score based on similarity of magnitude as wells
    peakScores = []
    prevPeaksMatched = []
    for (freq,mag) in samplePeaks:
        matchFreq,matchMag = bestMatch(freq,mag, mapPeaks, prevPeaksMatched)
        freqDiff = abs(freq - matchFreq)
        magDiff = abs(mag - matchMag)
        if debug: print freqDiff, magDiff
        peakScores.append(magDiff)
    peakScores.pop(peakScores.index(max(peakScores))) # .28, .48 with this line, .23, .48 without
    return sum(peakScores) / len(samplePeaks)

def classify(samplePeaks, trainingDataMap, ratio = 1.0, debug = False):
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
