#!/usr/bin/python

import random
import rawToFill
import os
import visualizer

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def test(trials = 100, ratio = 100, debug = False):
    if debug: print "testing " + str(trials) + " trials.."
    correct = 0
    close   = 0
    count   = 0
    guesses = {}
    oldData = None
    sampleSize = 1000
    fillLevels = [f for (p,f) in sorted([(p,f) for (f,p) in rawToFill.FILL_PERCENTAGES.items()])]
    for trial in range(trials):
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
        guess = rawToFill.rawToFill(data, ratio = ratio, debug = debug)
        if debug: visualizer.visualizeSampleWithFingerprints(data)
        if debug: print "guess: ", guess
        guesses[guess] = guesses.get(guess, 0) + 1
        if guess == fillLevel:
            correct += 1
        if abs(fillLevels.index(guess) - fillLevels.index(fillLevel)) <= 1:
            close += 1
        oldData = data
    print guesses
    return 1.0 * correct / trials, 1.0 * close / trials