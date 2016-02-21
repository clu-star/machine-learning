# requires that images are stored in an N*X*Y matrix, where
# 	N = number of images
#	X*Y = dimensions of each image

import Math
import random
import cv2
import numpy as np

PXperCM = 683

#===================
# class declarations
#===================

# model class - stores the model fit and centers
class Model:
	def __init__(self, score = 0, centers = []):
		self.score = score
		self.weights = []
		self.centers = []
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
	predictions = [0 0]
	# get img features
	features = SIFT DETECTOR (____)
	# compare each feature with model cluster centers
	mostSimilarToNoduleScore = 0 # the most nodule-like element
	for i in range(0,len(features)): # for each detected feature...
		currCenterDistances = []
		# find distances to each cluster center
		for j in range(0,len(model.centers)):
			
			.... problem: which feature is the one we care about?______
			__________need to multiply by image weight or 1-cluster weight
		currCenterDistances = softmax(currCenterDistances);
		probLN = 0;
		probNN = 0;
		for j in range(0,len(model.centers)):
			if model.centers[j].isNodule:
				probLN = probLN + currCenterDistances[j]
			else:
				probNN = probNN + currCenterDistances[j]
		currPrediction = [probLN probNN]
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
	imgsPerSplit = Math.floor(numImgs/numsplits)
	splits = []
	nextadd = 0
	for i in range(0,numsplits):
		split.append([])
		for j in range(nextadd,nextadd + imgsPerSplit):
			split[i].append(list[j])
		nextadd = nextadd + imgsPerSplit
	return splits
# end split


# takes in split data
# outputs model in the form
# <score, cluster-1-LN-probability, cluster-1-center, ....., cluster-n--LN-probability, cluster-n-center>
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
					keyClasses = []
					# classify the features based on if they are located
					# where we expect nodules to be
					noduleminx = splits[i][j].noduleX - splits[i][j].noduleSize/2.0
					nodulemaxx = splits[i][j].noduleX + splits[i][j].noduleSize/2.0
					noduleminy = splits[i][j].noduleY - splits[i][j].noduleSize/2.0
					nodulemaxy = splits[i][j].noduleY + splits[i][j].noduleSize/2.0
					for k in range(0,len(keyPoints)):
						if ((keyPoints[k].x > noduleMinX) && (keyPoints[k].x < noduleMaxX) && (keyPoints[k].y > noduleMinY) && (keyPoints[k].y < noduleMaxY)):
							keyClasses.append(True)
						else:
							keyClasses.append(False)
					allKeyPoints = np.append(allKeyPoints,keyPoints)
					allDescriptors = np.append(allDescriptors,descriptors)
					allKeyClasses = np.append(allKeyClasses,keyClasses)
		# k-means cluster all features
		currmodel = Model() # create a Model object
		compactness,labels,currmodel.clusters = cv2.kmeans()____
		____________parse model probs
		curmodel.weights = []
		# run and evaluate test data
		weights = [];
		for i in range(0,len(splits(testSplit)):
			# test against model
			weights = predict(currmodel,splits[testSplit][i])
		currmodel.score = softmax(weights)
		models.append(currmodel)
	return models
# end train

def main(list):
	# takes in two user parameters: number of splits and output filename
	numsplits = 13 # there will be 19 images per split
	splits = split(list,numsplits)
	models = train(splits,numsplits)
	target = open(outfile,'w')
	for i in range(0,len(models)):
		for j in range(0,len(models[i])):
			target.write('[' + models[i][j] + '] ');
	
# end main

main(list):
