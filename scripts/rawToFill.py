#!/usr/bin/python

import os
import classifySample
import fingerprinter as fp
import numpy as np
import datetime

FRONT_END_JSON_PATH = "../public/json/currentFill.json"
UNKNOWN_DATA_PATH   = "../data/UNKNOWN/"

FILL_PERCENTAGES = {
                    'EMPTY'         : 0,
                    'QUARTER'       : 25,
                    'HALF'          : 50,
                    'THREE_Q'       : 75,
                    'FULL'          : 100
                    }
# requires that each of the keys of FILL_PERCENTAGES exist as files in 
# ../fingerprints

def writeFile(path, text):
    with open(path, "wt") as f:
        f.write(text)

def writeToFrontEnd(label, percentage):
    #print datetime.datetime.now()
    contentsToWrite = '{"containerID" : %d,\n"fillLevel" : %d,\n"currentTime" : "%s"}'%(1,percentage,datetime.datetime.now())
    writeFile(FRONT_END_JSON_PATH, contentsToWrite)

def rawToFillTest(amplitudeDataSets, sampleMagMult = 1, sampleMagAdd = 0, debug = False, ratio = 100):
    if not os.path.exists(fp.FINGERPRINT_FILE_PATH):
        fp.fingerprint(FILL_PERCENTAGES.keys())
    fingerprints = fp.readFingerprints()

    peaks = []
    allData = []
    for data in amplitudeDataSets:
        allData.extend(map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, data))
    fill = classifySample.classify(fp.condenseData(allData), fingerprints, sampleMagMult = sampleMagMult, sampleMagAdd = sampleMagAdd, ratio = ratio, debug = debug)

    writeToFrontEnd(fill, FILL_PERCENTAGES.get(fill[0], None))

    return fill[0]

def rawToFillLive(sampleMagMult = 1, sampleMagAdd = 0, debug = False, ratio = 100):
    if not os.path.exists(fp.FINGERPRINT_FILE_PATH):
        fp.fingerprint(FILL_PERCENTAGES.keys())
    fingerprints = fp.readFingerprints()

    allData = []
    for file in os.listdir(UNKNOWN_DATA_PATH):
        fileData = readFile(UNKNOWN_DATA_PATH + "/" + file)
        allData.extend(map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, data))

    fill = classifySample.classify(fp.condenseData(allData), fingerprints, sampleMagMult = sampleMagMult, sampleMagAdd = sampleMagAdd, ratio = ratio, debug = debug)

    writeToFrontEnd(fill, FILL_PERCENTAGES.get(fill[0], None))