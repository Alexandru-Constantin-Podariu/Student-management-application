class Student:
    def __init__(self, student_id, name):
        self._id = student_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def set_id(self, st_id):
        self._id = st_id

    def set_name(self, name):
        self._name = name


class Discipline:
    def __init__(self, discipline_id, name):
        self._id = discipline_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def set_id(self, d_id):
        self._id = d_id

    def set_name(self, name):
        self._name = name


class Grade:
    def __init__(self, id, student_id, discipline_id, grade_value):
        self._id = id
        self._student_id = student_id
        self._discipline_id = discipline_id
        self._value = grade_value

    @property
    def get_id(self):
        return self._id

    @property
    def get_discipline_id(self):
        return self._discipline_id

    @property
    def get_student_id(self):
        return self._student_id

    @property
    def get_grade_value(self):
        return self._value

    def value(self, value):
        self._value = value

    def student_id(self, id):
        self._student_id = id

    def discipline_id(self, id):
        self._discipline_id = id

    def id(self, id):
        self._id = id


class AverageDisciplineGrade: # related to Statistics
    def __init__(self, student_id, student_name, discipline_id, discipline_name, average_grade):
        self._student_id = student_id
        self._student_name = student_name
        self._discipline_id = discipline_id
        self._discipline_name = discipline_name
        self._value = average_grade

    @property
    def get_discipline_id(self):
        return self._discipline_id

    @property
    def get_discipline_name(self):
        return self._discipline_name

    @property
    def get_student_id(self):
        return self._student_id

    @property
    def get_student_name(self):
        return self._student_name

    @property
    def get_grade_value(self):
        return self._value

    def value(self, value):
        self._value = value

    def student_id(self, id):
        self._student_id = id

    def student_name(self, name):
        self._student_name = name

    def discipline_id(self, id):
        self._discipline_id = id

    def discipline_name(self, name):
        self._discipline_name = name


class AverageGrade: # related to Statistics
    def __init__(self, id, name, average_grade):
        self._id = id
        self._name = name
        self._value = average_grade

    @property
    def get_id(self):
        return self._id

    @property
    def get_name(self):
        return self._name

    @property
    def get_grade_value(self):
        return self._value

    def value(self, value):
        self._value = value

    def id(self, id):
        self._id = id

    def name(self, name):
        self._name = name


