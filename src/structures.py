import numpy as np
import cv2 as cv

'''
Information related to RGB-D pair images
'''
class Image:
	def __init__(self):
		self.index = 0			# index of frame
		self.time = None		# Time taken
		self.rgb = None			# 1-channel cv::Mat containing rgb data
		self.gray = None		# 1-channel cv::Mat containing gray data
		self.dep = None			# 1-channel cv::Mat containing depth data
		self.rgb_path = "" 		# Path to rgb file
		self.dep_path = "" 		# Path to depth file

class CamFrame:
	def __init__(self):
		self.index = 0			# index of frame
		self.key_points = None	# list of feature points found in this image
		self.depths = None		# lsit of depth values of features found in this image

class ImagePair:
	def __init__(self):
		self.pair_index = [0, 0]
		self.matched_points = None
		self.matched_indices = None
		self.pair_depths = None
		self.R = None
		self.t = None

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


