import logging
import numpy as np
import cv2 as cv
import structures

def showImage(title, img):
	print("\nShowing image: {}".format(title))
	cv.namedWindow(title, cv.WINDOW_NORMAL)
	cv.imshow(title, img)

def showImageAndWait(title, img):
	pass

def backproject3D(x, y, depth, m_cameraMatrix):
	pass

###
# Custom logger, instantiate with namespace string to prefix messages with.
# For example:
#	Logger _log("Load Images")
##
class Logger(logging.LoggerAdapter):
	def _log(_namespace):
		self.logger = logging.getLogger(_namespace)
		return self.logger
	def tok():
		pass

def R2Quaternion(R):
	print(R)
	
def quat2R(q):
	pass

def checkCoherentRotation(R):
	pass

def checkCoherent(q0, q1):
	pass
		
if __name__ == "__main__":
	print("In util.py")
	i = structures.Image()