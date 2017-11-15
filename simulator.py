from dataset import Dataset
from detectors.brute_force import BruteForceDetector
from detectors.random_cache import RandomCacheDetector
from detectors.simple_random_sample import SRSDetector
from detectors.weighted_sample import WeightedSampleDetector
from constraints.functional_dependency import FunctionalDependency

class Simulator:

	def __init__(self, file_name):
		self.dataset = Dataset(file_name)
		fd1 = FunctionalDependency(["zip"], ["state"])
		fd2 = FunctionalDependency(["city", "zip"], ["state"])
		self.constraints = [fd1, fd2]
		

	def run(self):
		detector = BruteForceDetector(self.dataset, self.constraints)
		print("Brute Force Number of Functions: " + str(detector.find_violations()))
		cache_size = 5
		detector = RandomCacheDetector(self.dataset, self.constraints, cache_size)
		print("Cache Number of Functions: " + str(detector.find_violations()))
		#detector = SRSDetector(self.dataset, self.constraints, 0.01, 1)
		#print("SRS Number of Functions: " + str(detector.find_violations()))
		#detector = WeightedSampleDetector(self.dataset, self.constraints, 0.01, 1, use_inputs=True)
		#print("Weighted Number of Functions Ordered By Inputs: " + str(detector.find_violations()))
		#detector = WeightedSampleDetector(self.dataset, self.constraints, 0.01, 1, use_inputs=False)
		#print("Weighted Number of Functions Ordered By Outputs: " + str(detector.find_violations()))

if __name__ == "__main__":
	simulator = Simulator("datasets/dirty_hospital_small.csv")
	simulator.run()     
