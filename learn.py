# requires that images are stored in an N*X*Y matrix, where
# 	N = number of images
#	X*Y = dimensions of each image

import Math
import random
import cv2
import numpy as np

#===================
# class declarations
#===================

# model class - stores the model fit and centers
class Model:
	def __init__(self, score = 0, centers = []):
		self.score = score
		self.centers = []
# end class model

#=====================
# prediction functions
#=====================

# from a model and an image, determine if that image contains nodules
def predict(model,img):
	predictions = []
	# get img features
	features = SIFT DETECTOR (____)
	# compare each feature with model cluster centers
	centerDistances = [];
	centerValues = [];
	for i in range(0,len(features)):
		for j in range(0,len(model.centers)):
			.... problem: which feature is the one we care about?
	return predictions
	
# end predict

#===================
# training functions
#===================

# helper math evaluation stuff for test eval
npa = np.array

# use softmax to evaluate the cross-entropy loss from the classifiers
def softmax(w,t=1.0):
	e = np.exp(npa(w)/t)
	dist = e/np.sum(e)
	return dist
# end softmax

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
# <score, cluster-1-type, cluster-1-center, ....., cluster-n-type, cluster-n-center>
# where each of the above vector elements is a list/array
def train(splits,numsplits):
	models = []
	for testSplit in range(0,numsplits):
		currmodel = Model() # create a Model object
		for i in range(0,numsplits):
			if (i != testSplit):
				for j in range(0,len(splits[i])): # for each img in split
					# detect features with SIFT
					# classify the features based on if they are located
					# where we expect nodules to be
		# k-means cluster all features
		currmodel.clusters = kmeans......
		# run and evaluate test data
		weights = [];
		for i in range(0,len(splits(testSplit)):
			# test against model
			
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
