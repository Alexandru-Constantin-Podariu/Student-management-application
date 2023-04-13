from src.domain.domain import Grade, AverageGrade, AverageDisciplineGrade
from src.repository.iterable_sort_and_filter import FilterList, CombSort
import random
import copy

class GradeServices:
    def __init__(self, repository, students_repository, disciplines_repository, validator_class):
        self._repository = repository
        self._students_repository = students_repository
        self._disciplines_repository = disciplines_repository
        self._undo_redo_student_grades_list = []
        self._undo_redo_discipline_grades_list = []
        self._validator_class = validator_class

    def add_grade(self, id, student_id, discipline_id, value):
        x = Grade(id, student_id, discipline_id, value)
        self._validator_class.validate(x)
        self._repository.add(x)

    def list_grades(self):
        return self._repository.get_all()

    def delete_grade(self, del_id):
        print(del_id)
        self._repository.delete_by_id(del_id)

    def save_student_grades_for_undo_redo(self, student_id):
        for x in self._repository._entities:
            if int(x.get_student_id) == int(student_id):
                self._undo_redo_student_grades_list.append(x)

    def put_back_student_grades(self, student_id):
        for x in self._undo_redo_student_grades_list:
            if int(x.get_student_id) == int(student_id):
                self._repository.add(x)
        self._undo_redo_student_grades_list.clear()

    def delete_grades_student(self, id):
        temporary_list = []

        for x in self._repository._entities:
            if int(x.get_student_id) != int(id):
                temporary_list.append(x)

        self._repository._entities.clear()

        for x in temporary_list:
            self._repository.add(x)

    def delete_grades_discipline(self, id):
        temporary = []
        for x in self._repository._entities:
            if int(x.get_discipline_id) != int(id):
                temporary.append(x)

        self._repository._entities.clear()

        for x in temporary:
            self._repository.add(x)

    def save_discipline_grades_for_undo_redo(self, discipline_id):
        for x in self._repository._entities:
            if int(x.get_discipline_id) == int(discipline_id):
                self._undo_redo_discipline_grades_list.append(x)

    def put_back_discipline_grades(self, discipline_id):
        for x in self._undo_redo_discipline_grades_list:
            if int(x.get_discipline_id) == int(discipline_id):
                self._repository.add(x)
        self._undo_redo_discipline_grades_list.clear()

    def average_grades(self):  # related to Statistics
        grades = self._repository.get_all()
        students = self._students_repository.get_all()
        disciplines = self._disciplines_repository.get_all()
        average_discipline_grades = []

        for student in students:
            for discipline in disciplines:
                s = 0
                n = 0
                for grade in grades:
                    if grade._student_id == student._id and grade._discipline_id == discipline._id:
                        s += int(grade._value)
                        n += 1
                if s > 0 and n > 0:
                    average = s / n
                    x = AverageDisciplineGrade(student._id, student._name, discipline._id, discipline._name, average)
                    average_discipline_grades.append(x)
        return average_discipline_grades

    def failing_students(self):  # related to Statistics
        average_grades = self.average_grades()
        failing = []
        for x in average_grades:
            if x.get_grade_value < 5:
                failing.append(x)
        return failing

    def sort_best_grades(self, grades):  # related to Statistics

        for x in range(0, len(grades)):
            for y in range(x + 1, len(grades)):
                if grades[x].get_grade_value < grades[y].get_grade_value:
                    aux = grades[x]
                    grades[x] = grades[y]
                    grades[y] = aux

    def best_student_averages(self):  # related to Statistics
        average_discipline_grades = self.average_grades()
        students = self._students_repository.get_all()
        best_grades = []

        for student in students:
            s = 0
            n = 0
            for grade in average_discipline_grades:
                if grade.get_student_id == student._id:
                    s += grade.get_grade_value
                    n += 1
            if s > 0 and n > 0:
                average = s / n
                x = AverageGrade(student._id, student._name, average)
                best_grades.append(x)

        self.sort_best_grades(best_grades)
        return best_grades

    def discipline_average_grades(self):  # related to Statistics
        average_discipline_grades = self.average_grades()
        disciplines = self._disciplines_repository.get_all()
        best_grades = []

        for discipline in disciplines:
            s = 0
            n = 0
            for grade in average_discipline_grades:
                if grade.get_discipline_id == discipline._id:
                    s += grade.get_grade_value
                    n += 1
            if s > 0 and n > 0:
                average = s / n
                x = AverageGrade(discipline._id, discipline._name, average)
                best_grades.append(x)

        self.sort_best_grades(best_grades)
        return best_grades

    def generate_grades(self):
        i = 0
        while i < 20:
            student = random.randint(1, 20)
            discipline = random.randint(1, 17)
            grade = random.randint(1, 10)
            self.add_grade(i, student, discipline, grade)
            i += 1

    def filter_grades(self, type, params):
        Filter = FilterList
        keep_list = copy.deepcopy(self._repository._entities)

        if type == 1:
            Filter.filter(keep_list, Filter.filter_by_grade_greater_than, params)
        elif type == 2:
            Filter.filter(keep_list,  Filter.filter_by_grade_smaller_than, params)
        else:
            Filter.filter(keep_list, Filter.filter_by_grade_equal_to, params)

        return keep_list

    def sort_grades(self, mode):
        Sort = CombSort
        keep_list = copy.deepcopy(self._repository._entities)
        if mode == 1:
            Sort.comb_sort(keep_list, Sort.compare_grade_increasing)
        elif mode == 2:
            Sort.comb_sort(keep_list, Sort.compare_grade_decreasing)

        return keep_list