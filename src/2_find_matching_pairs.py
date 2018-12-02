import numpy as np
import cv2 as cv
import structures

import util

def find_matching_pairs(images, camframes, descriptors_vec, pairs):
	print("Step 2 (matching)")

	N = len(descriptors_vec)

	## Our parameters
	min_matches = 30

	for j in range(N):
		## Initialize descriptors matcher
		## Enable cross-checking
		bfmatcher = cv.BFMatcher(cv.NORM_L2, crossCheck = True)

		## Get descriptors of j-th image
		descriptors_j = descriptors_vec[j]
		descriptors_j = np.float32(descriptors_j) / 255.0

		for i in range(j+1, N):
			matches = []
			descriptors_i = descriptors_vec[i]

			## Must
			descriptors_i = np.float32(descriptors_i) / 255.0

			## Match descriptors
			## Output is distance between descriptors
			matches = bfmatcher.match(descriptors_i, descriptors_j)

			## Stop if not enough matches
			if len(matches) < min_matches:
				continue
			else:
				print("Got {} matches for {}-{}".format(len(matches), i, j))

				matched_keypoints_i = []
				matched_keypoints_j = []
				matched_indices_i = []
				matched_indices_j = []
				depth_values_i = []
				depth_values_j = []

				## Only store matched keypoints and their dpeths
				for it in matches:
					# print(it.trainIdx)

					## Only save pt, drop other keypoint members
					point_i = camframes[i].key_points[it.queryIdx].pt
					point_j = camframes[j].key_points[it.trainIdx].pt

					matched_keypoints_i.append(point_i)
					matched_keypoints_j.append(point_j)

					matched_indices_i.append(it.queryIdx)
					matched_indices_j.append(it.trainIdx)

					## Save depth of keypoints
					d_i = camframes[i].depths[it.queryIdx]
					d_j = camframes[j].depths[it.trainIdx]

					depth_values_i.append(d_i)
					depth_values_j.append(d_j)

				## Add to pairs structures
				pair = structures.ImagePair((i, j), (matched_keypoints_i, matched_keypoints_j), (matched_indices_i, matched_indices_j), (depth_values_i, depth_values_j))			
				pairs.append(pair)

				print("depth_values_i: {}".format(len(depth_values_i)))
				print("depth_values_j: {}".format(len(depth_values_j)))
			# Remove continue to see images
			continue
			print("{} \t {} \t {}".format(len(camframes[i].key_points), len(camframes[j].key_points), len(matches)))
			out = cv.drawMatches(images[i].rgb, camframes[i].key_points, \
							images[j].rgb, camframes[j].key_points, \
							matches, None, flags = 4) 
			print("Match {}-{}".format(i, j))
			util.showImageAndWait("Match results", out)

	return pairs, camframes


if __name__ == "__main__":
	print("In 2_find_matching_pairs.py")
