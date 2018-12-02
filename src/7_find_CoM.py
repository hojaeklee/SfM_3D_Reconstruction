import cv2 as cv

from Associativity import associativity
import util

def find_CoM(pointClusters, pointCloud):
	print("Step 7 (global)")
	print("cluster number = {}".format(len(pointClusters)))	

	# print(pointClusters[0])
	for c in range(len(pointClusters)):
		m = cv.reduce(pointClusters[c][0], 1, cv.REDUCE_AVG)
		pointCloud.append(m)

	return pointCloud
	## Skip _log.tok();
	
if __name__ == "__main__":
	print("In 7_find_CoM.py")