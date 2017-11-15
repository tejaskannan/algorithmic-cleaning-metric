
class BooleanConstraint:

	def __init__(self, input_attr, output_attr):
		self.input_attr = input_attr
		self.output_attr = output_attr

	# Returns True if the constraint is upheld, False if violated.
	# Tests whether f_1(<row1_inputs>, <row2_inputs>) => f_2(<row1_outputs>, <row2_outputs>)
	# The functions f_1 and f_2 are defined in this evaluate routine.
	# Input rows are named tuples given by output of DataFrame iterator.
	def evaluate(self, row1_tuple, row2_tuple):
		pass

	def get_input_attr(self):
		return self.input_attr

	def get_output_attr(self):
		return self.output_attr

	def get_num_input_attr(self):
		return len(self.get_input_attr())

	def get_num_output_attr(self):
		return len(self.get_output_attr())
