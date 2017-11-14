from detectors.random_sample import RandomSampleDetector

class WeightedSampleDetector(RandomSampleDetector):
	
	def __init__(self, dataset, constraints, fraction, rep_count, use_inputs=True):
		super(WeightedSampleDetector, self).__init__(dataset, constraints, fraction, rep_count)
		self.use_inputs = use_inputs

	# Returns a series of weights that correspond to the size of the grouping a record lives in. The group size is
	# tied to the functional dependency that has the largest input set (ties broken by first one seen)
	def get_weights(self):
		most_input_attributes = self.get_constraint_with_most(self.use_inputs).get_input_attr()	
		return self.dataset.weight_by_groups(most_input_attributes)

	def get_constraint_with_most(self, use_inputs):
		max_constraint = self.constraints[0]
		for i in range(1, len(self.constraints)):
			if (use_inputs and max_constraint.get_num_input_attr() < self.constraints[i].get_num_input_attr()) or \
			   (not use_inputs and max_constraint.get_num_output_attr() < self.constraints[i].get_num_output_attr()):
				max_constraint = self.constraints[i]
		return max_constraint 
		
