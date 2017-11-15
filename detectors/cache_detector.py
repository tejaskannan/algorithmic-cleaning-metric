from detectors.detector import Detector
import random

class CacheDetector(Detector):
	
	# For now, the cache_size is in the number of cache elements. We should change this
        # to be bytes in the future to standardize the problem.
	def __init__(self, dataset, constraints, cache_size):
		super(CacheDetector, self).__init__(dataset, constraints)
		self.cache_size = cache_size
		self.constraint_cache = {}

	# This algorithm works in O(n^2m) time where n is the number of records and m is the
	# number of functional dependences (assuming each fd takes constant time)
	def find_violations(self):
		num_comparisons = 0
		for index, row in self.dataset:
			for i, r in self.dataset:
				if i <= index:
					continue
				for j in range(0, len(self.constraints)):
					evaluated_value = self.check_cache(row, r, self.constraints[j], j)
					if evaluated_value == None:
						evaluated_value = self.constraints[j].evaluate(row, r)
						self.add_to_cache(self.get_attributes_key(row, r, self.constraints[j], j), evaluated_value)
						num_comparisons += 1
					if not evaluated_value:
						return num_comparisons, num_comparisons, 1.0
		return num_comparisons, num_comparisons, 1.0

	# Cache is a map from (row1[X], row2[X], row1[Y], row2[Y], constraint_index) : True/False, were value is if the 
	# contraint is upheld. We need to include the constraint index because multiple constraints can use the same
	# input/output sets but do different things. Need to consider (in the future) possible collisions here.
	def add_to_cache(self, key, eval_value):
		# Element is already in the cache
		if key in self.constraint_cache:
			return

		# We can fit both input and output values in the cache
		if len(self.constraint_cache) < self.cache_size:
			self.constraint_cache[key] = eval_value
			return

		# The cache is full, so we remove elements before adding this new entry
		while len(self.constraint_cache) >= self.cache_size:		
			self.remove_element_from_cache()
		self.constraint_cache[key] = eval_value

	# Returns True/False if constraint is cached, None if not in cache
	def check_cache(self, row1, row2, constraint, constraint_index):
		key = self.get_attributes_key(row1, row2, constraint, constraint_index)
		if key in self.constraint_cache:
			return self.constraint_cache[key]
		key = self.get_attributes_key(row2, row1, constraint, constraint_index)
		if key in self.constraint_cache:
			return self.constraint_cache[key]
		return None


	def remove_element_from_cache(self):
		pass

	def get_attributes_key(self, row1, row2, constraint, constraint_index):
		row1_input = tuple([row1.loc[attr] for attr in constraint.get_input_attr()])
		row1_output = tuple([row1.loc[attr] for attr in constraint.get_output_attr()])
		row2_input = tuple([row2.loc[attr] for attr in constraint.get_input_attr()])
		row2_output = tuple([row2.loc[attr] for attr in constraint.get_output_attr()])
		return (row1_input, row2_input, row1_output, row2_output, constraint_index)


