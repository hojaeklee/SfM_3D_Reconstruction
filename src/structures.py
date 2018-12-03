import numpy as np
import cv2 as cv

"""
Information related to RGB-D pair images
"""

class Image:
	def __init__(self, index, time, rgb, gray, dep, rgb_path, dep_path):
		self.index = index			# index of frame
		self.time = time			# Time taken
		self.rgb = rgb				# 1-channel cv::Mat containing rgb data
		self.gray = gray			# 1-channel cv::Mat containing gray data
		self.dep = dep				# 1-channel cv::Mat containing depth data
		self.rgb_path = rgb_path 	# Path to rgb file
		self.dep_path = dep_path 	# Path to depth file

class CamFrame:
	def __init__(self, index, key_points, depths):
		self.index = index				# index of frame
		self.key_points = key_points	# list of feature points found in this image
		self.depths = depths			# list of depth values of features found in this image

class ImagePair:
	def __init__(self, pair_index, matched_points, matched_indices, pair_depths, R = np.zeros((3, 3)), t = np.zeros((3, 1))):
		self.pair_index = pair_index
		self.matched_points = matched_points
		self.matched_indices = matched_indices
		self.pair_depths = pair_depths
		self.R = R
		self.t = t

class CameraPose:
	def __init__(self):
		self.R = None
		self.t = None


if __name__ == "__main__":
	print("In structures.py")
	i = Image()
	cf = CamFrame()
	ip = ImagePair()
	cp = CameraPose()


