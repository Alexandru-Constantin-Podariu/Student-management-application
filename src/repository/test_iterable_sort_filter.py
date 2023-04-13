from iterable_sort_and_filter import CombSort, FilterList, Data
from src.domain.domain import Student, Grade
import unittest


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    @staticmethod
    def test_initialize():
        items = []
        items.append(Student(3, "Ana Boimler"))
        items.append(Student(5, "Elaine Warlock"))
        items.append(Student(6, "George Seinfeld"))
        items.append(Student(9, "Jimmy Blue"))
        items.append(Student(2, "John Snow"))
        items.append(Student(10, "Chris Griffin"))
        return items

    @staticmethod
    def test_initialize_grades():
        items = []
        items.append(Grade(1, 1, 3, 5))
        items.append(Grade(21, 51, 3, 9))
        items.append(Grade(13, 1, 53, 2))
        items.append(Grade(15, 31, 3, 3))
        items.append(Grade(31, 1, 63, 7))
        return items

    def test_sort_id_increasing(self):
        items = Tests.test_initialize()
        Sort = CombSort
        Sort.comb_sort( items, Sort.compare_id_increasing)
        for x in range (1, len(items)):
            self.assertGreaterEqual(items[x].id, items[x-1].id)

    def test_sort_id_decreasing(self):
        items = Tests.test_initialize()
        Sort = CombSort
        Sort.comb_sort( items, Sort.compare_id_decreasing)
        for x in range(0, len(items)):
            print(items[x].id)
        for x in range (1, len(items)):
            self.assertGreaterEqual(items[x-1].id, items[x].id)

    def test_sort_name_increasing(self):
        items = Tests.test_initialize()
        Sort = CombSort
        Sort.comb_sort( items, Sort.compare_name_increasing)
        for x in range (1, len(items)):
            self.assertGreaterEqual(items[x].name, items[x-1].name)

    def test_sort_name_decreasing(self):
        items = Tests.test_initialize()
        Sort = CombSort
        Sort.comb_sort( items, Sort.compare_name_decreasing)
        for x in range (1, len(items)):
            self.assertGreaterEqual(items[x-1].name, items[x].name)

    def test_filter_name(self):
        items = Tests.test_initialize()
        Filter = FilterList
        Filter.filter( items, Filter.filter_by_name, "ana")
        for x in range(0, len(items)):
            self.assertIn("ana", items[x].name.lower())

    def test_filter_id_greater_than(self):
        items = Tests.test_initialize()
        Filter = FilterList
        Filter.filter( items, Filter.filter_by_id_greater_than, 3)
        for x in range(0, len(items)):
            self.assertGreater(items[x].id, 3)

    def test_filter_id_smaller_than(self):
        items = Tests.test_initialize()
        Filter = FilterList
        Filter.filter( items, Filter.filter_by_id_smaller_than, 9)
        for x in range(0, len(items)):
            self.assertLess(items[x].id, 9)

    def test_filter_id_equal_to(self):
        items = Tests.test_initialize()
        Filter = FilterList
        Filter.filter(items, Filter.filter_by_id_equal_to, 9)
        for x in range(0, len(items)):
            self.assertEqual(items[x].id, 9)

    def test_filter_grade_greater_than(self):
        items = Tests.test_initialize_grades()
        Filter = FilterList
        Filter.filter( items, Filter.filter_by_grade_greater_than, 6)
        for x in range(0, len(items)):
            self.assertGreater(items[x].get_grade_value, 6)

    def test_filter_grade_smaller_than(self):
        items = Tests.test_initialize_grades()
        Filter = FilterList
        Filter.filter( items, Filter.filter_by_grade_smaller_than, 8)
        for x in range(0, len(items)):
            self.assertLess(items[x].get_grade_value, 8)

    def test_filter_grade_equal_to(self):
        items = Tests.test_initialize_grades()
        Filter = FilterList
        Filter.filter(items, Filter.filter_by_grade_equal_to, 9)
        for x in range(0, len(items)):
            self.assertEqual(items[x].get_grade_value, 9)

    def test_sort_grade_increasing(self):
        items = Tests.test_initialize_grades()
        Sort = CombSort
        Sort.comb_sort(items, Sort.compare_grade_increasing)
        for x in range(1, len(items)):
            self.assertGreaterEqual(items[x].get_grade_value, items[x - 1].get_grade_value)

    def test_sort_grade_decreasing(self):
        items = Tests.test_initialize_grades()
        Sort = CombSort
        Sort.comb_sort(items, Sort.compare_grade_decreasing)
        for x in range(1, len(items)):
            self.assertGreaterEqual(items[x - 1].get_grade_value, items[x].get_grade_value)


    def test_iterable_structure(self):
        items = Data()
        items.append(0)
        items[0] = Student(3, "Ana")
        self.assertEqual(items[0].name, "Ana")
        x = Student(2, "Lorena")
        items.append(x)
        items.append(Student(3, "John"))
        items.append(Student(4, "Andrew"))
        self.assertEqual(len(items.list()), 4)
        del items[3]
        self.assertEqual(len(items), 3)

        items.pop()
        self.assertEqual(len(items), 2)
        c = 0
        for x in items:
            c += 1
        self.assertEqual(c, 2)
        items.remove(x)
        self.assertEqual(len(items), 1)

        items.clear()
        self.assertEqual(len(items), 0)

