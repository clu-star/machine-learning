# requires that images are stored in an N*X*Y matrix, where
# 	N = number of images
#	X*Y = dimensions of each image

# takes in N*X*Y matrix of images
# outputs split data
def split(list,numsplits):
	numImgs = len(list)
	
# end split


# takes in split data
# outputs model in the form
# <score, cluster-1-type, cluster-1-center, ....., cluster-n-type, cluster-n-center>
def train(splits):

# end train

def main(list):
	# takes in two user parameters: number of splits and output filename
	
	splits = split(list)
	models = train(splits)
	target = open(outfile,'w')
	for i in range(0,len(models)):
		for j in range(0,len(models[i])):
			target.write(models[i][j]+',');
	
# end main

main(list):
