import numpy as np
import cv2 as cv

import util
import structures

def glo_cam_poses(images, cameraPoses, pairs, tree):
	print("\nStep 5 (global)")

	## Add I for R, t of 0th camera
	## (Reference for "global" coordinate frame)
	cameraPoses.append(structures.CameraPose())
	cameraPoses[0].R = np.eye(3, dtype = "float32")
	cameraPoses[0].t = np.zeros((3, 1), dtype = "float32")

	## Go through spanning tree and for each camera calculate R and t
	## NOTE: This needs R, t of parent/previous camera
	if tree.n <= 1:
		return

	def walkfunc(i, j, pair):
		print("Checking ({} > {}) to calculate {}".format(i, j, j))

		R_i = cameraPoses[i].R
		t_i = cameraPoses[i].t

		if pair.pair_index[0] == i:
			R_ji = pair.R
			t_ji = pair.t
		else:
			R_ij = pair.R
			t_ij = pair.t
			R_ji = np.transpose(R_ij)
			t_ji = -1 * t_ij

		## Calculate j-th (global) camera pose
		R_j = np.matmul(R_ji, R_i)
		t_j = t_ji + t_i

		## Store calculated pose
		temp = structures.CameraPose()
		temp.R = R_j
		temp.t = t_j
		cameraPoses.append(temp)

	## iterate through all pairs
	for p in range(len(pairs)):
		pair = pairs[p]
		i = pair.pair_index[1]
		j = pair.pair_index[0]
		'''
		if i == pair.pair_index[0]:
			j = pair.pair_index[1]
		else:
			j = pair.pair_index[0]
		'''
		# chk_indx = assocMat.makeIndex(i, j)
		walkfunc(i, j, pair)

	# tree.walk(walkfunc)
	return cameraPoses

	

if __name__ == "__main__":
	print("In 5_global_cam_poses.py")