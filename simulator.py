import time
import csv
from plotter import plot
from dataset import Dataset
from detectors.brute_force import BruteForceDetector
from detectors.random_cache import RandomCacheDetector
from detectors.group_by_cache import GroupByCacheDetector
from detectors.simple_random_sample import SRSDetector
from detectors.weighted_sample import WeightedSampleDetector
from detectors.hierarchical import HierarchicalDetector
from detectors.hierarchical_sample import HierarchicalSampleDetector
from detectors.hierarchical_epsilon_greedy import HierarchicalEpsilonGreedyDetector
from detectors.individual_epsilon_greedy import IndividualEpsilonGreedyDetector
from constraints.boolean_constraint import BooleanConstraint

class Simulator:

	def __init__(self, file_name):
		self.dataset = Dataset(file_name)
		constr1 = BooleanConstraint(["phone"], "eq")
		constr2 = BooleanConstraint(["zip"], "neq")
		constr3 = BooleanConstraint([], "none")
		self.constraints = [constr1, constr2, constr3]
		

	def run(self):
		data_points = []
		#legend = ["Hierarchical"]
		max_num_comparisons = 400000

		legend = []
		ep = 0.01
		for i in range(0, 2):
			start = time.time()
			detector = IndividualEpsilonGreedyDetector(self.dataset, self.constraints[:], epsilon1=ep, epsilon2=ep)
			data_points.append(detector.find_violations(max_num_comparisons=max_num_comparisons))
			end = time.time()
			name = "Individual Epsilon Greedy " + str(ep) + " Time v" + str(i)
			print(name + " : " + str(end - start) + " seconds")
			legend.append(name)
		
		legend = legend + ["Brute Force", "Hierarchical"]

		start = time.time()
		detector = BruteForceDetector(self.dataset, self.constraints)
		data_points.append(detector.find_violations(max_num_comparisons=max_num_comparisons))
		end = time.time()
		print("Brute Force Time: " + str(end - start) + " seconds")

		start = time.time()
		detector = HierarchicalDetector(self.dataset, self.constraints[:])
		data_points.append(detector.find_violations(max_num_comparisons=max_num_comparisons))
		end = time.time()
		print("Hierarchical Time: " + str(end - start) + " seconds")

		plot(data_points, "Errors Found over Time", "Number of Comparisons", "Number of Errors", legend=legend, filename="output_500k_phone_zip.png", ymax=7000)

		#start = time.time()
		#detector = HierarchicalSampleDetector(self.dataset, self.constraints[:], 0.25)
		#print("Hierarchical Sample Number of Functions: " + str(detector.find_violations()))
		#end = time.time()
		#print("Time: " + str(end - start) + " seconds")
		
		#cache_size = 50
		#detector = RandomCacheDetector(self.dataset, self.constraints, cache_size)
		#start = time.time()
		#print("Cache Number of Functions: " + str(detector.find_violations()))
		#end = time.time()
		#print("Time: " + str(end - start))

		#detector = GroupByCacheDetector(self.dataset, self.constraints, cache_size)
		#start = time.time()
		#print("Group By Cache Number of Functions: " + str(detector.find_violations()))
		#end = time.time()
		#print("Time: " + str(end - start))
		
		#detector = SRSDetector(self.dataset, self.constraints, 0.01, 1)
		#print("SRS Number of Functions: " + str(detector.find_violations()))
		#detector = WeightedSampleDetector(self.dataset, self.constraints, 0.01, 1, use_inputs=True)
		#print("Weighted Number of Functions Ordered By Inputs: " + str(detector.find_violations()))
		#detector = WeightedSampleDetector(self.dataset, self.constraints, 0.01, 1, use_inputs=False)
		#print("Weighted Number of Functions Ordered By Outputs: " + str(detector.find_violations()))


if __name__ == "__main__":
	simulator = Simulator("datasets/dirty_hospital_small.csv")
	simulator.run()     
