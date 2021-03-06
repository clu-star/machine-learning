# requires that images are stored in an N*X*Y matrix, where
# 	N = number of images
#	X*Y = dimensions of each image

import sys
import math
import random
import cv2
import os
import csv
import numpy as np
from operator import add
from operator import mul
from operator import div

PXperCM = 683

#===================
# class declarations
#===================
class img:
    def __init__(self, filename):
        self.filename = filename
	self.hasNodule = False
        self.noduleSize = 0 
        self.noduleX = 0
        self.noduleY = 0
		
	# node
	if(filename.startswith('JPCLN')):
	    self.hasNodule = True

	    file = open('../data.csv', "rb")
	    reader = csv.reader(file)
	    for row in reader:
		if row[0].startswith(filename):
	    	    self.noduleSize = float(row[2])
	    	    self.noduleX = int(row[5])
	    	    self.noduleY = int(row[6])
		    break;

	self.cvdata = cv2.imread('data_pngs/'+filename, 0)

# model class - stores the model fit and centers
class Model:
	def __init__(self, score = 0, centers = []):
		self.score = score
		self.weights = []
		self.centers = []
		
	def printout():
		outstring = str(self.score)
		outstring = outstring + ' [' + ','.join(self.weights) + '] '
		outstring = outstring + ' [' + ','.join(self.centers) + '] '
		return outstring
# end class model

#============
# useful math
#============

# helper math evaluation stuff for test eval
npa = np.array
# use softmax to evaluate the cross-entropy loss from the classifiers
def softmax(w,t=1.0):
	e = np.exp(npa(w)/t)
	dist = e/np.sum(e)
	return dist
# end softmax

#=====================
# prediction functions
#=====================

# from a model and an image, determine if that image contains nodules
def predict(model,img):
	predictions = [0,0]
	# get img features
	#sift = cv2.xfeatures2d.SIFT_create()
	sift = cv2.SIFT()
	keyPoints,descriptors = sift.detectAndCompute(img,None)
	desc = np.reshape(descriptors,(len(descriptors)/128,128))
	# compare each feature with model cluster centers
	mostSimilarToNoduleScore = 0 # the most nodule-like element
	for j in range(0,len(descriptors)):
		for i in range(0,len(features)): # for each detected feature...
			currCenterDistances = []
			# find distances to each cluster center
			for j in range(0,len(model.centers)):
				arr = map(mul,model.centers[i],model.weights[i])
				arr = map(mul,arr,descriptors[i])
				currCenterDistances.append(sum(arr))
			currCenterDistances = softmax(currCenterDistances);
			probLN = 0;
			probNN = 0;
			for j in range(0,len(model.centers)):
				if model.centers[j].isNodule:
					probLN = probLN + currCenterDistances[j]
				else:
					probNN = probNN + currCenterDistances[j]
			currPrediction = [probLN,probNN]
			# if this is most similar to nodule so far...
			if (currPrediction[0] > predictions[0]):
				predictions = currPrediction
	return predictions
	
# end predict

#===================
# training functions
#===================

# takes in N*X*Y matrix of images
# outputs split data
def split(list,numsplits):
	random.shuffle(list)
	numImgs = len(list)
	imgsPerSplit = math.floor(numImgs/numsplits)
	splits = []
	nextadd = 0
	for i in range(0,numsplits):
		splits.append([])
		for j in range(int(nextadd),int(nextadd + imgsPerSplit)):
			splits[i].append(list[j])
		nextadd = nextadd + imgsPerSplit
	return splits
# end split


# takes in split data
# outputs model in the form
# score [cluster-1-LN-probability,..., cluster-n--LN-probability] [cluster-1-center,...,cluster-n-center]
# where each of the above vector elements is a list/array
def train(splits,numsplits):
	models = []
	for testSplit in range(0,numsplits):
		allKeyPoints = np.array([])
		allDescriptors = np.array([])
		allKeyClasses = []
		for i in range(0,numsplits):
			if (i != testSplit):
				for j in range(0,len(splits[i])): # for each img in split
					# detect features with SIFT
					sift = cv2.xfeatures2d.SIFT_create()
					keyPoints,descriptors = sift.detectAndCompute(splits[i][j],None)
					#keyPoints,descriptors = cv2.SIFT().detectAndCompute(splits[i][j],None)
					keyClasses = []
					# classify the features based on if they are located
					# where we expect nodules to be
					noduleMinX = splits[i][j].noduleX - splits[i][j].noduleSize*PXperCM/2.0
					noduleMaxX = splits[i][j].noduleX + splits[i][j].noduleSize*PXperCM/2.0
					noduleMinY = splits[i][j].noduleY - splits[i][j].noduleSize*PXperCM/2.0
					noduleMaxY = splits[i][j].noduleY + splits[i][j].noduleSize*PXperCM/2.0
					for k in range(0,len(keyPoints)):
						if ((keyPoints[k].x > noduleMinX) and (keyPoints[k].x < noduleMaxX) and (keyPoints[k].y > noduleMinY) and (keyPoints[k].y < noduleMaxY)):
							keyClasses.append(True) # is LN
						else:
							keyClasses.append(False) # is NN (not nodule)
					allKeyPoints = np.append(allKeyPoints,keyPoints)
					allDescriptors = np.append(allDescriptors,descriptors)
					allKeyClasses = np.append(allKeyClasses,keyClasses)
		# k-means cluster all features
		desc = np.reshape(allDescriptors,(len(allDescriptors)/128,128))
		desc = np.float32(desc)
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,1.0)
		flags = cv2.KMEANS_RANDOM_CENTERS
		currmodel = Model() # create a Model object
		compactness,labels,currmodel.clusters = cv2.kmeans(desc,40,None,criteria,20,flags)
		# parse model probabilities at each cluster
		countLN = []
		countNN = []
		for i in range(0,len(labels)):
			if (labels[i] >= len(countLN)):
					while (labels[i] >= len(countLN)):
						countLN.append(0)
						countNN.append(0)
			if allKeyClasses[i]:
				countLN[labels[i]] = countLN[labels[i]] + 1
			else:
				countNN[labels[i]] = countNN[labels[i]] + 1
		curmodel.weights = map(add,countLN,countNN)
		curmodel.weights = map(div,countLN,curmodel.weights)
		# run and evaluate test data
		scoreWeights = [];
		for i in range(0,len(splits(testSplit))):
			# test against model
			prediction = predict(currmodel,splits[testSplit][i])
			if (splits[testSplit][i].hasNodule):
				scoreWeights.append(prediction[0])
			else:
				scoreWeights.append(prediction[1])
		currmodel.score = (1/numSplits)*sum(scoreWeights)
		models.append(currmodel)
	return models
# end train

def main(list):
	# takes in one user parameter: output filename
	if len(sys.argv) != 2 :
		print("usage: python learn.py <output-filename>")
	else:
		# read images
		files = os.listdir("../data_pngs")
		imgarray = []
		for x in files:
			a = img(x)
			imgarray.append(a)
			print(a.filename + ": Has nodule: " + str(a.hasNodule) + " of size: " + str(a.noduleSize) + " at x,y: " + str(a.noduleX) + ", " + str(a.noduleY))
		print('imgarray.length: ' + str(len(imgarray)))
		# do learning
		numsplits = 13 # there will be 19 images per split
		splits = split(imgarray,numsplits)
		models = train(splits,numsplits)
		target = open(outfile,'w')
		for i in range(0,len(models)):
			target.write(models[i].printout());
# end main

main(list)
