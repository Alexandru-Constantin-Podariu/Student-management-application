from src.services.student_services import Student_services
from src.services.discipline_services import DisciplineServices
from src.services.grade_services import GradeServices
from src.repository.repository import Repository, TextFileRepository, BinFileRepository
from src.ui.ui import UI
from src.domain.Exceptions import *


def settings():
    f = open("settings.properties.txt", "rt")  # rt -> read, text-mode
    lines = f.readlines()
    f.close()
    a, b = lines[0].split(maxsplit=1, sep=' = ')
    if b.strip() == "inmemory":
        initialize_in_memory()
    elif b.strip() == "textfiles":
        a, b = lines[1].split(maxsplit=1, sep=' = ')
        c, d = lines[2].split(maxsplit=1, sep=' = ')
        e, f = lines[3].split(maxsplit=1, sep=' = ')
        initialize_text_files(b.strip(), d.strip(), f.strip())
    elif b.strip() == "binaryfiles":
        a, b = lines[1].split(maxsplit=1, sep=' = ')
        c, d = lines[2].split(maxsplit=1, sep=' = ')
        e, f = lines[3].split(maxsplit=1, sep=' = ')
        initialize_binary_files(b.strip(), d.strip(), f.strip())


def initialize_in_memory():

    student_validator = StudentValidator()
    student_repository = Repository()
    student_services = Student_services(student_repository, student_validator)
    student_services.generate_students()

    discipline_validator = DisciplineValidator()
    discipline_repository = Repository()
    discipline_services = DisciplineServices(discipline_repository, discipline_validator)
    discipline_services.generate_disciplines()

    grade_validator = GradeValidator()
    grade_repository = Repository()
    grade_services = GradeServices(grade_repository, student_repository, discipline_repository, grade_validator)
    grade_services.generate_grades()

    ui = UI(student_services, discipline_services, grade_services)
    ui.start()


def initialize_text_files(students_file, disciplines_file, grades_files):
    student_validator = StudentValidator()
    student_repository = TextFileRepository(students_file)
    student_services = Student_services(student_repository, student_validator)

    discipline_validator = DisciplineValidator()
    discipline_repository = TextFileRepository(disciplines_file)
    discipline_services = DisciplineServices(discipline_repository, discipline_validator)

    grade_validator = GradeValidator()
    grade_repository = TextFileRepository(grades_files)
    grade_services = GradeServices(grade_repository, student_repository, discipline_repository, grade_validator)

    ui = UI(student_services, discipline_services, grade_services)
    ui.start()


def initialize_binary_files(students_file, disciplines_file, grades_files):
    student_validator = StudentValidator()
    student_repository = BinFileRepository(students_file)
    student_services = Student_services(student_repository, student_validator)

    discipline_validator = DisciplineValidator()
    discipline_repository = BinFileRepository(disciplines_file)
    discipline_services = DisciplineServices(discipline_repository, discipline_validator)

    grade_validator = GradeValidator()
    grade_repository = BinFileRepository(grades_files)
    grade_services = GradeServices(grade_repository, student_repository, discipline_repository, grade_validator)

    ui = UI(student_services, discipline_services, grade_services)
    ui.start()


settings()
