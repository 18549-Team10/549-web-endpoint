#!/usr/bin/python

import random
import rawToFill
import os
import visualizer

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def test(trials = 100, ratio = .23, magMult = 1, magAdd = 0, debug = False, halfDiff=0):
    if debug: print "testing " + str(trials) + " trials.."
    largeNumTrialsThreshold = 50
    correct = dict()
    close   = 0
    count   = 0
    overallCorrect = 0
    guesses = {}
    oldData = None
    sampleSize = rawToFill.fp.SAMPLE_SIZE
    fillLevels = [f for (p,f) in sorted([(p,f) for (f,p) in rawToFill.FILL_PERCENTAGES.items()])]
    for trial in range(trials):
        if trials > largeNumTrialsThreshold and trial == trials / 4: print "25%...", 1.0*overallCorrect/trial, 1.0*close/trial
        elif trials > largeNumTrialsThreshold and trial == trials / 2: print "50%...", 1.0*overallCorrect/trial, 1.0*close/trial
        elif trials > largeNumTrialsThreshold and trial == trials * 3 / 4: print "75%...", 1.0*overallCorrect/trial, 1.0*close/trial
        fillLevel = random.choice(fillLevels)
        if debug: print "\nAnswer:", fillLevel
        rawSampleDir = "../data/" + fillLevel
        fills = dict()
        for playFreq in os.listdir(rawSampleDir):
            count += 1
            rawSampleString = readFile(rawSampleDir + os.sep + playFreq).splitlines()
            start = random.randint(0,len(rawSampleString)/sampleSize - 1) if sampleSize < len(rawSampleString) else 0
            data = rawSampleString[start*sampleSize:(start + 1)*sampleSize]
            rtfGuesses = rawToFill.rawToFillTest(data, playFreq, ratio = ratio, sampleMagMult = magMult, sampleMagAdd = magAdd, debug = debug, halfDiff=halfDiff)
        # guess = rawToFill.rawToFillLive(ratio = ratio, debug = debug)
        # if guess in fillLevels: guess = fillLevels[len(fillLevels) - 1 - fillLevels.index(guess)]
            for guess in rtfGuesses: 
                if debug: print "guess: ", guess
                fills[guess]   = fills.get(guess, 0) + 1
                guesses[guess] = guesses.get(guess, 0) + 1
                if guess == fillLevel:
                    correct[playFreq] = correct.get(playFreq, 0) + 1
                if guess in fillLevels and abs(fillLevels.index(guess) - fillLevels.index(fillLevel)) <= 1:
                    close += 1
        bestFill, bestNumMatches = [], 0
        for fill in fills:
            if fills[fill] > bestNumMatches:
                bestFill, bestNumMatches = [fill], fills[fill]
            elif fills[fill] == bestNumMatches:
                bestFill.append(fill)
        if bestFill == [fillLevel]:
            overallCorrect += 1
    print guesses, correct
    return 1.0*overallCorrect / trials, 1.0 * sum(correct.values()) / count, 1.0 * close / count

def testAndCreateConfusionMatrix(numTrials = 100):
    correct = 0
    sampleSize = rawToFill.fp.SAMPLE_SIZE
    largeNumTrialsThreshold = 50
    fillLevels = [f for (p,f) in sorted([(p,f) for (f,p) in rawToFill.FILL_PERCENTAGES.items()])]
    guesses = {fillLevel : {innerFillLevel : 0 for innerFillLevel in fillLevels} for fillLevel in fillLevels}
    for trial in range(numTrials):
        if numTrials > largeNumTrialsThreshold and trial == numTrials / 4: print "25%..."
        elif numTrials > largeNumTrialsThreshold and trial == numTrials / 2: print "50%..."
        elif numTrials > largeNumTrialsThreshold and trial == numTrials * 3 / 4: print "75%..."
        randomFillLevel = random.choice(fillLevels)
        rawSampleDir = "../data/" + randomFillLevel
        data = []
        for rawSampleFile in os.listdir(rawSampleDir):
            rawSampleString = readFile(rawSampleDir + os.sep + rawSampleFile).splitlines()
            start = random.randint(0,len(rawSampleString)/sampleSize - 1)
            rawSample = rawSampleString[start*sampleSize:(start + 1)*sampleSize]
            data.append(rawSample)
        guess = rawToFill.rawToFillTest(data, ratio = .23)
        guesses[randomFillLevel][guess] = guesses[randomFillLevel].get(guess, 0) + 1
    return guesses

# {'THREE_Q': {'QUARTER': 1, 'THREE_Q': 15, 'EMPTY': 2, 'HALF': 2}, 
# 'FULL': {'FULL': 21}, 
# 'QUARTER': {'QUARTER': 14, 'EMPTY': 2, 'HALF': 4}, 
# 'EMPTY': {'QUARTER': 8, 'EMPTY': 12, 'HALF': 2},  
# 'HALF': {'QUARTER': 10, 'EMPTY': 3, 'HALF': 4}}


# {'THREE_Q': {'THREE_Q': 158, 'FULL': 0, 'QUARTER': 7, 'EMPTY': 16, 'HALF': 14}, 
# 'FULL': {'THREE_Q': 0, 'FULL': 219, 'QUARTER': 0, 'EMPTY': 0, 'HALF': 0}, 
# 'QUARTER': {'THREE_Q': 0, 'FULL': 0, 'QUARTER': 128, 'EMPTY': 33, 'HALF': 43}, 
# 'EMPTY': {'THREE_Q': 0, 'FULL': 0, 'QUARTER': 89, 'EMPTY': 79, 'HALF': 26}, 
# 'HALF': {'THREE_Q': 0, 'FULL': 0, 'QUARTER': 127, 'EMPTY': 20, 'HALF': 41}}