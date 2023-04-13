from enum import Enum


def delete_student_handler (student_services, grade_services, id, name):
    """
    Delete student
    :return:
    """
    student_services.delete_student(id)
    grade_services.save_student_grades_for_undo_redo(id)
    grade_services.delete_grades_student(id)


def add_student_handler(student_services, grade_services, id, name):
    """
    Add student
    :return:
    """
    student_services.add_student(id, name)
    grade_services.put_back_student_grades(id)


def undo_update_student_handler(student_services, grade_services, id, name, new_name):
    """
    Undo update student
    :return:
    """
    student_services.update_student_name(id, name)


def delete_discipline_handler(discipline_services, grade_services, id, name):
    """
    Delete discipline
    :return:
    """
    discipline_services.delete_discipline(id)
    grade_services.save_discipline_grades_for_undo_redo(id)
    grade_services.delete_grades_discipline(id)


def add_discipline_handler(discipline_services, grade_services, id, name):
    """
    Add discipline
    :return:
    """
    discipline_services.add_discipline(id, name)
    grade_services.put_back_discipline_grades(id)


def undo_update_discipline_handler(discipline_services, grade_services, id, name, new_name):
    """
    Undo update discipline
    :return:
    """
    discipline_services.update_discipline_name(id, name)


def delete_grade_handler(grade_services, service, id, s_id, d_id, value):
    """
    Delete grade
    :return:
    """
    grade_services.delete_grade(id)


def add_grade_handler(grade_services, services, id, s_id, d_id, value):
    """
    Add discipline
    :return:
    """
    grade_services.add_grade(id, s_id, d_id, value)


def redo_update_student_handler(student_services, grade_services,  id, name, new_name):
    """
    Undo update student
    :return:
    """
    student_services.update_student_name(id, new_name)


def redo_update_discipline_handler(discipline_services, grade_services, id, name, new_name):
    """
    Undo update discipline
    :return:
    """
    discipline_services.update_discipline_name(id, new_name)


class UndoHandlers(Enum):
    ADD_STUDENT = delete_student_handler
    DELETE_STUDENT = add_student_handler
    UPDATE_STUDENT = undo_update_student_handler

    ADD_DISCIPLINE = delete_discipline_handler
    DELETE_DISCIPLINE = add_discipline_handler
    UPDATE_DISCIPLINE = undo_update_discipline_handler

    ADD_GRADE = delete_grade_handler


class RedoHandlers(Enum):
    ADD_STUDENT = add_student_handler
    DELETE_STUDENT = delete_student_handler
    UPDATE_STUDENT = redo_update_student_handler

    ADD_DISCIPLINE = add_discipline_handler
    DELETE_DISCIPLINE = delete_discipline_handler
    UPDATE_DISCIPLINE = redo_update_discipline_handler

    ADD_GRADE = add_grade_handler

