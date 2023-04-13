from src.domain.domain import Discipline
from src.repository.iterable_sort_and_filter import FilterList, CombSort
import random
import copy


class DisciplineServices:
    def __init__(self, repository, validator_class):
        self._repository = repository
        self._validator_class = validator_class

    def add_discipline(self, id, name):
        '''
        Function that adds a discipline to the dictionary
        :param id: The id of the discipline
        :param name: The name of the discipline
        :return:
        '''
        x = Discipline(id, name)
        self._validator_class.validate(x)
        self._repository.add(x)

    def list_disciplines(self):
        '''
        Function that returns the list all of the disciplines
        :return: List of disciplines
        '''
        return self._repository.get_all()

    def delete_discipline(self, id):
        '''
        Function that deletes a discipline based on its id
        :param id: The id of the discipline
        :return:
        '''
        self._repository.delete_by_id(id)

    def update_discipline_name(self, id, new_name):
        '''
        Functio that updates a discipline based on its id
        :param id: The id of the discipline
        :param new_name: The new name of the discipline
        :return:
        '''
        self._repository.update_name(id, new_name)

    def check_discipline_id(self, id):
        '''
        Function that checks that an id is not used
        :param id: The id of the discipline
        :return: True if the id is not used, False otherwise
        '''
        if self._repository.find_by_id(id) is not None:
            return True
        return False

    def generate_disciplines(self):
        '''
        Function that programmatically generates the disciplines in the dictionary
        :return:
        '''
        names = [" ", "Mathematical Analysis", "Algebra", "Fundamentals of Programming", "Logic",
                 "Advanced Methods of Programming","Computer systems architecture", "Sport",
                 "Communication and professional development","Fundamentals of entrepreneurship",
                 "Educational Psychology", "Tutoring", "Operating Systems", "Object Oriented Programming",
                 "Data Structures and Algorithms", "Geometry", "Dynamic Systems", "Graphs"]

        for i in range(1, 18):
                x = Discipline(i, names[i])
                self._repository.add(x)

    def search_discipline_by_name(self, string):
        return self._repository.search_by_name(string)

    def search_discipline_by_id(self, string):
        return self._repository.search_by_id(string)

    def get_discipline(self, id):
        return self._repository.find_by_id(id)

    def filter_disciplines(self, type, params):
        Filter = FilterList
        keep_list = copy.deepcopy(self._repository._entities)
        if type == 1:
            Filter.filter(keep_list, Filter.filter_by_name, params)
        elif type == 2:
            Filter.filter(keep_list, Filter.filter_by_id_greater_than, params)
        elif type == 3:
            Filter.filter(keep_list, Filter.filter_by_id_smaller_than, params)
        else:
            Filter.filter(keep_list, Filter.filter_by_id_equal_to, params)
        return keep_list

    def sort_disciplines(self, mode):
        Sort = CombSort
        keep_list = copy.deepcopy(self._repository._entities)
        print(keep_list[1].name)
        if mode == 1:
            Sort.comb_sort(keep_list, Sort.compare_name_increasing)
        elif mode == 2:
            Sort.comb_sort(keep_list, Sort.compare_name_decreasing)
        elif mode == 3:
            Sort.comb_sort(keep_list, Sort.compare_id_increasing)
        else:
            Sort.comb_sort(keep_list, Sort.compare_id_decreasing)

        return keep_list
