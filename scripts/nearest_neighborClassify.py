#!/usr/bin/python

import os
import csv
from sklearn.neighbors import KNeighborsClassifier
import random

def formatTrainingData():
	rawTrainingData = list(csv.reader(open("../fingerprintData/artur_fingerprints.csv")))
	print(rawTrainingData[0])
	formattedTrainingData = []
	fillLevelData = []
	for i in range(len(rawTrainingData)):
		fillLevel = rawTrainingData[i][0]
		freqVal = float(rawTrainingData[i][1][6:])
		freq1 = float(rawTrainingData[i][2])
		mag1 = float(rawTrainingData[i][6])
		freq2 = float(rawTrainingData[i][3])
		mag2 = float(rawTrainingData[i][7])
		freq3 = float(rawTrainingData[i][4])
		mag3 = float(rawTrainingData[i][8])
		freq4 = float(rawTrainingData[i][5])
		mag4 = float(rawTrainingData[i][9])
		formattedTrainingData.append([freqVal, freq1, mag1])
		fillLevelData.append(fillLevel)
		formattedTrainingData.append([freqVal, freq2, mag2])
		fillLevelData.append(fillLevel)
		formattedTrainingData.append([freqVal, freq3, mag3])
		fillLevelData.append(fillLevel)
		formattedTrainingData.append([freqVal, freq4, mag4])
		fillLevelData.append(fillLevel)
	return [formattedTrainingData, fillLevelData]

def classifyNearestNeighbor(numTrials = 100):
	[formattedTrainingData, fillLevelData] = formatTrainingData()
	neigh = KNeighborsClassifier(n_neighbors=1)
	neigh.fit(formattedTrainingData, fillLevelData)
	count = 0
	for trial in range(numTrials):
		randIndex = random.randint(0, len(formattedTrainingData)-1)
		correctLevel = fillLevelData[randIndex]
		print("Expected Level = " + str(correctLevel))
		sampleToTest = formattedTrainingData[randIndex]
		#print(sampleToTest)
		#print(neigh.predict([sampleToTest]))
		predictedLevel = neigh.predict([sampleToTest])
		print(predictedLevel[0])
		if (str(predictedLevel[0]) == str(correctLevel)):
			print "yay!"
			count += 1
		print("\n")
	print ("Count = " + str(count))