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
    for trial in range(trials):
        fillLevel = random.choice(rawToFill.FILL_PERCENTAGES.keys())
        rawSampleDir = "../data/" + fillLevel
        # print rawSampleDir
        data = []
        for rawSampleFile in os.listdir(rawSampleDir):
            count += 1
            sampleSize = 256
            rawSampleString = readFile(rawSampleDir + os.sep + rawSampleFile).splitlines()
            start = random.randint(0,len(rawSampleString)/sampleSize - 1)
            rawSample = rawSampleString[start:start + sampleSize]
            sample = map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, rawSample)
            data.append(sample)
        guess = rawToFill.rawToFill(data)
        guesses[guess] = guesses.get(guess, 0) + 1
        if guess == rawToFill.FILL_PERCENTAGES[fillLevel]:
            correct += 1
    print guesses
    return 1.0 * correct / trials