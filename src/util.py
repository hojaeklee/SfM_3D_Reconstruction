import logging
import numpy as np
import cv2 as cv
import structures

import sys
import yaml

def showImage(title, img):
	print("\nShowing image: {}".format(title))
	cv.namedWindow(title, cv.WINDOW_NORMAL)
	cv.imshow(title, img)

def showImageAndWait(title, img):
	showImage(title, img)
	print("Press any key to continue...")
	cv.waitKey(0)

def backproject3D(x, y, depth, m_cameraMatrix):
	p = np.array([[x], [y], [1.0]])

	new_point = depth * np.matmul(np.linalg.inv(m_cameraMatrix), p)
	return new_point

###
# Custom logger, instantiate with namespace string to prefix messages with.
# For example:
#	Logger _log("Load Images")
##
class Logger(logging.LoggerAdapter):
	def _log(_namespace):
		logger = logging.getLogger(_namespace)
		return logger
	def tok():
		pass

def R2Quaternion(R):
	print(R)
	
def quat2R(q):
	pass

def checkCoherentRotation(R):
	if(np.abs(np.linalg.det(R)) - 1.0 > 1e-05):
		return false
	return true

def checkCoherent(q0, q1):
	q0_normed = cv.normalize(q0, None)
	q1_normed = cv.normalize(q1, None)

	if cv.norm(q1_normed + q0_normed) > 0.2:
		return False

	if cv.norm(q0) - cv.norm(q1) > 0.2 or cv.norm(q0) - cv.norm(q1) < -0.2:
		return False

	return True
		
def parseYamlFile(filename):
    '''
    Read the camera intrinsics, distortion coefficients, and some parameters for SfM pipeline.
    '''
    f = open(filename)
    x = yaml.load(f)
    f.close()

    mtx = np.array(x['camera_matrix']['data'], dtype = np.float32)
    low = x['depth_thresholds']['low']
    high = x['depth_thresholds']['high']
    return mtx.reshape(3,3), low, high

if __name__ == "__main__":
	print("In util.py")