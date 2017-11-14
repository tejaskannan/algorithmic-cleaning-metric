from detectors.random_sample import RandomSampleDetector

class SRSDetector(RandomSampleDetector):
	
	def __init__(self, dataset, constraints, fraction, rep_count):
		super(SRSDetector, self).__init__(dataset, constraints, fraction, rep_count)
		self.fraction = fraction
		self.rep_count = rep_count

	def get_weights(self):
		return None
