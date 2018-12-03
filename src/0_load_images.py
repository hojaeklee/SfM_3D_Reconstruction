import os
import re

import numpy as np
from skimage import img_as_float
import cv2 as cv 
from cv2 import xphoto

from util import Logger	
import structures 

def load_images(folder_path, images):
	Logger._log("\nStep 0 (preprocess)")

	## Get list of image files from dataset path
	if not os.path.exists(folder_path):
		raise ValueError("Invalid data path: {}".format(folder_path))

	## Reset images list
	images = []

	# Regex to parse image names
	fname_regex = "^.*/frame_([\\dT\\.]+)_(rgb|depth)\\.png$"

	## Create intermediate map structure
	_tstamps = {}

	for filename in os.listdir(folder_path):
		path = os.path.abspath(filename)
		match = re.match(fname_regex, path)

		if match != None:
			"""
			* 0: ../data/frame_20150312T172452.627702_depth.png
			* 1: 20150312T172452.627702
			* 2: depth
			"""
			time_str = match.group(1)
			_tstamps[time_str] = True

	## Convert to vector of timestamps
	n = len(_tstamps)
	tstamps = []

	for key in _tstamps.keys():
		tstamps.append(key)

	new_n = 0
	for i in range(n):
		## Get time string
		time_str = tstamps[i]

		## Get file paths
		rgb_path = "{}/frame_{}_rgb.jpg".format(folder_path, time_str)
		dep_path = "{}/frame_{}_depth.png".format(folder_path, time_str)
		rgb_img = cv.imread(rgb_path)
		# _depth_img = cv.imread(dep_path, cv.IMREAD_ANYDEPTH) # load 16bit img; 2 refers to CV_LOAD_IMAGE_ANYDEPTH
		_depth_img = cv.imread(dep_path, 2)
		
		'''
		cv.imshow("rgb_img", rgb_img)
		cv.waitKey()
		cv.destroyAllWindows()
		'''

		## White-balance RGB image
		'''
		wb = xphoto.createGrayworldWB()
		wb.setSaturationThreshold(0.9) # This threshold is set manually
		rgb_undist_img = wb.balanceWhite(rgb_img)
		'''
		rgb_undist_img = np.zeros_like(rgb_img)
		cv.xphoto.balanceWhite(rgb_img, rgb_undist_img, 0)

		## Get grayscale image
		gray_undist_img = cv.cvtColor(rgb_undist_img, cv.COLOR_BGR2GRAY)
		
		## Bm1
		gray_undist_img = cv.cvtColor(rgb_img, cv.COLOR_BGR2GRAY)
		'''
		cv.imshow("gray_undist_img", gray_undist_img)
		cv.waitKey()
		cv.destroyAllWindows()
		'''
		## Convert depth map to floats
		# depth_img = (_depth_img.astype(float)) / 65535
		# depth_img = img_as_float(_depth_img) 
		depth_img = np.float32(_depth_img)

		'''
		cv.imshow("depth_img", depth_img)
		cv.waitKey()
		cv.destroyAllWindows()
		'''

		## Smooth depth map
		depth_smooth_img = cv.bilateralFilter(depth_img, 5, 10, 10)

		image = structures.Image(i, time_str, rgb_undist_img, gray_undist_img, depth_smooth_img, rgb_path, dep_path)
		images.append(image)

		new_n += 1

	print("Loaded {} RGB_D images.".format(new_n))
	return images


if __name__ == "__main__":
	print("In 0_load_images.py")