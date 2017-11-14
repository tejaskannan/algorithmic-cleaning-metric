from detectors.detector import Detector

class BruteForceDetector(Detector):
	
	def __init__(self, dataset, constraints):
		super(BruteForceDetector, self).__init__(dataset, constraints)

	# This algorithm works in O(n^2m) time where n is the number of records and m is the
	# number of functional dependences (assuming each fd takes constant time)
	def find_violations(self):
		num_comparisons = 0
		for index, row in self.dataset:
			for i, r in self.dataset:
				if i <= index:
					continue
				for constraint in self.constraints:
					num_comparisons += 1
					if not constraint.evaluate(row, r):
						return num_comparisons, num_comparisons, 1.0
		return num_comparisons, num_comparisons, 1.0
