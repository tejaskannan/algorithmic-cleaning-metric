import time
import math
from detectors.detector import Detector

class HierarchicalDetector(Detector):
	
	NAME = "Hierarchical Detector"

	# For now, the cache_size is in the number of cache elements. We should change this
        # to be bytes in the future to standardize the problem.
	def __init__(self, dataset, constraints):
		super(HierarchicalDetector, self).__init__(dataset, constraints)

		self.most_constraining, index = self.choose_most_constraining(constraints)

		if self.most_constraining.is_equals():
			self.constraints.pop(index)
			self.ordered_dataset = self.dataset.group_by(self.most_constraining.get_attrs())
		elif self.most_constraining.is_range():
			self.ordered_dataset = self.dataset.sort_values(self.most_constraining.get_attrs(), asc=self.most_constrainting.should_sort_ascending())
		

	# This algorithm will iterate over groups and cache results to prevent evaluating functional dependencies
	# multiple times. The group sizes are often small and we would expect the violations to be within these groups 
	# first. This algorithm will be extended to check other groups afterwards (maybe in a smarter way than just doing it randomly)
	def find_violations(self, comp_freq=10000, max_num_comparisons=250000):
		num_comparisons = 0

		# account for the comparisons needed in preprocessing
		num_records_compared = len(self.dataset) * math.ceil(math.log(len(self.dataset)))
		num_errors = 0
		comp_dict = {}

		groups = [group for name, group in self.ordered_dataset]
		#groups.sort(key=lambda g: len(g), reverse=False)


		for group in groups:
			completed_indexes = set()
			for index, record in group.iterrows():
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


		return comp_dict

	def find_violations_with_groups(self, comp_freq, max_num_comparisons):
		num_comparisons = 0
		num_records_compared = 0
		num_errors = 0
		comp_dict = {}

		for name, group in self.ordered_dataset:
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

	def find_violations_sorted(self, comp_freq, max_num_comparisons):
		num_comparisons = 0
		num_records_compared = 0
		num_errors = 0
		comp_dict = {}

		for index, record in self.ordered_dataset:
			for i, inner_record in self.ordered_dataset:
				if not self.most_constraining.evaluate(record, inner_record):
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
					num_errors += 1		

				self.report_stats(num_errors, num_records_compared, comp_freq, comp_dict) 

				if num_records_compared >= max_num_comparisons:
					return comp_dict
		return comp_dict


	def choose_most_constraining(self, constraints):
		equal_constraints = [constraint for constraint in constraints if constraint.is_equals()]
		if len(equal_constraints) > 0:
			return self.select_largest_input_set(equal_constraints)

		range_constraints = [constraint for constraint in constraints if constraint.is_range()]
		if len(range_constraints) > 0:
			return self.select_largest_input_set(range_constraints)

		return constraints[0], 0

	def select_largest_input_set(self, constraints):
		constr = constraints[0]
		index = 0
		for i in range(1, len(constraints)):
			if len(constr.get_attrs()) < len(constraints[i].get_attrs()):
				constr = constraints[i]
				index = i
		return constr, index






