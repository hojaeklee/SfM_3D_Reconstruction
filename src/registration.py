import numpy as np
import cv2 as cv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D


import util

def register_camera(pairs, cam_Frames, cameraMatrix, distCoeffs):
	print("\nStep 3 (register)")
	
	## ------- Parameters for solvePnPRansac ------- ##
	useExtrinsicGuess = False
	iterationsCount = 1000
	reprojectionError = 2.5

	confidence = 0.999
	minInliers = 30

	flag = cv.SOLVEPNP_EPNP

	# get 3D-2D registration for all matched frames
	for p in range(len(pairs)):
		pair = pairs[p]

		i = pair.pair_index[0]
		j = pair.pair_index[1]

		keyPoints_i = pair.matched_points[0]
		keyPoints_j = pair.matched_points[1]

		depths_i = pair.pair_depths[0]
		depths_j = pair.pair_depths[1]

		## get depth value of all matched keypoints in image1
		points3D_i = []
		points3D_j = []

		for k in range(len(keyPoints_i)):
			x_i = keyPoints_i[k][0]
			y_i = keyPoints_i[k][1]
			d_i = depths_i[k]		

			## backproject 3D points
			objPoint_i = util.backproject3D(x_i, y_i, d_i, cameraMatrix)
			points3D_i.append(objPoint_i)

			x_j = keyPoints_j[k][0]
			y_j = keyPoints_j[k][1]
			d_j = depths_j[k]

			objPoint_j = util.backproject3D(x_j, y_j, d_j, cameraMatrix)
			points3D_j.append(objPoint_j)



		# print("objPoint_i: \n{}".format(objPoint_i))
		# print("points3D_i: \n{}".format(points3D_i))
		## OPENCV:
		## i provides: model coordinate system
		## j provides: camera coordinate system

		## rvec together with tvec, brings points from the model
		## coordinate system to the camera coordinate system.

		## US:
		## R_ji * p_i = p_j

		points3D_i = np.array(points3D_i)
		points3D_i = np.squeeze(points3D_i)
		
		points3D_ii = np.zeros((points3D_i.shape[0], 1, 3), np.float32)
		points3D_ii[:, 0, :] = points3D_i[:, :]
	
		
		points3D_j = np.array(points3D_j)
		points3D_j = np.squeeze(points3D_j)
		
		points3D_jj = np.zeros((points3D_j.shape[0], 1, 3), np.float32)
		points3D_jj[:, 0, :] = points3D_j[:, :]
		
		keyPoints_i = np.array(keyPoints_i)
		keyPoints_i = np.reshape(keyPoints_i, (keyPoints_i.shape[0], 1, keyPoints_i.shape[1]))

		keyPoints_j = np.array(keyPoints_j)
		keyPoints_j = np.reshape(keyPoints_j, (keyPoints_j.shape[0], 1, keyPoints_j.shape[1]))
		
		work_i, rvec_i, tvec_i, inliers_i = cv.solvePnPRansac(points3D_ii, keyPoints_j, cameraMatrix, \
								distCoeffs = None, \
								rvec = None, tvec = None, \
								useExtrinsicGuess = useExtrinsicGuess, \
								iterationsCount = iterationsCount, \
								reprojectionError = reprojectionError, \
								confidence = confidence, \
								inliers = None, flags = flag)
		

		work_j, rvec_j, tvec_j, inliers_j = cv.solvePnPRansac(points3D_jj, keyPoints_i, cameraMatrix, \
								distCoeffs = None, \
								rvec = None, tvec = None, \
								useExtrinsicGuess = useExtrinsicGuess, \
								iterationsCount = iterationsCount, \
								reprojectionError = reprojectionError, \
								confidence = confidence, \
								inliers = None, flags = flag)
		
		'''
		print("work_i: {}".format(work_i))
		print("work_j: {}".format(work_j))

		print("rvec_i: \n{}".format(rvec_i))
		print("rvec_j: \n{}".format(rvec_j))

		print("tvec_i: \n{}".format(tvec_i))
		print("tvec_j: \n{}".format(tvec_j))

		print("Inliers_i: {}".format(inliers_i.shape))
		print("Inliers_j: {}".format(inliers_j.shape))
		'''

		if (inliers_i.shape[0] < minInliers or inliers_j.shape[0] < minInliers):
			continue
		

		print("{}/{} inliers for {}-{} pair.".format(inliers_i.shape[0], inliers_j.shape[0], i, j))

		## Convert rvec and tvec to floats
		tvec_i = np.float32(tvec_i)
		rvec_i = np.float32(rvec_i)
		tvec_j = np.float32(tvec_j)
		rvec_j = np.float32(rvec_j)

		## Average R_i & R_j and t_i & t_j
		rvec = (rvec_i - rvec_j) / 2.0
		tvec = tvec_i
		R = cv.Rodrigues(rvec)[0]

		if not util.checkCoherent(rvec_i, rvec_j):
			print("Invalid r in {}-{}, this pair is skipped!".format(i, j))
			continue
		
		## Store, R, t
		pair.R = R
		pair.t = tvec

		# New vectors to retain only inliers info
		new_matched_indices_i = []
		new_matched_indices_j = []
		new_matched_kp_i = []
		new_matched_kp_j = []
		new_matched_depth_i = []
		new_matched_depth_j = []

		inliers_idx_j = 0
		inliers_idx_i = 0

		while (inliers_idx_i != inliers_i.shape[0]) and (inliers_idx_j != inliers_j.shape[0]):
			if inliers_i[inliers_idx_i, 0] < inliers_j[inliers_idx_j, 0]:
				inliers_idx_i += 1
			else: 
				if inliers_j[inliers_idx_j, 0] == inliers_i[inliers_idx_i, 0]:
					idx = inliers_j[inliers_idx_j, 0]
					# print(pair.matched_indices[0])
					new_matched_indices_i.append(pair.matched_indices[0][idx])
					new_matched_indices_j.append(pair.matched_indices[1][idx])
					new_matched_kp_i.append(keyPoints_i[idx])
					new_matched_kp_j.append(keyPoints_j[idx])
					new_matched_depth_i.append(depths_i[idx])
					new_matched_depth_j.append(depths_j[idx])
				inliers_idx_j += 1

		pair.matched_indices = (new_matched_indices_i, new_matched_indices_j)
		pair.matched_points = (new_matched_kp_i, new_matched_kp_j)
		pair.pair_depths = (new_matched_depth_i, new_matched_depth_j)

	return pairs, cam_Frames

if __name__ == "__main__":
	print("In 3_registration.py")