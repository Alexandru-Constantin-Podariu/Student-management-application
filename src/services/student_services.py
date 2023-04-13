import copy

from src.domain.domain import Student
from src.repository.iterable_sort_and_filter import FilterList, CombSort
import random


class Student_services:
    def __init__(self, repository, validator_class):
        self._validator_class = validator_class
        self._repository = repository

    def add_student(self, id, name):
        '''
        Function that adds a student to the repository
        :param id: The id of the student
        :param name: T~he name of the student
        :return:
        '''
        x = Student(id, name)
        self._validator_class.validate(x)
        self._repository.add(x)

    def list_students(self):
        '''
        Function that returns a list all the students
        :return: List of students
        '''
        return self._repository.get_all()

    def delete_student(self, id):
        '''
        Function that deletes a students based on its id
        :param id: The id of the student to delete
        :return:
        '''
        print(id)
        self._repository.delete_by_id(id)

    def update_student_name(self, id, new_name):
        '''
        Function that updates the name of a student based on its id
        :param id: The id of the student
        :param new_name:
        :return:
        '''
        self._repository.update_name(id, new_name)

    def check_student_id(self, id):
        '''
        Function that check that an id is not used
        :param id: The id of the student
        :return: True if the id is not used, False otherwise
        '''
        if self._repository.find_by_id(id) is not None:
            return True
        return False

    def generate_students(self):
        '''
        Function that programmatically generates the students in the dictionary
        :return:
        '''
        for i in range (1, 21):
            names = [" ", "Ana Flore", "Ana Popescu", "Diana Pop", "Andrei Comali", "Ion Costin", "Alex Bridger",
                     "Paul Walk", "Paul Novaki", "John Snow", "Luke Skywalker", "Darth Vader", "Leia Organa",
                     "Corina Costin", "Johnny Green", "Emilia Castelletto", "Kelly Piquet", "Phil Dunphy"]
            gen = random.randint(1, 17)
            name = names[gen]
            if self._repository.find_by_id(i) is None:
                x = Student(i, name)
                self._repository.add(x)

    def search_student_by_name(self, string):
        return self._repository.search_by_name(string)

    def search_student_by_id(self, string):
        return self._repository.search_by_id(string)

    def get_student(self, id):
        return self._repository.find_by_id(id)

    def filter_students(self, type, params):
        Filter = FilterList
        keep_list = copy.deepcopy(self._repository._entities)
        if type == 1:
            Filter.filter(keep_list, Filter.filter_by_name, params)
        elif type == 2:
            Filter.filter(keep_list, Filter.filter_by_id_greater_than, params)
        elif type == 3:
            Filter.filter(keep_list, Filter.filter_by_id_smaller_than, params)
        else:
            Filter.filter(keep_list,  Filter.filter_by_id_equal_to, params)

        return keep_list

    def sort_students(self, mode):
        Sort = CombSort
        keep_list = copy.deepcopy(self._repository._entities)
        if mode == 1:
            Sort.comb_sort(keep_list, Sort.compare_name_increasing)
        elif mode == 2:
            Sort.comb_sort(keep_list, Sort.compare_name_decreasing)
        elif mode == 3:
            Sort.comb_sort(keep_list, Sort.compare_id_increasing)
        else:
            Sort.comb_sort(keep_list, Sort.compare_id_decreasing)

        return keep_list