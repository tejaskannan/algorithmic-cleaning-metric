import time
from detectors.detector import Detector

class BruteForceDetector(Detector):
		
	NAME = "Brute Force"

	def __init__(self, dataset, constraints):
		super(BruteForceDetector, self).__init__(dataset, constraints)

	# This algorithm works in O(n^2m) time where n is the number of records and m is the
	# number of functional dependences (assuming each fd takes constant time)
	def find_violations(self, comp_freq=10000, max_num_comparisons=250000):
		constr1 = self.constraints[0]
		constr2 = self.constraints[1]
		constr3 = self.constraints[2]

		# initialize counters
		num_comparisons = 0
		num_records_compared = 0
		num_errors = 0
		comp_dict = {}
	
		for index, row in self.dataset:
			for i, r in self.dataset:
				if i <= index:
					continue

				record_has_error = True	
				for constraint in self.constraints:
					num_comparisons += 1
					if not constraint.evaluate(row, r):
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
