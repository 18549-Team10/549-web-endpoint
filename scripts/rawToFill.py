#!/usr/bin/python

import os
import classifySample
import fingerprinter as fp
import numpy as np

FILL_PERCENTAGES = {'EMPTY'         : 0,
                    'QUARTER'       : 25,
                    'HALF'          : 50,
                    'THREE_Q'       : 75,
                    'FULL'          : 100}
# requires that each of the keys of FILL_PERCENTAGES exist as files in 
# ../fingerprints

def writeFile(path, text):
    with open(path, "wt") as f:
        f.write(text)

def writeToFrontEnd(label, percentage):
    contentsToWrite = '{"containerID" : %d,\nfillLevel : %d"}'%(1,percentage)
    writeFile("../public/json/currentFill.json",contentsToWrite)

def rawToFill(amplitudeDataSets):
    if not os.path.exists(fp.FINGERPRINT_FILE_PATH):
        fp.fingerprint(FILL_PERCENTAGES.keys())
    fingerprints = fp.readFingerprints()

    peaks = []
    allData = []
    for data in amplitudeDataSets:
        allData.extend(map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, data))
        # TODO: edit this
    n = len(allData)
    frq = [1.0 * i * fp.SAMPLING_RATE / (n/2) for i in range(n/2)]
    freqResponse = np.fft.fft(allData) # [range(n/2)]
    freqResponseCut = freqResponse[:len(freqResponse)/2]
    # freqResponseCut[:int(1.0*fp.HIGHPASS_FREQ/fp.SAMPLING_RATE*(n/2))] = [0 for i in range(int(1.0*fp.HIGHPASS_FREQ/fp.SAMPLING_RATE*(n/2)))] # this is mostly noise
    peaks = [(abs(freqResponseCut[i]), frq[i]) for i in range(len(freqResponseCut))]
    condensedPeaks = fp.condensePeaks(sorted([(f,m) for (m,f) in sorted(peaks)[n/2 - 100:]]))
    fill = classifySample.classify(condensedPeaks, fingerprints)

    writeToFrontEnd(fill, FILL_PERCENTAGES.get(fill[0], None))

    return fill[0]