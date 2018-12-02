import numpy as np
import cv2 as cv
import pcl

import util

class viewer:
	def __init__(self, title):
		print("PCL")
		self._title = title

	def reduceCloud(self, cloud):
		pass

	def createPointCloud(self, images, poses, cameraMatrix):
		## Fill cloud structure
		# pcl_points = pcl.PointCloud()

		## Per camera
		pcl_p = pcl.PointCloud_PointXYZRGB()
		all_points = np.zeros(shape = (2, 4), dtype = np.float32)
		
		print("Len of poses: {}".format(poses))
		
		bad_depths = []
		for c in range(len(poses)):
			image = images[c]
			R = poses[c].R
			t = poses[c].t

			if R.size == 0:
				continue

			print("Image.dep.shape[0]: {}".format(image.dep.shape[0]))
			print("Image.dep.shape[1]: {}".format(image.dep.shape[1]))
			for i in range(image.dep.shape[0]):
				rgbs = image.rgb[i]
				deps = image.dep[i]

				for j in range(image.dep.shape[1]):
					rgb = rgbs[j]
					dep = deps[j]

					if dep < 400 or dep > 8000:
						bad_depths.append(dep)
						#print(j * i)
						continue

					# print("dep: {}".format(dep))

					point = util.backproject3D(j, i, dep, cameraMatrix)
					gPoint = np.transpose(R) @ point - t
					point = gPoint

					point_ext = np.array([[point[0][0], point[1][0], point[2][0], 255.0]], dtype = np.float32)
					rgb_ext = np.array([[rgb[2], rgb[1], rgb[0], 255.0]], dtype = np.float32)
					# print(rgb_ext)
					single_point = np.concatenate((point_ext, rgb_ext), axis = 0)

				all_points = np.concatenate((all_points, single_point), axis = 0)
			
		pcl_p.from_array(all_points)

			## Reduce points every 10 cameras


		## Final reduction of points
		print("Bad Depths: {}".format(len(bad_depths)))
		print("Generated {} points.".format(all_points.shape[0]))
		return pcl_p

	def saveCloud(self, pcl_points, fname):
		writer = pcl.save(pcl_points, fname)
		print("Saved point cloud to: {}".format(fname))

	def showCloudPoints(self, images, poses, cameraMatrix):
		pcl_points = self.createPointCloud(images, poses, cameraMatrix)
		pass

if __name__ == "__main__":
	print("In Viewer.py")