class StudentManagementException(Exception):
    pass


class StudentExceptions(StudentManagementException):
    pass


class DisciplineExceptions(StudentManagementException):
    pass


class GradeExceptions(StudentManagementException):
    pass


class StudentValidator:
    @staticmethod
    def validate(student):
        '''
        Function that validates a student
        :param student:
        :return:
        '''
        if type(student.id) != int:
            raise StudentExceptions("The id has to be a number!")
        if student.id < 1:
            raise StudentExceptions("The id cannot be less than one!")


class DisciplineValidator:
    @staticmethod
    def validate(discipline):
        '''
        Function that validates a discipline
        :param discipline:
        :return:
        '''
        if type(discipline.id) != int:
            raise DisciplineExceptions("The id has to be a number!")
        if discipline.id < 1:
            raise DisciplineExceptions("The id cannot be less than one!")


class GradeValidator:
    @staticmethod
    def validate(grade):
        '''
        Function that validates a grade
        :param grade:
        :return:
        '''
        if type(grade.get_student_id) != int:
            raise GradeExceptions("The id has to be a number!")
        if grade.get_student_id < 1:
            raise GradeExceptions("The id cannot be less than one!")

        if type(grade.get_discipline_id) != int:
            raise GradeExceptions("The id has to be a number!")
        if grade.get_discipline_id < 1:
            raise GradeExceptions("The id cannot be less than one!")

        if type(grade.get_grade_value) != int:
            raise GradeExceptions("The grade has to be a number!")
        if grade.get_grade_value not in range(1, 11):
            raise GradeExceptions("The grade has to be a number between 1 and 10!")
