import time
import random
import math
from detectors.detector import Detector

class IndividualEpsilonGreedyDetector(Detector):
	
	NAME = "Individual Epsilon Greedy Detector"

	# For now, the cache_size is in the number of cache elements. We should change this
        # to be bytes in the future to standardize the problem.
	def __init__(self, dataset, constraints, epsilon, discount):
		super(IndividualEpsilonGreedyDetector, self).__init__(dataset, constraints)
		self.epsilon = epsilon
		self.discount = discount

	# This algorithm will iterate over groups and cache results to prevent evaluating functional dependencies
	# multiple times. The group sizes are often small and we would expect the violations to be within these groups 
	# first. This algorithm will be extended to check other groups afterwards (maybe in a smarter way than just doing it randomly)
	def find_violations(self, comp_freq=10000, max_num_comparisons=250000):
		# Account for comparisons needed while preprocessing
		num_records_compared = len(self.dataset) * math.ceil(math.log(len(self.dataset)))

		# Choose most constraining
		self.most_constraining, index = self.choose_most_constraining(self.constraints)

		# Run Algorithm based on the type of constraint presented
		if self.most_constraining.is_equals():
			self.constraints.pop(index)
			ordered_dataset = self.dataset.group_by(self.most_constraining.get_attrs())
			return self.find_violations_with_groups(ordered_dataset, num_records_compared, comp_freq, max_num_comparisons)
		if self.most_constraining.is_range():
			ordered_dataset = self.dataset.sort_values(self.most_constraining.get_attrs(), asc=self.most_constraining.should_sort_ascending())
			return self.find_violations_sorted(ordered_dataset, num_records_compared, comp_freq, max_num_comparisons)
		
		

	# This algorithm will iterate over groups and cache results to prevent evaluating functional dependencies
	# multiple times. The group sizes are often small and we would expect the violations to be within these groups 
	# first. This algorithm will be extended to check other groups afterwards (maybe in a smarter way than just doing it randomly)
	def find_violations_with_groups(self, groups, num_records_compared, comp_freq, max_num_comparisons):
		num_comparisons = 0
		num_errors = 0
		comp_dict = {}

		group_indices = list(range(0, len(groups)))
		group_index = -1

		group_dict = {}
		for name, group in groups:
			group_dict[name] = set()

		while len(group_indices) > 0:
			# With probability epsilon1, we choose a random group. Otherwise, we go onto the next group.
			group_index = self.get_next_group_index(group_index, group_indices)
			name, group = self.get_specific_group(groups, group_indices[group_index])

			epsilon = self.epsilon

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
						epsilon *= self.discount
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

		return comp_dict

	def find_violations_sorted(self, ordered_dataset, num_records_compared, comp_freq, max_num_comparisons):
		num_comparisons = 0
		num_errors = 0
		comp_dict = {}

		record_dict = {}

		completed_set = set()

		current_record_index = -1
		total_num_records = len(ordered_dataset)
		indices_to_process = list(range(0, len(ordered_dataset)))
		while len(indices_to_process) > 0:

			# Get next record to process
			current_record_index += 1
			if current_record_index >= len(indices_to_process):
				current_record_index = 0
			
			index = indices_to_process[current_record_index]
			if index not in record_dict:
				record_dict[index] = set()

			# Get the corresponding record
			record_index, record = self.get_specific_record(ordered_dataset, index)

			# Initialize the epsilon value
			epsilon = self.epsilon

			completed = False

			for inner_index, inner_record in ordered_dataset.iterrows():
				# If we have already processed this inner record, then we move on
				if inner_index in record_dict[index]:
					continue

				record_dict[index].add(inner_index)

				# If we reach the current record, then we break (this is a sorted database)
				if not self.most_constraining.evaluate(record, inner_record):
					completed = True
					break

				record_has_error = True	
				for constraint in self.constraints:
					num_comparisons += 1
					if not constraint.evaluate(record, inner_record):
						record_has_error = False
						break

				num_records_compared += 1

				# We have a violation if all three clauses are true
				if record_has_error:
					epsilon *= self.discount
					num_errors += 1

				t = (record_index, inner_index)
				if inner_index < record_index:
					t = (inner_index, record_index)
				if t in completed_set:
					print(str(t) + " was a duplicate")
				completed_set.add(t)

				self.report_stats(num_errors, num_records_compared, comp_freq, comp_dict)

				if num_records_compared >= max_num_comparisons:
					return comp_dict

				# With probability epsilon2 we just break here and move to a new record
				if random.random() < epsilon:
					break

			# If we have reached the current record, then we stop here (and call this record completed)
			if completed:
				del record_dict[index]
				indices_to_process.pop(current_record_index)


		return comp_dict

	def get_specific_record(self, ordered_dataset, index):
		i = 0
		for j, record in ordered_dataset.iterrows():
			if i == index:
				return j, record
			i += 1
		return None, None

	def get_specific_group(self, groups, index):
		i = 0
		for name, group in groups:
			if i == index:
				return name, group
			i += 1
		return None, None

	def get_next_group_index(self, group_index, group_indices):
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
