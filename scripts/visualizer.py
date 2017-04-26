#!/usr/bin/python

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def visualizeFreq(sampleData, dataLabels, graphDir):
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
    plt.savefig(graphDir + os.path.sep + "freq_response.png")

def visualizeTimeOrderedData(sampleData, dataLabels, graphDir):
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
    plt.savefig(graphDir + os.path.sep + "time_ordered_data.png")


def getDataAndVisualize(dataDir = "../data", graphDir = "../graphs"):
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
    if not os.path.isdir(graphDir):
        os.mkdir(graphDir)
    visualizeTimeOrderedData(voltageData, dataLabels, graphDir)
    visualizeFreq(voltageData, dataLabels, graphDir)
    print("done!")

getDataAndVisualize()
