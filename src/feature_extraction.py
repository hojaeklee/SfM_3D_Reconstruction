

import numpy as np
import cv2 as cv

import structures

def extract_features(images, cam_Frames, descriptors_vec, low_threshold, high_threshold):
	print("\nStep 1 (features)")

	n = len(images)
	cam_Frames = [] 
	descriptors_vec = [] 

	## Create a SIFT detector
	feature_num = 0 
	octavelayers_num = 4
	contrast_thresh = 0.04
	edge_threshold = 4.0
	sigma = 1.6

	## BeersNMore
	sift = cv.xfeatures2d.SIFT_create(feature_num, octavelayers_num, contrast_thresh, edge_threshold, sigma)

	for i in range(n):
		image = images[i]

		## Detect keypoints and calculate descriptor vectors
		key_points, descriptors = sift.detectAndCompute(image.gray, None)

		keep_key_points = []
		keep_descriptors = []
		keep_depths = []

		## Keep 
		# print("# keypoints: {}".format(len(key_points)))
		for k in range(len(key_points)):
			d = image.dep[np.int(key_points[k].pt[1]), np.int(key_points[k].pt[0])]
			

			if d < low_threshold or d > high_threshold:
				continue
			else:
				keep_key_points.append(key_points[k])
				keep_descriptors.append(descriptors[k,])
				keep_depths.append(d)

		# print("# keep_key_points: {}".format(len(keep_key_points)))
		
		## wrap keypoints to cam_Frame and add in to cam_Frames
		cam_Frames.append(structures.CamFrame(i, keep_key_points, keep_depths))
		descriptors_vec.append(keep_descriptors)

		print("Found {} key points in image {}".format(len(keep_key_points), i))

	return images, cam_Frames, descriptors_vec

if __name__ == "__main__":
	print("In 1_feature_extraction.py")