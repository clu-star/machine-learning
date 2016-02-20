# requires that images are stored in an N*X*Y matrix, where
# 	N = number of images
#	X*Y = dimensions of each image

import Math
import random
import cv2
import numpy as np




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
	testSplit = 0
	
# end train

def main(list):
	# takes in two user parameters: number of splits and output filename
	numsplits = 13 # there will be 19 images per split
	splits = split(list,numsplits)
	models = train(splits,numsplits)
	target = open(outfile,'w')
	for i in range(0,len(models)):
		for j in range(0,len(models[i])):
			target.write('[' + models[i][j] + ']');
	
# end main

main(list):
