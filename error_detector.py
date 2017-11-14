import numpy as np
import random

class ErrorDetector:

    def __init__(self, precision, recall, data, labels):
        assert len(data) == len(labels)

        self.precision = precision
        self.recall = recall
        self.data = data
        self.labels = labels

        n = len(data)
        func_map = {}
        count_map = {}
        for i in range(0, n):
            assert labels[i] == 0 or labels[i] == 1

            # The function key maps the data row to a clean/dirty value
            key = ",".join([str(x) for x in data[i]])
            if key not in count_map:
                count_map[key] = 0

            if key in func_map:
                assert func_map[key] == labels[i]

            # Set the count and function maps
            func_map[key] = labels[i]
            count_map[key] += 1

        # Find all inputs marked dirty and clean. The cleaning function is well-defined, so this
        # list does not double count
        true_dirty = []
        true_clean = []
        true_dirty_count = 0
        true_clean_count = 0
        for key in func_map:
            if func_map[key] == 1:
                true_dirty.append((key, 1, count_map[key]))
                true_dirty_count += count_map[key]
            else:
                true_clean.append((key, 0, count_map[key]))
                true_clean_count += count_map[key]

        # Ensure the recall is the specified percetage
        recall_number = true_dirty_count - recall * true_dirty_count
        recall_left = self.mark_random_sample_close_to_size(true_dirty, recall_number, func_map)

        dirty_count = true_dirty_count - (recall_number - recall_left)
        self.recall = dirty_count / true_dirty_count
        print("Actual Recall: %s" % self.recall)

        precision_count = round(((1 - precision) / precision) * dirty_count, 0)
        precision_left = self.mark_random_sample_close_to_size(true_clean, precision_count, func_map)

        self.precision = dirty_count / (dirty_count + (precision_count - precision_left))
        print("Actual Precision: %s" % self.precision)
        
        self.dirty_count = dirty_count + precision_count - precision_left
        self.function = func_map

    def is_dirty(self, record):
        record_str = ",".join([str(x) for x  in record])
        return self.function[record_str]

    def mark_random_sample_close_to_size(self, data, size, func_map):
        data_copy = [entity for entity in data]
        while size > 0 and len(data_copy) > 0:
            index = random.randint(0, len(data_copy) - 1)
            key, label, count = data_copy[index]
            if size >= count:
                func_map[key] = label == 0 if 1 else 0
                size -= count
            del data_copy[index]
        return size


