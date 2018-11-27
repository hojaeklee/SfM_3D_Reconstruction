import numpy as np
import cv2 as cv
import Pipeline
import Associativity
import util

def glo_cam_poses(images, cameraPoses, pairs, tree):
	print("Step 5 (global)")

	## Add I for R, t of 0th camera
	## (Reference for "global" coordinate frame)

	cameraPoses.resize(tree.n)
	cameraPoses[0].R = np.eye(3, dtype = "float32")
	cameraPoses[0].t = np.zeros((3, 1), dtype = "float32")

	## Go through spanning tree and for each camera calculate R and t
	## NOTE: This needs R, t of parent/previous camera
	if tree.n <= 1:
		return
	tree.walk()

	# Skip _log.tok() for now

if __name__ == "__main__":
	print("In 5_global_cam_poses.py")