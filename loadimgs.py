import numpy as np
import cv2
import os
import csv

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

	    file = open('data.csv', "rb")
	    reader = csv.reader(file)
	    for row in reader:
		if row[0].startswith(filename):
	    	    self.noduleSize = row[2]
	    	    self.noduleX = row[5]
	    	    self.noduleY = row[6]
		    break;

	self.cvdata = cv2.imread('data_pngs/'+filename, 0)

files = os.listdir("./data_pngs")
imgarray = []

for x in files:
    a = img(x)
    imgarray.append(a)
    print(a.filename + ": Has nodule: " + str(a.hasNodule) + " of size: " + str(a.noduleSize) + " at x,y: " + str(a.noduleX) + ", " + str(a.noduleY))

print('imgarray.length: ' + str(len(imgarray)))
