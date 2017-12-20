from detectors.detector import Detector

class HierarchicalSampleDetector(Detector):
	
	# For now, the cache_size is in the number of cache elements. We should change this
        # to be bytes in the future to standardize the problem.
	def __init__(self, dataset, constraints, fraction):
		super(HierarchicalSampleDetector, self).__init__(dataset, constraints)

		self.most_constraining, index = self.choose_most_constraining(constraints)
		self.constraints.pop(index)
		self.fraction = fraction
		

	# This algorithm will iterate over groups and cache results to prevent evaluating functional dependencies
	# multiple times. The group sizes are often small and we would expect the violations to be within these groups 
	# first. This algorithm will be extended to check other groups afterwards (maybe in a smarter way than just doing it randomly)
	def find_violations(self):
		num_comparisons = 0
		self.ordered_dataset = self.dataset.get_random_sample(self.fraction).groupby(self.most_constraining.get_attrs())

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

					# We have a violation if all three clauses are true
					if record_has_error:			
						return num_comparisons, num_comparisons, 1.0

					completed_indexes.add(inner_index)
		return num_comparisons, num_comparisons, 0.0

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






