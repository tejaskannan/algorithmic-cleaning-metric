from constraints.operations import Operations

class BooleanConstraint:

	RANGE_OPS = ['le', 'leq', 'ge', 'geq']

	# Operation is in ['eq', 'neq', 'le', 'leq', 'ge', 'geq', 'none']
	def __init__(self, attrs, operation_name):
		self.attrs = attrs
		self.operation_name = operation_name
		self.operation = Operations().get_operation(operation_name)

	# Returns True if the constraint is upheld, False if violated.
	# True generally means error while False means no error
	# Input rows are named tuples given by output of DataFrame iterator.
	def evaluate(self, row1_tuple, row2_tuple):
		if len(self.attrs) == 0:
			return True

		for attr in self.attrs:
			if not self.operation(row1_tuple.loc[attr], row2_tuple.loc[attr]):
				return False
		return True

	def get_attrs(self):
		return self.attrs

	def get_num_attr(self):
		return len(self.get_attrs())

	def get_operation_name(self):
		return self.operation_name

	def is_equals(self):
		return self.get_operation_name() == "eq"

	def is_range(self):
		return self.get_operation_name() in self.RANGE_OPS

	def should_sort_ascending(self):
		return self.get_operation_name() == "ge" or self.get_operation_name() == "geq"

	def __repr__(self):
		return "_".join(self.get_attrs())
