from constraints.boolean_constraint import BooleanConstraint

class FunctionalDependency(BooleanConstraint):

	def __init__(self, input_attr, output_attr):
		super(FunctionalDependency, self).__init__(input_attr, output_attr)

	# Implementation of a functional dependency as a subclass of general boolean constraints
	def evaluate(self, row1_tuple, row2_tuple):
		for attr in self.input_attr:
			if row1_tuple.loc[attr] != row2_tuple.loc[attr]:
				return True

		for attr in self.output_attr:
			if row1_tuple.loc[attr] != row2_tuple.loc[attr]:
				return False
		return True

