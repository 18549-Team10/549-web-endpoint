import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def visualizeFreq(sampleData, dataLabels):
    handles = []
    freq_responses = []
    for data in sampleData:
        n = len(data)
        frq = range(n)
        freq_response = (np.fft.fft(data)/n)#[range(n/2)]
        handle, = plt.plot(frq, abs(freq_response))
        handles.append(handle)
    plt.xlabel('Freq')
    plt.ylabel('|Y(freq)|')
    plt.title('Frequency reponse')
    plt.legend(handles, dataLabels)
    plt.grid(True)
    plt.show()

def visualizeTimeOrderedData(sampleData, dataLabels):
    handles = []
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


def getDataAndVisualize(dataDir = "../data"):
    print("starting up...")
    dataFiles = []
    if os.path.isdir(dataDir):
        dataFiles.extend(os.listdir(dataDir))
    head = []
    dataLabels = []
    for fname in dataFiles:
        dataLabels.append(fname)
        with open(dataDir + os.path.sep + fname) as myfile:
            nextHead = myfile.read().splitlines()
        head.append(nextHead)
        print len(nextHead), len(head)
    voltageData = map(lambda y : map(lambda x : float(((int(x) >> 2) & 0xFFF)) * 1.4 / 4096, y), head)
    print("visualizing..")
    visualizeTimeOrderedData(voltageData, dataLabels)
    visualizeFreq(voltageData, dataLabels)
    print("done!")

getDataAndVisualize()