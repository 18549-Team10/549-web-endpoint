#!/usr/bin/python

import os
import sys
import numpy as np
import datetime
import visualizer

FRONT_END_JSON_PATH   = "../public/json/currentFill.json"
FRONT_END_JSON_TIME_PATH = "../public/json/allPrevFills"
UNKNOWN_DATA_PATH     = "../data/UNKNOWN/"
FINGERPRINT_FILE_PATH = "../fingerprintData/fingerprints.csv"
FROZEN_DATA_FILE_NAME = "frozenVoltages"

FILL_PERCENTAGES = {
                    'EMPTY'         : 0,
                    'QUARTER'       : 25,
                    'HALF'          : 50,
                    # 'THREE_Q'       : 75,
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
    writeFile(SCRIPT_PATH + os.sep + FRONT_END_JSON_PATH, contentsToWrite)

def writeToFrontEndTime(percentage, time, debug = False):
    prevData = readFile(SCRIPT_PATH + os.sep + FRONT_END_JSON_TIME_PATH).splitlines() if os.path.exists(SCRIPT_PATH + os.sep + FRONT_END_JSON_TIME_PATH) else []
    if prevData == []: prevData = ["",""] # happens when file does not exist or is empty
    if debug: print "prev data", prevData
    timeValues = [float(x) for x in prevData[0].split(",") if x != ''] + [time.minute + time.second * 1.0/60]
    fillLevels = [int(x) for x in prevData[1].split(",") if x != ''] + [percentage]
    contentsToWrite = ",".join([str(x) for x in timeValues]) + "\n" + ",".join([str(x) for x in fillLevels])
    if debug: print contentsToWrite
    writeFile(SCRIPT_PATH + os.sep + FRONT_END_JSON_TIME_PATH, contentsToWrite)
    visualizer.createPrevFillLevelGraph(timeValues, fillLevels, SCRIPT_PATH)

    jsonContentsToWrite = '{ '+str(timeValues) + '\n''}'
    writeFile(SCRIPT_PATH + os.sep + FRONT_END_JSON_TIME_PATH + ".json", jsonContentsToWrite)

def clearUnknownDataFiles(debug):
    if debug: print "clearing files!"
    for filename in os.listdir(SCRIPT_PATH + os.sep + UNKNOWN_DATA_PATH):
        if filename == FROZEN_DATA_FILE_NAME: continue
        writeFile(SCRIPT_PATH + os.sep + UNKNOWN_DATA_PATH + os.sep + filename, "")

def rawToFillTest(amplitudeDataSets, sampleMagMult = 1, sampleMagAdd = 0, debug = False, ratio = 100, halfDiff=0):
    if not os.path.exists():
        fp.fingerprint(FILL_PERCENTAGES.keys())
    fingerprints = fp.readFingerprints()

    peaks = []
    allData = []
    for data in amplitudeDataSets:
        allData.extend(map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, data))
    fill = cs.classify(fp.condenseData(allData), fingerprints, sampleMagMult = sampleMagMult, sampleMagAdd = sampleMagAdd, ratio = ratio, debug = debug, halfDiff = halfDiff)

    return fill[0]

def rawToFillLive(sampleMagMult = 1, sampleMagAdd = 0, debug = False, ratio = .23):
    fingerprintPath = SCRIPT_PATH + os.sep + FINGERPRINT_FILE_PATH
    if not os.path.exists(fingerprintPath):
        fp.fingerprint(FILL_PERCENTAGES.keys(), fingerprintPath)
    fingerprints = fp.readFingerprints(fingerprintPath)

    allData = []
    files = os.listdir(SCRIPT_PATH + os.sep + UNKNOWN_DATA_PATH)

    # fresh data?
    if len(files) == 0:
        if debug: print "ERROR: No unknkown data files or previous saved data.  Cannot perform analysis."
        return # no data available for analysis
    elif len(files) == 1 or len(readFile(SCRIPT_PATH + os.sep + UNKNOWN_DATA_PATH + os.sep + "output06000")) == 0:
        if debug: print "no fresh data"
        # no fresh data, just read from frozen data
        allData = [float(x) for x in readFile(SCRIPT_PATH + os.sep + UNKNOWN_DATA_PATH + os.sep + FROZEN_DATA_FILE_NAME).splitlines()]
    else:
        # fresh data!  need to reclassify
        if debug: print "fresh data"
        for filename in files:
            if filename == FROZEN_DATA_FILE_NAME: continue
            fileData = readFile(SCRIPT_PATH + os.sep + UNKNOWN_DATA_PATH + os.sep + filename).splitlines()
            allData.extend(map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, fileData))

    fill = cs.classify(fp.condenseData(allData), fingerprints,
        sampleMagMult = sampleMagMult, sampleMagAdd = sampleMagAdd,
        ratio = ratio, debug = debug)

    if debug: print "fill", fill

    writeToFrontEnd(fill, FILL_PERCENTAGES.get(fill[0], None))
    writeToFrontEndTime(FILL_PERCENTAGES.get(fill[0], None), datetime.datetime.now(), debug)
    # we clear the files so that the cc3200 can keep appending to them,
    # rather than needing to overwrite them
    clearUnknownDataFiles(debug)

    # we write the values again, so that we can recompute even if we do not have
    # new data
    writeFile(SCRIPT_PATH + os.sep + UNKNOWN_DATA_PATH + os.sep + FROZEN_DATA_FILE_NAME, "\n".join([str(x) for x in allData]))

if len(sys.argv) == 3:
    print(sys.argv)
    SCRIPT_PATH = os.path.dirname(sys.argv[0])
    DO_KEG = bool(int(sys.argv[1]))
    debug = bool(int(sys.argv[2]))
else:
    print "correct usage: script_path do_keg debug"
    SCRIPT_PATH = "."
    DO_KEG = True
    debug = True

if DO_KEG:
    print "keg!", sys.argv[1]
    import classifySample as cs
    import fingerprinter as fp
else:
    print "waterbottle.", sys.argv[1]
    import wb_classifySample as cs
    import wb_fingerprinter as fp

rawToFillLive(debug = debug)
