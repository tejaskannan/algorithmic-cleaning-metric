from detectors.cache_detector import CacheDetector
from dataset import Dataset
import random

class RandomCacheDetector(CacheDetector):

	def __init__(self, dataset, constraints, cache_size):
		super(RandomCacheDetector, self).__init__(dataset, constraints, cache_size)

	def remove_element_from_cache(self):
		index_to_remove = random.randint(0, self.cache_size - 1)
		key_to_remove = list(self.constraint_cache.keys())[index_to_remove]
		del self.constraint_cache[key_to_remove]

