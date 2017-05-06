#!/usr/bin/python

import test

def frange(start, stop, step):
    out = []
    i = start
    while i < stop: 
        out.append(i)
        i += step
    return out

def testRatios(numTrials = 100):
    tested = set()
    bestRatio, bestScore, allRatios = None, None, []
    # for ratio in frange(.001,2,.001):
    #     score = test.test(numTrials,ratio)
    #     allRatios.append(score)
    #     if bestScore == None or score > bestScore:
    #         bestRatio, bestScore = ratio, score
    for ratio in range(70,120):
        score = test.test(numTrials,ratio = ratio)
        allRatios.append(score)
        if bestScore == None or score > bestScore:
            bestRatio, bestScore = ratio, score
    return bestRatio, bestScore, allRatios

def testSamplePeakModifications(numTrials = 100):
    bestModifications, bestScore, allResults = None, None, []
    for add in frange(0, 30, .5):
        for mult in frange(1, 30, .2):
            score = test.test(numTrials, ratio = 1, magMult = mult, magAdd = add)
            if bestScore == None or score > bestScore:
                bestModifications, bestScore = (add, mult), score
            allResults.append(((add, mult), score))
    return bestModifications, bestScore, allResults

def testCutoffs(numTrials = 100):
    tested = set()
    bestCutoff, bestScore, allCutoffs = None, None, []
    for cutoff in range(7000,8000,10):
        score = test.test(numTrials,halfDiff=cutoff)
        allCutoffs.append(score)
        if bestScore == None or score > bestScore:
            bestCutoff, bestScore = cutoff, score
    return bestCutoff, bestScore, allCutoffs

# keg data
# peaks  ratio  success  close
#    10    .01     .284   .539
#     4    .01     .201   .486
