class Operations:

	OPS = {
		'eq': lambda r1, r2: r1 == r2,
		'neq': lambda r1, r2: r1 != r2,
		'le': lambda r1, r2: r1 < r2,
		'leq': lambda r1, r2: r1 <= r2,
		'ge': lambda r1, r2: r1 > r2,
		'geq': lambda r1, r2: r1 >= r2,
		'none': lambda r1, r2: False
	}

	def get_operation(self, operation_name):
		return self.OPS[operation_name]
