#!/usr/bin/python

import os
import sys
import classifySample
import fingerprinter as fp
import numpy as np
import datetime
import visualizer

FRONT_END_JSON_PATH   = "../public/json/currentFill.json"
FRONT_END_JSON_TIME_PATH = "../public/json/allPrevFills"
UNKNOWN_DATA_PATH     = "../data/UNKNOWN/"
FROZEN_DATA_FILE_NAME = "frozenVoltages"

FILL_PERCENTAGES = {
                    # 'EMPTY'         : 0,
                    'QUARTER'       : 25,
                    'HALF'          : 50,
                    'THREE_Q'       : 75,
                    'FULL'          : 100
                    }
# requires that each of the keys of FILL_PERCENTAGES exist as files in 
# ../fingerprints

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, text):
    with open(path, "wt") as f:
        f.write(text)

def writeToFrontEnd(label, percentage):
    contentsToWrite = '{"containerID" : %d,\n"fillLevel" : %d,\n"currentTime" : "%s"}'%(1,percentage,datetime.datetime.now())
    writeFile(FRONT_END_JSON_PATH, contentsToWrite)

def writeToFrontEndTime(percentage, time, debug = False):
    prevData = readFile(FRONT_END_JSON_TIME_PATH).splitlines() if os.path.exists(FRONT_END_JSON_TIME_PATH) else []
    if prevData == []: prevData = ["",""] # happens when file does not exist or is empty
    if debug: print "prev data", prevData
    timeValues = [float(x) for x in prevData[0].split(",") if x != ''] + [time.minute + time.second * 1.0/60]
    fillLevels = [int(x) for x in prevData[1].split(",") if x != ''] + [percentage]
    contentsToWrite = ",".join([str(x) for x in timeValues]) + "\n" + ",".join([str(x) for x in fillLevels])
    if debug: print contentsToWrite
    writeFile(FRONT_END_JSON_TIME_PATH, contentsToWrite)
    visualizer.createPrevFillLevelGraph(timeValues, fillLevels)

def clearUnknownDataFiles():
    for filename in os.listdir(UNKNOWN_DATA_PATH):
        if filename == FROZEN_DATA_FILE_NAME: continue
        writeFile(UNKNOWN_DATA_PATH + os.sep + filename, "")

def rawToFillTest(amplitudeDataSets, sampleMagMult = 1, sampleMagAdd = 0, debug = False, ratio = 100, halfDiff=0):
    if not os.path.exists(fp.FINGERPRINT_FILE_PATH):
        fp.fingerprint(FILL_PERCENTAGES.keys())
    fingerprints = fp.readFingerprints()

    peaks = []
    allData = []
    for data in amplitudeDataSets:
        allData.extend(map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, data))
    fill = classifySample.classify(fp.condenseData(allData), fingerprints, sampleMagMult = sampleMagMult, sampleMagAdd = sampleMagAdd, ratio = ratio, debug = debug, halfDiff = halfDiff)

    return fill[0]

def rawToFillLive(sampleMagMult = 1, sampleMagAdd = 0, debug = False, ratio = 100):
    if not os.path.exists(fp.FINGERPRINT_FILE_PATH):
        fp.fingerprint(FILL_PERCENTAGES.keys())
    fingerprints = fp.readFingerprints()

    allData = []
    files = os.listdir(UNKNOWN_DATA_PATH)

    # fresh data?
    if len(files) == 0:
        if debug: print "ERROR: No unknkown data files or previous saved data.  Cannot perform analysis."
        return # no data available for analysis
    elif len(files) == 1 or len(readFile(UNKNOWN_DATA_PATH + os.sep + "output06000")) == 0:
        if debug: print "no fresh data"
        # no fresh data, just read from frozen data
        allData = [float(x) for x in readFile(UNKNOWN_DATA_PATH + os.sep + FROZEN_DATA_FILE_NAME).splitlines()]
    else:
        # fresh data!  need to reclassify
        if debug: print "fresh data"
        for filename in files:
            if filename == FROZEN_DATA_FILE_NAME: continue
            fileData = readFile(UNKNOWN_DATA_PATH + os.sep + filename).splitlines()
            allData.extend(map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, fileData))

    fill = classifySample.classify(fp.condenseData(allData), fingerprints, 
        sampleMagMult = sampleMagMult, sampleMagAdd = sampleMagAdd, 
        ratio = ratio, debug = debug)

    if debug: print "fill", fill
    
    writeToFrontEnd(fill, FILL_PERCENTAGES.get(fill[0], None))
    writeToFrontEndTime(FILL_PERCENTAGES.get(fill[0], None), datetime.datetime.now(), debug)
    # we clear the files so that the cc3200 can keep appending to them, 
    # rather than needing to overwrite them
    clearUnknownDataFiles()

    # we write the values again, so that we can recompute even if we do not have 
    # new data
    writeFile(UNKNOWN_DATA_PATH + os.sep + FROZEN_DATA_FILE_NAME, "\n".join([str(x) for x in allData]))

if len(sys.argv) > 1:
    print(sys.argv)
    debug = bool(sys.argv[0])
else:
    debug = True

rawToFillLive(debug = debug)