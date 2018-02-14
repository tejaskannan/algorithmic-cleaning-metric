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
		self.report_freq = 10000
		self.max_num_comparisons = 20000

	def write_to_csv(self, file_name, data_points, legend):
		checkpoints = list(range(self.report_freq, self.max_num_comparisons + 1, self.report_freq))
		with open(file_name, "w") as csvfile:
			csv_writer = csv.writer(csvfile, delimiter='\t', quotechar='\t', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow(legend)
			for checkpoint in checkpoints:
				row = [checkpoint]
				for data_point in data_points:
					if checkpoint not in data_point:
						row.append("0")
					else:
						row.append(str(data_point[checkpoint]))
				csv_writer.writerow(row)
				

	def run(self, tests):
		#legend = ["Hierarchical"]
		random_trials = 1
		epsilons = [0.99]
		lambdas = [0.5]

		i = 0
		for file_name, constraints in tests:
			dataset = Dataset(file_name)
			data_points = []
			legend = ["Comparisons"]
			for constraint in constraints:
				brute_force_detector = BruteForceDetector(dataset, constraint[:])
				data_points.append(brute_force_detector.find_violations(comp_freq=self.report_freq, max_num_comparisons=self.max_num_comparisons))
				legend.append("Brute Force")

				hierarchical_detector = HierarchicalDetector(dataset, constraint[:])
				data_points.append(hierarchical_detector.find_violations(comp_freq=self.report_freq, max_num_comparisons=self.max_num_comparisons))
				legend.append("Hierarchical")

				for epsilon in epsilons:
					for lmbda in lambdas:
						for trial in range(0, random_trials):
							random_detector = IndividualEpsilonGreedyDetector(dataset, constraint[:], epsilon=epsilon, discount=lmbda)
							data_points.append(random_detector.find_violations(comp_freq=self.report_freq, max_num_comparisons=self.max_num_comparisons))
							legend.append("Epsilon Greedy Ep: " + str(epsilon) + " Disc: " + str(lmbda) + " v" + str(trial))

				dataset_name = (file_name.split("/")[1]).split(".")[0]
				attrs = [constr.get_attrs() for constr in constraint]
				flattened_attrs = []
				for attr_list in attrs:
					for attr in attr_list:
						flattened_attrs.append(attr)
				constr_str = "_".join(flattened_attrs)
				self.write_to_csv(dataset_name + "_" + constr_str + "_" + str(i) + ".csv", data_points, legend)
				i += 1
				


if __name__ == "__main__":
	simulator = Simulator("datasets/dirty_hospital_small.csv")
	constr1 = BooleanConstraint(["zip"], "le")
	constr2 = BooleanConstraint(["phone"], "ge")
	constr3 = BooleanConstraint([], "none")
	constraints = [[constr1, constr2, constr3]]
	simulator.run([("datasets/dirty_hospital_small.csv", constraints)])    




 
