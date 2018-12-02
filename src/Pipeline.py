import os
import logging
import time
import importlib

import numpy as np
import cv2 as cv

import util
from util import Logger
from Associativity import associativity
from Viewer import viewer

_intrinsic_array = np.array([524, 0, 316.7, 0, 524, 238.5, 0, 0, 1])
_discoeff_array = np.array([0.2402, -0.6861, -0.0015, 0.0003])

class Pipeline:
	def __init__(self, _folder_path):
		self.folder_path = _folder_path
		self.cameraMatrix = np.reshape(_intrinsic_array, (3, 3))
		self.distCoeffs = np.reshape(_discoeff_array, (1, 4))
		self.load_images = importlib.import_module("0_load_images")
		self.feature_extraction = importlib.import_module("1_feature_extraction")
		self.find_matching_pairs = importlib.import_module("2_find_matching_pairs")
		self.registration = importlib.import_module("3_registration")
		self.spanning_tree = importlib.import_module("4_spanning_tree")
		self.global_cam_poses = importlib.import_module("5_global_cam_poses")
		self.find_clust = importlib.import_module("6_find_clusters")
		self.findCoM = importlib.import_module("7_find_CoM")
		self.BA = importlib.import_module("8_bundle_adjustment")

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
		images = []
		images = self.load_images.load_images(self.folder_path, images)
		

		###
		# Stage 1: Detect features in loaded images
		## 
		cam_Frames = []
		descriptors_vec = []
		images, cam_Frames, descriptors_vec = self.feature_extraction.extract_features(images, cam_Frames, descriptors_vec)
		
		###
		# Stage 2: Calculate descriptors and find image pairs through matching
		##
		image_pairs = []
		image_pairs, cam_Frames = self.find_matching_pairs.find_matching_pairs(images, cam_Frames, descriptors_vec, image_pairs)


		###
		# Stage 3: Compute pairwise R and t
		##
		image_pairs, cam_Frames = self.registration.register_camera(image_pairs, cam_Frames, self.cameraMatrix, self.distCoeffs)


		###
		# Stage 4: Construct associativity matrix and spannign tree
		##
		assocMat = associativity(len(cam_Frames))
		# print(dir(assocMat))

		for p in range(len(image_pairs)):
			pair = image_pairs[p]
			i = pair.pair_index[0]
			j = pair.pair_index[1]

			if pair.R.size != 0:
				continue
			
			assocMat.assignPair(i, j, pair)
			assocMat.assignPair(j, i, pair)

		tree = associativity()
		camera_num = self.spanning_tree.build_spanning_tree(image_pairs, assocMat, tree)

		tree = assocMat

		###
		# Stage 5: Compute global Rs and ts
		##
		gCameraPoses = []
		gCameraPoses = self.global_cam_poses.glo_cam_poses(images, gCameraPoses, image_pairs, tree)
		
		###
		# Stage 6: Find and cluster depth points from local camera frame to global camera frame
		##
		pointClusters = []
		pointMap = {}
		pointClusters, pointMap = self.find_clust.find_clusters(assocMat, gCameraPoses, cam_Frames, pointClusters, pointMap, self.cameraMatrix, image_pairs)

		###
		# Stage 7: get center of mass from clusters
		## 
		pointCloud = []
		pointCloud = self.findCoM.find_CoM(pointClusters, pointCloud)

		## Save cloud before BA
		view = viewer("Before BA")
		cloud = view.createPointCloud(images, gCameraPoses, self.cameraMatrix)
		# n = len(clouds.points)
		# folder = os.current_dir()
		fname = "./test.pcd"

		# if save_clouds:
		view.saveCloud(cloud, fname)
		

		###
		# Stage 8: Bundle Adjustment
		## 
		_placeholder = self.BA.bundle_adjustment(pointMap, cam_Frames, False, gCameraPoses, pointCloud)


		## Show calculated pointcloud



if __name__ == "__main__":
	print("In Pipeline.py")
