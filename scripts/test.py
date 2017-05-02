#!/usr/bin/python

import random
import rawToFill
import os

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def test(trials = 100):
    correct = 0
    count   = 0
    guesses = {}
    oldData = None
    sampleSize = 10000
    for trial in range(trials):
        fillLevel = random.choice(rawToFill.FILL_PERCENTAGES.keys())
        print "\nAnswer:", fillLevel
        rawSampleDir = "../data/" + fillLevel
        data = []
        for rawSampleFile in os.listdir(rawSampleDir):
            count += 1
            rawSampleString = readFile(rawSampleDir + os.sep + rawSampleFile).splitlines()
            start = random.randint(0,len(rawSampleString)/sampleSize - 1)
            rawSample = rawSampleString[start*sampleSize:(start + 1)*sampleSize]
            data.append(rawSample)
        guess = rawToFill.rawToFill(data)
        print "guess: ", guess
        guesses[guess] = guesses.get(guess, 0) + 1
        if guess == fillLevel:
            correct += 1
        oldData = data
    print guesses
    return 1.0 * correct / trials