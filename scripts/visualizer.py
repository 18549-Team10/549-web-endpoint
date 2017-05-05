#!/usr/bin/python

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import fingerprinter as fp

def visualizeFreq(sampleData, dataLabels, graphDir):
    handles = []
    freq_responses = []
    #clear any data off graph
    plt.clf()
    samplingRate = 62500 # 62.5 kHz
    for data in sampleData:
        n = len(data)
        if n > 0:
            print n, type(data), data[0]
            frq = [1.0 * i * samplingRate / (n/2) for i in range(n/2)]
            freq_response = np.fft.fft(data) # len [range(n/2)]
            freq_response = freq_response[:len(freq_response) / 2]
            handle, = plt.plot(frq, abs(freq_response))
            handles.append(handle)

    plt.xlabel('Freq')
    plt.ylabel('|Y(freq)|')
    plt.title('Frequency reponse')
    plt.legend(handles, dataLabels)
    plt.grid(True)
    plt.show()
    # plt.savefig(graphDir + os.path.sep + "freq_response.png")

def visualizeTimeOrderedData(sampleData, dataLabels, graphDir):
    handles = []
    #clear any data off graph
    plt.clf()
    for data in sampleData:
        n = len(data)
        frq = range(n)
        handle, = plt.plot(frq, data)
        handles.append(handle)
    plt.xlabel('Time')
    plt.ylabel('Voltage')
    plt.title('Time ordered piezo data')
    plt.legend(handles, dataLabels)
    plt.grid(True)
    plt.show()
    # plt.savefig(graphDir + os.path.sep + "time_ordered_data.png")


def getDataAndVisualize(dataDir = "../data/", graphDir = "../graphs"):
    print("starting up pulling from " + dataDir)
    dataFiles = []
    if os.path.isdir(dataDir):
        dataFiles.extend(os.listdir(dataDir))
    print(dataFiles)
    dataLabels = []
    data = []
    head = []

    #One directory at a time
    for fname in dataFiles:
        if os.path.isfile(dataDir + os.path.sep + fname):
            base, ext = os.path.splitext(fname)
            nextHead =[]
            if ext == "" or ext == "txt":
                with open(dataDir + os.path.sep + fname) as myfile:
                    nextHead = myfile.read().splitlines()
            head.extend(nextHead)
    voltageData = map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, head)
    data.append(voltageData)

    print("visualizing in " + graphDir)
    if not os.path.isdir(graphDir):
        os.mkdir(graphDir)
    # visualizeTimeOrderedData(data, dataLabels, graphDir)
    visualizeFreq(data, dataLabels, graphDir)
    print("done!")

def fingerprintVisualize():
    plt.clf()
    fingerprints = fp.readFingerprints()
    dataLabels = []
    handles = []
    for fingerprint in fingerprints:
        x = [f for (f,m) in fingerprints[fingerprint]]
        y = [m for (f,m) in fingerprints[fingerprint]]
        handle, = plt.plot(x,y)
        handles.append(handle)
        dataLabels.append(fingerprint)
    plt.xlabel('Freq')
    plt.ylabel('|Y(Freq)|')
    plt.title('Fingerprints')
    plt.legend(handles, dataLabels)
    plt.grid(True)
    plt.show()

def visualizeSampleWithFingerprints(amplitudeDataSets):
    plt.clf()
    fingerprints = fp.readFingerprints()
    allData = []
    for data in amplitudeDataSets:
        allData.extend(map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, data))
    print "visualizer... getting fingerprint for sample"
    sampleFingerprint = fp.condenseData(allData)
    print "visualizer... sample fingerprint", sampleFingerprint
    dataLabels = []
    handles = []
    for fingerprint in fingerprints:
        x = [f for (f,m) in fingerprints[fingerprint]]
        y = [m for (f,m) in fingerprints[fingerprint]]
        handle, = plt.plot(x,y)
        handles.append(handle)
        dataLabels.append(fingerprint)
    x = [f for (f,m) in sampleFingerprint]
    y = [m for (f,m) in sampleFingerprint]
    handle, = plt.plot(x,y)
    handles.append(handle)
    dataLabels.append("sample")
    plt.xlabel('Freq')
    plt.ylabel('|Y(Freq)|')
    plt.title('Fingerprints')
    plt.legend(handles, dataLabels)
    plt.grid(True)
    plt.show()

if len(sys.argv) > 1:
    print(sys.argv)
    scriptPath = sys.argv[0]
    extension = sys.argv[1]
    dataDir = os.path.dirname(scriptPath) + os.path.sep + "../data" + os.path.sep + extension
    graphDir = os.path.dirname(scriptPath) + os.path.sep + "../graphs" + os.path.sep + extension
    getDataAndVisualize(dataDir, graphDir)
# else:
#     # getDataAndVisualize()
#     fingerprintVisualize()
