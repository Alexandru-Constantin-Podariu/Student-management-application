import unittest

from src.domain.domain import Student, Discipline, Grade, AverageGrade, AverageDisciplineGrade
from src.domain.Exceptions import *
from src.services.student_services import Student_services
from src.services.discipline_services import DisciplineServices
from src.services.grade_services import GradeServices
from src.repository.repository import Repository, RepositoryException
from src.domain.Exceptions import *
from src.services.handlers import *
from src.services.undo_redo import *
import random


class ServicesTest(unittest.TestCase):
    def setUp(self):
        self._studentValidator = StudentValidator
        self._student_repository = Repository()
        self._student_service = Student_services(self._student_repository, self._studentValidator)

        self._disciplineValidator = DisciplineValidator
        self._discipline_repository = Repository()
        self._discipline_service = DisciplineServices(self._discipline_repository, self._disciplineValidator)

        self._gradeValidator = GradeValidator
        self._grade_repository = Repository()
        self._grade_service = GradeServices(self._grade_repository, self._student_repository,
                                            self._discipline_repository, self._gradeValidator)

    def tearDown(self) -> None:
        pass

# Student Tests

    def test_Students_add_setup_and_get(self):
        x = Student(1, "Ana Roman")
        self._student_repository.add(x)
        self.assertEqual(len(self._student_repository._entities), 1)
        self.assertEqual(self._student_repository.find_by_id(1).name, "Ana Roman")
        self.assertEqual(self._student_repository.find_by_id(1), x)

        # Add test
        self._student_service.add_student(3, "Ana Boimler")
        x = Student(5, "Elaine Warlock")
        self._student_repository.add(x)
        x = Student(5, "Elaine Warlock")
        with self.assertRaises(Exception):
            self._student_repository.add(x)
        self._student_service.add_student(6, "George Seinfeld")
        self._student_service.add_student(9, "Jimmy Blue")
        self._student_service.add_student(2, "John Snow")
        self._student_service.add_student(10, "Chris Griffin")
        self.assertEqual(self._student_repository.find_by_id(3).name, "Ana Boimler")
        self.assertEqual(self._student_repository.find_by_id(5).name, "Elaine Warlock")
        x = self._student_service.get_student(10)
        self.assertEqual(x.name, "Chris Griffin")
        self.assertNotEqual(x.name, "John Snow")

    def test_Student_setters(self):
        x = Student(9, "Simona Ligia")

        x.set_id(10)
        self.assertEqual(x.id, 10)

        x.set_name("Ion Cristian")
        self.assertEqual(x.name, "Ion Cristian")

    def test_Student_validator(self):
        validator = StudentValidator
        x = Student(9, "Simona Ligia")
        x.set_id(-1)
        with self.assertRaises(Exception):
            validator.validate(x)

        x.set_id("cha cha")
        with self.assertRaises(Exception):
            validator.validate(x)

    def test_Student_list_checkid(self):

        self.test_Students_add_setup_and_get()
        # List tests
        self.assertEqual(len(self._student_service.list_students()), 7)
        self.assertEqual(len(self._student_repository.get_all()), 7)

        # Check Id tests
        self.assertEqual(self._student_service.check_student_id(8), False)
        self.assertEqual(self._student_service.check_student_id(5), True)
        self.assertIsNotNone(self._student_repository.find_by_id(1))
        self.assertEqual(self._student_repository.find_by_id(11), None)

    def test_Student_update(self):
        self.test_Students_add_setup_and_get()
        # Update tests
        self._student_service.update_student_name(6, "Gordon Grey")
        self._student_service.update_student_name(1, "Tracy Monroe")
        self._student_repository.update_name(3, "Travis Dunes")
        with self.assertRaises(Exception):
            self._student_repository.update_name(88)
        self.assertEqual(self._student_repository.find_by_id(6).name, "Gordon Grey")
        self.assertEqual(self._student_repository.find_by_id(1).name, "Tracy Monroe")
        self.assertEqual(self._student_repository.find_by_id(3).name, "Travis Dunes")

    def test_Student_delete(self):
        self.test_Students_add_setup_and_get()
        # Delete Tests
        self._student_service.delete_student(6)
        self._student_service.delete_student(2)
        self._student_repository.delete_by_id(3)
        self.assertEqual(self._student_repository.find_by_id(6), None)
        self.assertEqual(self._student_repository.find_by_id(2), None)
        self.assertEqual(self._student_repository.find_by_id(3), None)

    def test_Student_search(self):
        self.test_Students_add_setup_and_get()
        # search tests
        self.assertEqual(len(self._student_repository.search_by_name("roen")), 0)
        self.assertEqual(len(self._student_service.search_student_by_name("boim")), 1)
        self.assertEqual(len(self._student_service.search_student_by_id("5")), 1)

    def test_Student_generate(self):
        # generate
        self._student_service.generate_students()
        self.assertEqual(len(self._student_repository._entities), 20)

    def test_Undo_Redo_add_student(self):
        self._student_service.add_student(27, "Ana Romana")
        UndoRedoManager.register_undo_operation(self._student_service, self._grade_service,UndoHandlers.ADD_STUDENT, 27, "Ana Romana")
        UndoRedoManager.undo()
        self.assertEqual(self._student_repository.find_by_id(27), None)
        UndoRedoManager.register_redo_operation(self._student_service, self._grade_service,  RedoHandlers.ADD_STUDENT, 27, "Ana Romana")
        UndoRedoManager.redo()
        self.assertNotEqual(self._student_repository.find_by_id(27), None)
        UndoRedoManager.undo()
        UndoRedoManager.redo()
        UndoRedoManager.undo()

    def test_Undo_Redo_delete_student(self):
        self.test_Students_add_setup_and_get()
        self._student_service.delete_student(10)

        UndoRedoManager.register_undo_operation(self._student_service, self._grade_service, UndoHandlers.DELETE_STUDENT, 10, "Chris Griffin")
        UndoRedoManager.undo()
        self.assertNotEqual(self._student_repository.find_by_id(10), None)

        UndoRedoManager.register_redo_operation(self._student_service, self._grade_service, RedoHandlers.DELETE_STUDENT, 10, "Chris Griffin")
        UndoRedoManager.redo()
        self.assertEqual(self._student_repository.find_by_id(10), None)
        UndoRedoManager.undo()
        UndoRedoManager.redo()
        UndoRedoManager.undo()

    def test_Undo_Redo_update_student(self):
        self.test_Students_add_setup_and_get()
        self._student_service.update_student_name(3, "Andreas Long")

        UndoRedoManager.register_undo_operation(self._student_service, self._grade_service, UndoHandlers.UPDATE_STUDENT, 3, "Chris Griffin", "Andreas Long")
        UndoRedoManager.undo()
        self.assertEqual(self._student_repository.find_by_id(3).name, "Chris Griffin")

        UndoRedoManager.register_redo_operation(self._student_service, self._grade_service, RedoHandlers.UPDATE_STUDENT, 3, "Chris Griffin", "Andreas Long")
        UndoRedoManager.redo()
        self.assertEqual(self._student_repository.find_by_id(3).name, "Andreas Long")
        UndoRedoManager.undo()
        UndoRedoManager.redo()
        UndoRedoManager.undo()


# Discipline Tests


    def test_Discipline_add_setup(self):
        # Add test
        self._discipline_service.add_discipline(33, "Math")
        x = Discipline(55, "Biology")
        self._discipline_repository.add(x)
        self._discipline_service.add_discipline(66, "Physics")
        self._discipline_service.add_discipline(111, "English")
        self._discipline_service.add_discipline(22, "Latin")
        self.assertEqual(self._discipline_repository.find_by_id(33).name, "Math")
        self.assertEqual(self._discipline_repository.find_by_id(55).name, "Biology")

    def test_Discipline_setters(self):
        x = Discipline(9, "Chemistry")

        x.set_id(78)
        self.assertEqual(x.id, 78)

        x.set_name("German")
        self.assertEqual(x.name, "German")

    def test_Discipline_validator(self):
        validator = DisciplineValidator
        x = Discipline(9, "Biology")
        x.set_id(-1)
        with self.assertRaises(Exception):
            validator.validate(x)

        x.set_id("cha cha")
        with self.assertRaises(Exception):
            validator.validate(x)

    def test_Discipline_list_checkId(self):
        self.test_Discipline_add_setup()
        # List tests
        self.assertEqual(len(self._discipline_service.list_disciplines()), 5)
        self.assertEqual(len(self._discipline_repository.get_all()), 5)

        # Check Id tests
        self.assertEqual(self._discipline_service.check_discipline_id(88), False)
        self.assertEqual(self._discipline_service.check_discipline_id(55), True)
        self.assertIsNotNone((self._discipline_repository.find_by_id(33)))
        self.assertIsNone((self._discipline_repository.find_by_id(99)))

    def test_Discipline_update(self):
        self.test_Discipline_add_setup()
        # Update tests
        self._discipline_service.update_discipline_name(66, "Economy")
        self._discipline_service.update_discipline_name(111, "Sport")
        self._discipline_repository.update_name(33, "Entrepreneurship")
        with self.assertRaises(Exception):
            self._discipline_repository.update_name(77, "Psychology")
        self.assertEqual(self._discipline_repository.find_by_id(66).name, "Economy")
        self.assertEqual(self._discipline_repository.find_by_id(111).name, "Sport")
        self.assertEqual(self._discipline_repository.find_by_id(33).name, "Entrepreneurship")

    def test_Discipline_delete(self):
        self.test_Discipline_add_setup()
        # Delete Tests
        self._discipline_service.delete_discipline(66)
        self._discipline_service.delete_discipline(22)
        self._discipline_repository.delete_by_id(33)
        with self.assertRaises(Exception):
            self._discipline_repository.delete_by_id(77)
        self.assertEqual(self._discipline_repository.find_by_id(66), None)
        self.assertEqual(self._discipline_repository.find_by_id(22), None)
        self.assertEqual(self._discipline_repository.find_by_id(33), None)

    def test_Discipline_generate(self):
        # Generate Tests
        self._discipline_service.generate_disciplines()
        self.assertEqual(len(self._discipline_repository._entities), 17)

    def test_Discipline_search(self):
        self._discipline_service.generate_disciplines()
        self.assertEqual(len(self._discipline_service.search_discipline_by_name("compute")), 1)
        self.assertEqual(len(self._discipline_service.search_discipline_by_name("bio")), 0)
        self.assertEqual(len(self._discipline_service.search_discipline_by_id("1")), 9)

    def test_Discipline_getter(self):
        self._discipline_service.generate_disciplines()
        x = self._discipline_service.get_discipline(17)
        self.assertEqual(x.name, "Graphs")
        x = self._discipline_service.get_discipline(13)
        self.assertNotEqual(x.name, "Biology")

    def test_Undo_Redo_add_discipline(self):
        self._discipline_service.add_discipline(27, "Biology")

        UndoRedoManager.register_undo_operation(self._discipline_service, self._grade_service, UndoHandlers.ADD_DISCIPLINE, 27, "Biology")
        UndoRedoManager.undo()
        self.assertEqual(self._discipline_repository.find_by_id(27), None)

        UndoRedoManager.register_redo_operation(self._discipline_service, self._grade_service, RedoHandlers.ADD_DISCIPLINE, 27, "Biology")
        UndoRedoManager.redo()
        self.assertNotEqual(self._discipline_repository.find_by_id(27), None)
        UndoRedoManager.undo()
        UndoRedoManager.redo()
        UndoRedoManager.undo()

    def test_Undo_Redo_delete_discipline(self):
        self.test_Discipline_add_setup()
        self._discipline_service.delete_discipline(33)

        UndoRedoManager.register_undo_operation(self._discipline_service, self._grade_service, UndoHandlers.DELETE_DISCIPLINE, 33, "Math")
        UndoRedoManager.undo()
        self.assertEqual(self._discipline_repository.find_by_id(33).name, "Math")

        UndoRedoManager.register_redo_operation(self._discipline_service, self._grade_service, RedoHandlers.DELETE_DISCIPLINE, 33, "Math")
        UndoRedoManager.redo()
        self.assertEqual(self._discipline_repository.find_by_id(33), None)
        UndoRedoManager.undo()
        UndoRedoManager.redo()
        UndoRedoManager.undo()

    def test_Undo_Redo_update_discipline(self):
        self.test_Discipline_add_setup()
        self._discipline_service.update_discipline_name(22, "French")

        UndoRedoManager.register_undo_operation(self._discipline_service, self._grade_service, UndoHandlers.UPDATE_DISCIPLINE, 22, "Latin", "French")
        UndoRedoManager.undo()
        self.assertEqual(self._discipline_repository.find_by_id(22).name, "Latin")

        UndoRedoManager.register_redo_operation(self._discipline_service, self._grade_service, RedoHandlers.UPDATE_DISCIPLINE, 22, "Latin", "French")
        UndoRedoManager.redo()
        self.assertEqual(self._discipline_repository.find_by_id(22).name, "French")
        UndoRedoManager.undo()
        UndoRedoManager.redo()
        UndoRedoManager.undo()

# Grade Tests

    def test_Grade_add_setup(self):
        # Add Tests
        self._grade_service.add_grade(1, 1, 3, 10)
        self.assertEqual(len(self._grade_repository._entities), 1)
        self._grade_service.add_grade(2, 6, 9, 5)
        self._grade_service.add_grade(3, 5, 7, 10)

    def test_Grade_setters_getters(self):
        x = Grade(9, 4, 3, 10)
        self.assertEqual(x.get_id, 9)

        x.id(10)
        self.assertEqual(x.get_id, 10)

        x.student_id(8)
        self.assertEqual(x.get_student_id, 8)

        x.discipline_id(5)
        self.assertEqual(x.get_discipline_id, 5)

        x.value(7)
        self.assertEqual(x.get_grade_value, 7)

    def test_Grade_list(self):
        self.test_Grade_add_setup()
        # List
        self.assertEqual(len(self._grade_service.list_grades()), 3)

    def test_Grade_delete(self):
        self.test_Grade_add_setup()
        # Delete Tests
        self._grade_service.delete_grades_student(1)
        self.assertEqual(len(self._grade_service.list_grades()), 2)

        self._grade_service.delete_grades_discipline(7)
        self.assertEqual(len(self._grade_service.list_grades()), 1)

    def test_Undo_Redo_Grade(self):
        self._grade_service.add_grade(1, 1, 3, 10)

        UndoRedoManager.register_undo_operation(self._grade_service, self._grade_service, UndoHandlers.ADD_GRADE, 1, 1, 3, 10)
        UndoRedoManager.undo()
        self.assertEqual(self._grade_repository.find_by_id(1), None)

        UndoRedoManager.register_redo_operation(self._grade_service, self._grade_service, RedoHandlers.ADD_GRADE, 1, 1, 3, 10)
        UndoRedoManager.redo()
        self.assertEqual(self._grade_repository.find_by_id(1).get_grade_value, 10)

    def test_statistics_setup(self):
        self.test_Student_generate()
        self.test_Discipline_generate()
        i = 1
        while i <= 20:
            student = random.randint(1, 20)
            discipline = random.randint(1, 17)
            grade = random.randint(1, 10)
            if self._student_service.check_student_id(student) and self._discipline_service.check_discipline_id(discipline):
                self._grade_service.add_grade(i, student, discipline, grade)
                i += 1

    def test_statistics_students(self):
        self.test_statistics_setup()
        self.assertEqual(len(self._grade_repository._entities), 20)
        self._grade_service.failing_students()
        self._grade_service.best_student_averages()
        self._grade_service.discipline_average_grades()

    def test_average_grade(self):
        x = AverageGrade(5, "Alex Thompson", 9.6)
        x.id(8)
        self.assertEqual(x.get_id, 8)
        x.name("Paul Davis")
        self.assertEqual(x.get_name, "Paul Davis")
        x.value(9.8)
        self.assertEqual(x.get_grade_value, 9.8)

    def test_average_discipline_name(self):
        x = AverageDisciplineGrade(9, "Thomas Riker", 7, "Biology", 9.2)
        x.student_id(7)
        self.assertEqual(x.get_student_id, 7)

        x.student_name("Julia Picard")
        self.assertEqual(x.get_student_name, "Julia Picard")

        x.discipline_id(5)
        self.assertEqual(x.get_discipline_id, 5)

        x.discipline_name("Math")
        self.assertEqual(x.get_discipline_name, "Math")

        x.value(9.5)
        self.assertEqual(x.get_grade_value, 9.5)

    def test_grade_validator(self):
        x = Grade(4, 5, 6, 7)
        x.value(-1)
        with self.assertRaises(Exception):
            self._gradeValidator.validate(x)
        x.value("cha cha")
        with self.assertRaises(Exception):
            self._gradeValidator.validate(x)

        x.discipline_id(-1)
        with self.assertRaises(Exception):
            self._gradeValidator.validate(x)
        x.discipline_id("cha cha")
        with self.assertRaises(Exception):
            self._gradeValidator.validate(x)

        x.student_id(-1)
        with self.assertRaises(Exception):
            self._gradeValidator.validate(x)
        x.student_id("cha cha")
        with self.assertRaises(Exception):
            self._gradeValidator.validate(x)



