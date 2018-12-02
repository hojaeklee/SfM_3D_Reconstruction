import numpy as np
import cv2 as cv
import pcl

import util

class viewer:
	def __init__(self, title, low_thresh = 400, high_thresh = 8000):
		print("\nPCL")
		self._title = title
		self.low_thresh = low_thresh
		self.high_thresh = high_thresh

	def reduceCloud(self, cloud):
		voxel_resolution = 20.0
		sor = pcl.VoxelGridFilter_PointXYZRGBA(cloud)
		# sor.setInputCloud(cloud)
		sor.set_leaf_size(voxel_resolution, voxel_resolution, voxel_resolution)

		reduc = sor.filter()
		return reduc

	def createPointCloud(self, images, poses, cameraMatrix):
		## Fill cloud structure
		# pcl_points = pcl.PointCloud()

		## Per camera
		pcl_p = pcl.PointCloud_PointXYZRGBA()
		all_points = np.zeros(shape = (1, 4), dtype = np.float32)
				
		bad_depths = []
		for c in range(len(poses)):
			image = images[c]
			R = poses[c].R
			t = poses[c].t

			if R.size == 0:
				continue
			
			for i in range(image.dep.shape[0]):
				rgbs = image.rgb[i]
				deps = image.dep[i]

				for j in range(image.dep.shape[1]):
					rgb = rgbs[j]
					dep = deps[j]

					if dep < self.low_thresh or dep > self.high_thresh:
						bad_depths.append(dep)
						continue

					point = util.backproject3D(j, i, dep, cameraMatrix)
					gPoint = np.transpose(R) @ point - t
					point = gPoint

					rgb_temp = rgb[2] << 16 | rgb[1] << 8 | rgb[0] 
					point_ext = np.array([[point[0][0], point[1][0], point[2][0], rgb_temp]], dtype = np.float32)
					single_point = point_ext

					all_points = np.concatenate((all_points, single_point), axis = 0)
			
		pcl_p.from_array(all_points)
		# pcl_p_reduced = self.reduceCloud(pcl_p)

		print("Generated {} points.".format(len(pcl_p.to_list())))
		return pcl_p

	def saveCloud(self, pcl_points, fname):
		writer = pcl.save(pcl_points, fname)
		print("Saved point cloud to: {}".format(fname))

	def showCloudPoints(self, images, poses, cameraMatrix):
		pcl_points = self.createPointCloud(images, poses, cameraMatrix)
		pass

if __name__ == "__main__":
	print("In Viewer.py")