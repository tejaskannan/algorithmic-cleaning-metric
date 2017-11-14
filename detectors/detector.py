class Detector:
	def __init__(self, dataset, constraints):
		assert len(constraints) > 0
		self.dataset = dataset
		self.constraints = constraints

	# Return value is tuple of: 
	# 1. average number of fd's evalutated to reach violation (even if failure)
	# 2. average number of fd's evalutated to reach violation (only considering repetitions that find a violation)
	# 3. Fraction of reptitions that find a violation
	def find_violations(self):
		pass

	def is_dataset_dirty(self):
		violations = find_violations()
		return violations > 0, violations

