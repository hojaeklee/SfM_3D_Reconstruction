import logging
import time
import importlib

import numpy as np
import cv2 as cv

import util
from util import Logger

_intrinsic_array = np.array([524, 0, 316.7, 0, 524, 238.5, 0, 0, 1])
_discoeff_array = np.array([0.2402, -0.6861, -0.0015, 0.0003])

class Pipeline:
	load_images = importlib.import_module("0_load_images")
	feature_extraction = importlib.import_module("1_feature_extraction")
	find_matching_pairs = importlib.import_module("2_find_matching_pairs")
	registration = importlib.import_module("3_registration")
	spanning_tree = importlib.import_module("4_spanning_tree")
	global_cam_poses = importlib.import_module("5_global_cam_poses")
	find_clusters = importlib.import_module("6_find_clusters")
	find_CoM = importlib.import_module("7_find_CoM")
	bundle_adjustment = importlib.import_module("8_bundle_adjustment")

	def __init__(self, _folder_path):
		self.folder_path = _folder_path
		
	def run(self, save_clouds, show_clouds):
		"""
		Args:
			save_clouds (bool): Default False
			show_clouds (bool): Default False

		Returns: void
		"""
		Logger._log("Pipeline")

		###
		# Stage 0: Detect features in loaded images
		##
		'''
		NOTE: We should return modified things for scoping purposes,
				unless someone knows very well how to split classes in Python.
				I have looked at some ways but honestly it's not really "Pythonic". 
		'''
		images = load_images.load_images(self.folder_path, images)
		

		###
		# Stage 1: Detect features in loaded images
		## 
		_placeholder = feature_extraction.extract_features(images, cam_Frames, descriptors_vec)
		pass

if __name__ == "__main__":
	print("In Pipeline.py")
