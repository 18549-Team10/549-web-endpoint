#!/usr/bin/python

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def visualizeFreq(sampleData, dataLabels, graphDir):
    handles = []
    freq_responses = []
    #clear any data off graph
    plt.clf()
    samplingRate = 62500 # 62.5 kHz
    data = []
    for d in sampleData: data.extend(d)
    # for data in sampleData:
    n = len(data)
    frq = [1.0 * i * samplingRate / (n/2) for i in range(n/2)]
    freq_response = (np.fft.fft(data)) #len [range(n/2)]
    freq_response[0] = 0
    freq_response = freq_response[:len(freq_response) / 2]
    handle, = plt.plot(frq, abs(freq_response))
    handles.append(handle)
    
    plt.xlabel('Freq')
    plt.ylabel('|Y(freq)|')
    plt.title('Frequency reponse')
    plt.legend(handles, dataLabels)
    plt.grid(True)
    # plt.show()
    plt.savefig(graphDir + os.path.sep + "freq_response.png")

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
    # plt.show()
    plt.savefig(graphDir + os.path.sep + "time_ordered_data.png")


def getDataAndVisualize(dataDir = "../data/FULL", graphDir = "../graphs"):
    print("starting up pulling from " + dataDir)
    dataFiles = []
    if os.path.isdir(dataDir):
        dataFiles.extend(os.listdir(dataDir))
    print(dataFiles)
    head = []
    dataLabels = []
    for fname in dataFiles:
        dataLabels.append(fname)
        nextHead = []
        if os.path.isfile(dataDir + os.path.sep + fname):
            with open(dataDir + os.path.sep + fname) as myfile:
                nextHead = myfile.read().splitlines()
            head.append(nextHead)
        print len(nextHead), len(head)
    voltageData = map(lambda y : map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, y), head)
    print("visualizing in " + graphDir)
    if not os.path.isdir(graphDir):
        os.mkdir(graphDir)
    visualizeTimeOrderedData(voltageData, dataLabels, graphDir)
    visualizeFreq(voltageData, dataLabels, graphDir)
    print("done!")

if len(sys.argv) > 1:
    print(sys.argv)
    scriptPath = sys.argv[0]
    extension = sys.argv[1]
    dataDir = os.path.dirname(scriptPath) + os.path.sep + "../data" + os.path.sep + extension
    graphDir = os.path.dirname(scriptPath) + os.path.sep + "../graphs" + os.path.sep + extension
    getDataAndVisualize(dataDir, graphDir)
else:
    getDataAndVisualize()
