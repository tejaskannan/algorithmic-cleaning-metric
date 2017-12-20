class Detector:
	def __init__(self, dataset, constraints):
		assert len(constraints) == 3
		self.dataset = dataset
		self.constraints = constraints

	# Return value is tuple of: 
	# 1. average number of fd's evalutated to reach violation (even if failure)
	# 2. average number of fd's evalutated to reach violation (only considering repetitions that find a violation)
	# 3. Fraction of reptitions that find a violation
	def find_violations(self, comp_freq=10000, max_num_comparisons=250000):
		pass

	def is_dataset_dirty(self):
		violations = find_violations()
		return violations > 0, violations

	def report_stats(self, num_errors, num_records_compared, comp_freq, comp_dict):
		if num_records_compared % comp_freq == 0:
			# print(self.NAME + " : " + str(num_errors) + " after " + str(num_records_compared) + " records compared.")
			comp_dict[num_records_compared] = num_errors


