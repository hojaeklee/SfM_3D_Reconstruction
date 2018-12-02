import numpy as np
import cv2 as cv

import Associativity
import util
import structures

def find_clusters(assocMat, cameraPoses, camFrames, pointClusters, pointMap, cameraMatrix, pairs):
	print("Step 6 (clusters)")

	## Function when walking through the pair tree
	
	## Skip _log.tok();
	def walkfunc(i, j, pair):
		depths_i = []; depths_j = []
		keypoints_i = []; keypoints_j = []
		kpIdx_i = []; kpIdx_j = []

		## Find index of other side of pair
		if pair.pair_index[0] == j:
			print("==j")
			kpIdx_i = pair.matched_indices[1]
			keypoints_i = pair.matched_points[1]
			depths_i = pair.pair_depths[1]

			kpIdx_j = pair.matched_indices[0]
			keypoints_j = pair.matched_points[0]
			depths_j = pair.pair_depths[0]
		else:
			print("==i")
			kpIdx_i = pair.matched_indices[0]
			keypoints_i = pair.matched_points[0]
			depths_i = pair.pair_depths[0]

			kpIdx_j = pair.matched_indices[1]
			keypoints_j = pair.matched_points[1]
			depths_j = pair.pair_depths[1]

		## get R and t of each camera in this pair
		R_i = cameraPoses[i].R
		t_i = cameraPoses[i].t
		R_j = cameraPoses[j].R
		t_j = cameraPoses[j].t

		if R_i.size == 0 or R_j.size == 0:
			return True

		## for all matching in camera j, get their global coordinate
		## and insert them in correponding cluster

		for m in range(len(keypoints_j)):
			x_j = keypoints_j[m][0][0]
			y_j = keypoints_j[m][0][1]
			point3D_j = util.backproject3D(x_j, y_j, depths_j[m], cameraMatrix)

			## Transform into global frame
			gPoint3D_j = np.transpose(R_j) @ point3D_j - t_j
			
			## Find matching global point from pointMap
			key = (i, kpIdx_i[m])
			p3D_idx = 0
			if not key in pointMap.keys():
				# if matching keypoint in camera i was not added to any cluster yet
				x_i = keypoints_i[m][0][0]
				y_i = keypoints_i[m][0][1]

				point3D_i = util.backproject3D(x_i, y_i, depths_i[m], cameraMatrix)

				## transform into global frame
				gPoint3D_i = np.transpose(R_i) @ point3D_i - t_i

				## add new entry in pointMap for camera i
				p3D_idx = len(pointClusters)
				pointMap[key] = p3D_idx

				## add 3D point in i into a new cluster
				pointClusters.append(gPoint3D_i)
			else:
				## if matching keypoint in camera j was added to a cluster already
				entry = list(pointMap.keys()).index(key)
				p3D_idx = entry[1]
			
			## Add current keypoint in camera j in pointmap
			key = (j, kpIdx_j[m])
			pointMap[key] = p3D_idx
		
			## Add 3D point in j into the cluster
			pointClusters[p3D_idx] = []
			pointClusters[p3D_idx].append(gPoint3D_j)

	# assocMat.walk(walkfunc)

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

	return pointClusters, pointMap

if __name__ == "__main__":
	print("In 6_find_clusters.py")