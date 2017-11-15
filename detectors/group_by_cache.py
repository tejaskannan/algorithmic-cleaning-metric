from detectors.random_cache import RandomCacheDetector

class GroupByCacheDetector(RandomCacheDetector):
	
	# For now, the cache_size is in the number of cache elements. We should change this
        # to be bytes in the future to standardize the problem.
	def __init__(self, dataset, constraints, cache_size):
		super(GroupByCacheDetector, self).__init__(dataset, constraints, cache_size)
		self.grouped_dataset = self.dataset.group_by(self.get_attr_to_group_by(constraints))

	# This algorithm works in O(n^2m) time where n is the number of records and m is the
	# number of functional dependences (assuming each fd takes constant time)
	def find_violations(self):
		num_comparisons = 0

		for name, group in self.grouped_dataset:
			for index, record in group.iterrows():	
				completed_indexes = set()
				completed_indexes.add(index)
				for inner_index, inner_record in group.iterrows():
					if inner_index in completed_indexes:
						continue
					evaluation, num_comparisons = self.evaluate_records(record, inner_record, num_comparisons)
					if not evaluation:
						return num_comparisons, num_comparisons, 1.0
					completed_indexes.add(inner_index)
		return num_comparisons, num_comparisons, 1.0
		
	def evaluate_records(self, record1, record2, num_comparisons):
		for j in range(0, len(self.constraints)):
			evaluated_value = self.check_cache(record1, record2, self.constraints[j], j)
			if evaluated_value == None:
				evaluated_value = self.constraints[j].evaluate(record1, record2)
				self.add_to_cache(self.get_attributes_key(record1, record2, self.constraints[j], j), evaluated_value)
				num_comparisons += 1
			if not evaluated_value:
				return False, num_comparisons
		return True, num_comparisons


	def get_attr_to_group_by(self, contraints):
		return self.constraints[0].get_input_attr()

