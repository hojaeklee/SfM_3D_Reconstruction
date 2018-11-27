import cv2 as cv
import Pipeline
import Associativity
import util

def find_CoM(pointClusters, pointCloud):
	"""find_CoM
	
	Args:
		pointClusters
		pointCloud

	Returns:
		None
	"""
	print("Step 7 (global)")
	print("cluster number = {}".format(pointClusters.size()))	

	for c in range(pointClusters.size()):
		mean_ = cv.reduce(pointClusters[c])
		# 
		pointCloud[c] = mean

	## Skip _log.tok();
	
if __name__ == "__main__":
	print("In 7_find_CoM.py")