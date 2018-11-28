"""
This file contains information from:
	* Associativity.cpp
	* Associativity.hpp
"""

import structures
import utils

class Associativity:
	"""Associativity of cameras (matching features, essentially camera pairs)"""

	"""
	typedef std::pair<int, int> PairIndex; 
		--> Python tuple 
	std::unordered_map<PairIndex, ImagePair*> _map;
		--> Python dictionary with tuple PairIndex as key and ImagePair* as value
	"""
	PairIndex = [0,0]
	_map = {}

	def __init__(self):
		self.n = 0

	def __init__(self, _n):
		self.n = _n

	def __init__(self, i, j):
		if (i, j) in _map.keys():
			return _map[(i, j)] # Return value of the key
		else:
			_map[makeIndex(i, j)] = None
			return None # Return value of the created key

	def makeIndex(a, b):
		i = min(a, b)
		j = b if i == a else a
		return (i, j)

	def getAssociatedPairs(i):
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

	def walk(func):
		checked = {}



if __name__ == "__main__":
	print("In Associativity.py")
	assocMat = Associativity()