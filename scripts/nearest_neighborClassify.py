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

def formatUnknownData():
	rawTrainingData = list(csv.reader(open("../fingerprintData/unknown.csv")))
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


def classifyNearestNeighbor(formattedTrainingData, fillLevelData, neighbors):
	neigh = KNeighborsClassifier(n_neighbors=neighbors)
	neigh.fit(formattedTrainingData, fillLevelData)
	return neigh

def testClassifyNearestNeighbor(numTrials = 100, neighbors = 1):
	[formattedTrainingData, fillLevelData] = formatTrainingData()
	[formattedData, fillData] = formatUnknownData()
	neigh = classifyNearestNeighbor(formattedTrainingData, fillLevelData, neighbors)
	count = 0
	emptyCount = 0
	quarterCount = 0
	halfCount = 0
	threeQCount = 0
	fullCount = 0
	for index in range(len(formattedData)):
	#for trial in range(numTrials):
		#randIndex = random.randint(0, len(formattedTrainingData)-1)
		#correctLevel = fillLevelData[randIndex]
		#print("Expected Level = " + str(correctLevel))
		sampleToTest = formattedData[index]
		print(sampleToTest)
		#print(neigh.predict([sampleToTest]))
		predictedLevel = neigh.predict([sampleToTest])
		print("Predicted Level = " + str(predictedLevel[0]))
		if (str(predictedLevel[0]) == "EMPTY"):
			emptyCount += 1
		elif (str(predictedLevel[0]) == "QUARTER"):
			quarterCount += 1
		elif (str(predictedLevel[0]) == "HALF"):
			halfCount += 1
		elif (str(predictedLevel[0]) == "THREE_Q"):
			threeQCount += 1
		elif (str(predictedLevel[0]) == "FULL"):
			fullCount += 1
		#if (str(predictedLevel[0]) == str(correctLevel)):
			#print "yay!"
		#	count += 1
		print("\n")
	#print("Percent Accuracy = " + str(float(count/numTrials) * 100))
	print("Empty Count = " + str(emptyCount))
	print("Quarter Count = " + str(quarterCount))
	print("Half Count = " + str(halfCount))
	print("Three_Q Count = " + str(threeQCount))
	print("Full Count = " + str(fullCount))