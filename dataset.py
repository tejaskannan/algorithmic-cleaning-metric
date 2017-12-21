import csv
import pandas as pd

class Dataset:
	
	def __init__(self, file_name, dataset=None, use_dataset=False):
		assert (file_name != None and len(file_name) > 0) or (use_dataset == True)

		if use_dataset == True:
			self.dataset = dataset
			self.columns = list(dataset.columns)
			return

		self.columns = []
		data = {}
		with open(file_name, 'r') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=",", quotechar="|")
			is_header = True
			for record in csv_reader:
				for index in range(0, len(record)):
					entry = record[index]
					if is_header:
						self.columns.append(entry)
						data[entry] = []
					else:
						column = self.columns[index]
						data[column].append(entry)
				is_header = False
		self.dataset = pd.DataFrame(data=data)

	def __iter__(self):
		return self.dataset.iterrows()

	def __len__(self):
		return len(self.dataset)

	def get_random_sample(self, fraction, weights=None):
		if weights is None:
			return self.dataset.sample(frac=fraction)
		return self.dataset.sample(frac=fraction, weights=weights)

	def get_column_index(self, column_name):
		index = self.columns.index(column_name)
		if index > -1:
			return index + 1
		return index

	def sort_values(self, attrs, asc=True):
		return self.dataset.sort_values(attrs, ascending=asc)

	def group_by(self, input_attrs):
		return self.dataset.groupby(input_attrs)

	def get_num_rows(self):
		return self.dataset.shape[0]

	def weight_by_groups(self, input_attrs):
		return self.group_by(input_attrs)[input_attrs[0]].transform('count')


			
