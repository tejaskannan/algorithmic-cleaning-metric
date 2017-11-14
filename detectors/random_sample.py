from detectors.detector import Detector

class RandomSampleDetector(Detector):
	
	def __init__(self, dataset, constraints, fraction, rep_count):
		super(RandomSampleDetector, self).__init__(dataset, constraints)
		self.fraction = fraction
		self.rep_count = rep_count

	# This algorithm works in O(n + (np)^2(m)) time where n is the number of records, p is the sample fraction, and m is the
	# number of functional dependences (assuming each fd takes constant time). Runtime may be affected by the implementation of get_weights() too.
	def find_violations(self):
		weights = self.get_weights()
		times_found = 0
		number_of_comparisons = 0
		number_of_comparisons_when_found = 0
		for _ in range(0, self.rep_count):
			count, found = self.find_violations_runner(weights)
			number_of_comparisons += count
			if found:
				times_found += 1
				number_of_comparisons_when_found += count
		return number_of_comparisons / self.rep_count, number_of_comparisons_when_found / self.rep_count, times_found / self.rep_count

	def find_violations_runner(self, weights):
		num_comparisons = 0
		sampled_dataframe = self.dataset.get_random_sample(self.fraction, weights)
		for index, row in sampled_dataframe.iterrows():
			for i, r in sampled_dataframe.iterrows():
				if i <= index:
					continue
				for constraint in self.constraints:
					num_comparisons += 1
					if not constraint.evaluate(row, r):
						return num_comparisons, True
		return num_comparisons, False

	def get_weights(self):
		pass

		
