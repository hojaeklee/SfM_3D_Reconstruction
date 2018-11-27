import cv2 as cv
import Pipeline
import Associativity
import util

def find_clusters(assocMat, cameraPoses, camFrames, pointClusters, pointMap):
	"""find_clusters

	Args:
		assocMat: 
		cameraPoses:

	Returns:
	
	"""
	print("Step 6 (clusters)")

	## Function when walking through the pair tree
	assocMat.walk()

	## Skip _log.tok();

if __name__ == "__main__":
	print("In 6_find_clusters.py")