"""
This file contains information from:
	* Associativity.cpp
	* Associativity.hpp
"""

import structures
import util
from queue import *

class associativity:
	"""Associativity of cameras (matching features, essentially camera pairs)"""

	"""
	typedef std::pair<int, int> PairIndex; 
		--> Python tuple 
	std::unordered_map<PairIndex, ImagePair*> _map;
		--> Python dictionary with tuple PairIndex as key and ImagePair* as value
	"""
	def __init__(self, _n = 0):
		self.n = _n
		self._map = {}
		self.PairIndex = (0, 0)

	def makeIndex(self, a, b):
		i = min(a, b)
		j = b if i == a else a
		return (i, j)

	def assignPair(self, i, j, pair):
		if (i, j) in self._map.keys():
			print("Already in _map")
			pass
			# return _map[(i, j)] # Return value of the key
		else:
			self._map[self.makeIndex(i, j)] = pair
			# return None # Return value of the created key

	def getAssociatedPairs(self, i):
		"""
		pImagePairs/ImagePairs is an array of ImagePair() objects defined in structure.py
		ImagePair() is a class defined in structures.py
		"""
		pairs = []
		pair = structures.ImagePair()
		
		for j in range(self.n):
			if i == j:
				continue
			else:
				pass

		return pairs

	def walk(self, func):
		checked = {}
		pass


if __name__ == "__main__":
	print("In Associativity.py")
	assocMat = Associativity()