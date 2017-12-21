import time
import random
import math
from detectors.detector import Detector

class IndividualEpsilonGreedyDetector(Detector):
	
	NAME = "Individual Epsilon Greedy Detector"

	# For now, the cache_size is in the number of cache elements. We should change this
        # to be bytes in the future to standardize the problem.
	def __init__(self, dataset, constraints, epsilon1, epsilon2):
		super(IndividualEpsilonGreedyDetector, self).__init__(dataset, constraints)

		most_constraining, index = self.choose_most_constraining(constraints)
		self.constraints.pop(index)
		self.ordered_dataset = self.dataset.group_by(most_constraining.get_attrs())
		self.epsilon1 = epsilon1
		self.epsilon2 = epsilon2
		

	# This algorithm will iterate over groups and cache results to prevent evaluating functional dependencies
	# multiple times. The group sizes are often small and we would expect the violations to be within these groups 
	# first. This algorithm will be extended to check other groups afterwards (maybe in a smarter way than just doing it randomly)
	def find_violations(self, comp_freq=10000, max_num_comparisons=250000):
		num_comparisons = 0

		# account for the comparisons needed in preprocessing
		num_records_compared = len(self.dataset) * math.ceil(math.log(len(self.dataset)))
		num_errors = 0
		comp_dict = {}

		group_indices = list(range(0, len(self.ordered_dataset)))
		group_index = -1

		group_dict = {}
		groups = []
		for name, group in self.ordered_dataset:
			group_dict[name] = set()
			groups.append((name, group))

		#groups = [group for name, group in self.ordered_dataset]
		#groups.sort(key=lambda g: len(g), reverse=False)
		discount = 0.9


		while len(group_indices) > 0:
			# With probability epsilon1, we choose a random group. Otherwise, we go onto the next group.
			group_index = self.get_next_group_index(group_index, group_indices)
			name, group = self.get_specific_group(groups, group_indices[group_index])

			epsilon = self.epsilon2

			for index, record in group.iterrows():
				if index in group_dict[name]:
					continue

				# Add to the set of completed indices
				group_dict[name].add(index)

				for inner_index, inner_record in group.iterrows():
					if inner_index in group_dict[name]:
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
						epsilon *= discount
						num_errors += 1

					self.report_stats(num_errors, num_records_compared, comp_freq, comp_dict)

					if num_records_compared >= max_num_comparisons:
						return comp_dict

				# With probability epsilon2 we just break here and move to a new group
				if random.random() < epsilon:
					break

			# Add this group to the completed groups when we have processed all indices
			if len(group_dict[name]) == len(group):
				group_indices.pop(group_index)

		print(len(groups))
		print(num_records_compared)

		return comp_dict


	def get_specific_group(self, groups, index):
		i = 0
		for name, group in groups:
			if i == index:
				return name, group
			i += 1
		return None, None

	def get_next_group_index(self, group_index, group_indices):
		#r = random.random()
		r = 1.0
		if r < self.epsilon1:
			group_index = random.randint(0, len(group_indices))
		else:
			group_index += 1
		
		if group_index >= len(group_indices) or group_index < 0:
			return 0
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
