#!/usr/bin/python

import random
import rawToFill
import os
import visualizer

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def test(trials = 100, ratio = 100, magMult = 1, magAdd = 0, debug = False, halfDiff=7500):
    if debug: print "testing " + str(trials) + " trials.."
    largeNumTrialsThreshold = 50
    correct = 0
    close   = 0
    count   = 0
    guesses = {}
    oldData = None
    sampleSize = rawToFill.fp.SAMPLE_SIZE
    fillLevels = [f for (p,f) in sorted([(p,f) for (f,p) in rawToFill.FILL_PERCENTAGES.items()])]
    for trial in range(trials):
        if trials > largeNumTrialsThreshold and trial == trials / 4: print "25%..."
        elif trials > largeNumTrialsThreshold and trial == trials / 2: print "50%..."
        elif trials > largeNumTrialsThreshold and trial == trials * 3 / 4: print "75%..."
        fillLevel = random.choice(fillLevels)
        if debug: print "\nAnswer:", fillLevel
        rawSampleDir = "../data/" + fillLevel
        data = []
        for rawSampleFile in os.listdir(rawSampleDir):
            count += 1
            rawSampleString = readFile(rawSampleDir + os.sep + rawSampleFile).splitlines()
            start = random.randint(0,len(rawSampleString)/sampleSize - 1)
            rawSample = rawSampleString[start*sampleSize:(start + 1)*sampleSize]
            data.append(rawSample)
        if debug: visualizer.visualizeSampleWithFingerprints(data, sampleMagMult = magMult, sampleMagAdd = magAdd)
        guess = rawToFill.rawToFillTest(data, ratio = ratio, sampleMagMult = magMult, sampleMagAdd = magAdd, debug = debug, halfDiff=halfDiff)
        if debug: print "guess: ", guess
        guesses[guess] = guesses.get(guess, 0) + 1
        if guess == fillLevel:
            correct += 1
        if abs(fillLevels.index(guess) - fillLevels.index(fillLevel)) <= 1:
            close += 1
        oldData = data
    print guesses
    return 1.0 * correct / trials, 1.0 * close / trials