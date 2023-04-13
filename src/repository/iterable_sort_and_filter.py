class Data:
    def __init__(self):
        self._data = []

    def __iter__(self):
        return Iterator(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, item):
        self._data[key] = item

    def __delitem__(self, key):
        del self._data[key]

    def __len__(self):
        return len(self._data)

    def clear(self):
        self._data.clear()

    def pop(self):
        self._data.pop()

    def append(self, value):
        self._data.append(value)

    def remove(self, value):
        self._data.remove(value)

    def list(self):
        return list(self._data)


class Iterator:
    def __init__(self, col):
        self._collection = col
        self._iter = iter(self._collection)

    def __next__(self):
        return next(self._iter)


class CombSort:

    @staticmethod
    def compare_id_increasing(a, b):
        if a.id > b.id:
            return 1
        return 0

    @staticmethod
    def compare_grade_decreasing(a, b):
        if a.get_grade_value < b.get_grade_value:
            return True
        return False

    @staticmethod
    def compare_grade_increasing(a, b):
        if a.get_grade_value > b.get_grade_value:
            return 1
        return 0

    @staticmethod
    def compare_id_decreasing(a, b):
        if a.id < b.id:
            return True
        return False

    @staticmethod
    def compare_name_increasing(a, b):
        if a.name > b.name:
            return True
        return False

    @staticmethod
    def compare_name_decreasing(a, b):
        if a.name < b.name:
            return True
        return False

    @staticmethod
    def get_gap(n):
        n = (n * 10) // 13  # The shrink factor is 1.3 ( the ideal shrink factor)
        return n

    @staticmethod
    def comb_sort(library, function):
        '''
        The comb sort is a sorting algorithm based on bubble sort
        It is more efficient than bubble sort because it eliminates the "turtles", the small values near the end of
        the list.
        The "rabbits", large values around the beginning of the list, do not matter in bubble sort.
        :param library:
        :param function:
        :return:
        '''
        n = len(library)
        gap = n  # At first the gap is n, then it starts to shrink
        done = False  # Checks if the sorting is done
        while not done:
            # We execute while the gap is bigger than 1 or we no longer invert values
            gap = CombSort.get_gap(gap)
            if gap <= 1:
                done = True  # the sort finishes once the gap gets to one or lower
                gap = 1
            for i in range(0, n - gap):
                if function(library[i], library[i + gap]):
                    # If the comparison returns as True then we invert the values
                    library[i], library[i + gap] = library[i + gap], library[i]
                    done = False


class FilterList:
    @staticmethod
    def filter_by_name(a, filter_param):
        if filter_param.lower() in a.name.lower():
            return True
        return False

    @staticmethod
    def filter_by_id_greater_than(a, filter_param):
        if a.id > filter_param:
            return True
        return False

    @staticmethod
    def filter_by_id_smaller_than(a, filter_param):
        if a.id < filter_param:
            return True
        return False

    @staticmethod
    def filter_by_id_equal_to(a, filter_param):
        if a.id == filter_param:
            return True
        return False

    @staticmethod
    def filter_by_grade_greater_than(a, filter_param):
        if a.get_grade_value > filter_param:
            return True
        return False

    @staticmethod
    def filter_by_grade_smaller_than(a, filter_param):
        if a.get_grade_value < filter_param:
            return True
        return False

    @staticmethod
    def filter_by_grade_equal_to(a, filter_param):
        if a.get_grade_value == filter_param:
            return True
        return False

    @staticmethod
    def filter(library, function, filter_param):
        intermediate = Data()
        for item in library:
            if function(item, filter_param):
                intermediate.append(item)

        library.clear()

        for item in intermediate:
            library.append(item)

