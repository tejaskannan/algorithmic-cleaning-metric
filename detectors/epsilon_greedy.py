import time
import random
from detectors.detector import Detector

class HierarchicalEpsilonGreedyDetector(Detector):
	
	NAME = "Hierarchical Epsilon Greedy Detector"

	# For now, the cache_size is in the number of cache elements. We should change this
        # to be bytes in the future to standardize the problem.
	def __init__(self, dataset, constraints, epsilon):
		super(HierarchicalEpsilonGreedyDetector, self).__init__(dataset, constraints)

		most_constraining, index = self.choose_most_constraining(constraints)
		self.constraints.pop(index)
		self.ordered_dataset = self.dataset.group_by(most_constraining.get_attrs())
		self.epsilon = epsilon
		

	# This algorithm will iterate over groups and cache results to prevent evaluating functional dependencies
	# multiple times. The group sizes are often small and we would expect the violations to be within these groups 
	# first. This algorithm will be extended to check other groups afterwards (maybe in a smarter way than just doing it randomly)
	def find_violations(self, comp_freq=10000, max_num_comparisons=250000):
		num_comparisons = 0
		num_records_compared = 0
		num_errors = 0
		comp_dict = {}

		group_indices = list(range(0, len(self.ordered_dataset)))
		group_index = -1

		while len(group_indices) > 0:
			group_index = self.get_next_group_index(group_index, group_indices)
			group = self.get_specific_group(self.ordered_dataset, group_index)
			for index, record in group.iterrows():	
				completed_indexes = set()
				completed_indexes.add(index)
				for inner_index, inner_record in group.iterrows():
					if inner_index in completed_indexes:
						continue

					record_has_error = True	
					for constraint in self.constraints:
						num_comparisons += 1
						if not constraint.evaluate(record, inner_record):
							record_has_error = False
							break

					num_records_compared += 1

					# We have a violation if all three clauses are true
					if record_has_error:
						num_errors += 1		

					self.report_stats(num_errors, num_records_compared, comp_freq, comp_dict) 
	
					if num_records_compared >= max_num_comparisons:
						return comp_dict

					completed_indexes.add(inner_index)

		return comp_dict


	def get_specific_group(self, groups, index):
		i = 0
		for name, group in self.ordered_dataset:
			if i == index:
				return group
			i += 1
		return None

	def get_next_group_index(self, group_index, group_indices):
		r = random.random()
		if r < self.epsilon:
			group_index = random.randint(0, len(group_indices))
		else:
			group_index = min(group_index + 1, len(group_indices) - 1)
		group_indices.pop(group_index)
		return group_index

	def choose_most_constraining(self, constraints):
		equal_constraints = [constraint for constraint in constraints if constraint.get_operation_name() == "eq"]
		if len(equal_constraints) > 0:
			constr = equal_constraints[0]
			index = 0
			for i in range(1, len(equal_constraints)):
				if len(constr.get_attrs()) < len(equal_constraints[i].get_attrs()):
					constr = equal_constraints[i]
					index = i
			return constr, index
		return constraints[0], 0
