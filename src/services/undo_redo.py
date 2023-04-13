from dataclasses import dataclass
from src.services.handlers import *

@dataclass
class UndoOperation:
    target_object: object
    intermediary_object: object
    handler: object
    args: tuple


@dataclass
class RedoOperation:
    target_object: object
    intermediary_object: object
    handler: object
    args: tuple


class UndoRedoManager:
    __undo_operations = []
    __redo_operations = []
    __redo_args = []
    __undo_args = []

    @staticmethod
    def register_undo_operation(target_object, intermediary_object, handler, *args):
        UndoRedoManager.__undo_operations.append(UndoOperation(target_object, intermediary_object, handler, args))

    @staticmethod
    def register_redo_operation(target_object, intermediary_object, handler, *args):
        UndoRedoManager.__redo_operations.append(RedoOperation(target_object, intermediary_object, handler, args))

    @staticmethod
    def add_new_undo(target_object, intermediary_object, handler, *args):
        UndoRedoManager.__redo_operations.clear()
        UndoRedoManager.register_undo_operation(target_object, intermediary_object, handler, *args)

    @staticmethod
    def find_function_type_for_undo(function):
        if function == delete_student_handler:
            return RedoHandlers.ADD_STUDENT
        elif function == add_student_handler:
            return RedoHandlers.DELETE_STUDENT
        elif function == undo_update_student_handler:
            return RedoHandlers.UPDATE_STUDENT

        elif function == delete_discipline_handler:
            return RedoHandlers.ADD_DISCIPLINE
        elif function == add_discipline_handler:
            return RedoHandlers.DELETE_DISCIPLINE
        elif function == undo_update_discipline_handler:
            return RedoHandlers.UPDATE_DISCIPLINE

        elif function == delete_grade_handler:
            return RedoHandlers.ADD_GRADE

    @staticmethod
    def find_function_type_for_redo(function):
        if function == add_student_handler:
            return UndoHandlers.ADD_STUDENT
        elif function == delete_student_handler:
            return UndoHandlers.DELETE_STUDENT
        elif function == redo_update_student_handler:
            return UndoHandlers.UPDATE_STUDENT

        elif function == add_discipline_handler:
            return UndoHandlers.ADD_DISCIPLINE
        elif function == delete_discipline_handler:
            return UndoHandlers.DELETE_DISCIPLINE
        elif function == redo_update_discipline_handler:
            return UndoHandlers.UPDATE_DISCIPLINE

        elif function == add_grade_handler:
            return UndoHandlers.ADD_GRADE



    @staticmethod
    def undo():
        if not UndoRedoManager.__undo_operations:
            print("Can't undo any further!")
            return
        undo_operation = UndoRedoManager.__undo_operations.pop()
        handler = UndoRedoManager.find_function_type_for_undo(undo_operation.handler)
        UndoRedoManager.register_redo_operation(undo_operation.target_object,  undo_operation.intermediary_object,\
                                                handler, *undo_operation.args)
        undo_operation.handler(undo_operation.target_object, undo_operation.intermediary_object, *undo_operation.args)

    @staticmethod
    def redo():
        if not UndoRedoManager.__redo_operations:
            print("Can't redo any further!")
            return
        redo_operation = UndoRedoManager.__redo_operations.pop()
        handler = UndoRedoManager.find_function_type_for_redo(redo_operation.handler)
        UndoRedoManager.register_undo_operation(redo_operation.target_object, redo_operation.intermediary_object,\
                                                handler, *redo_operation.args)
        redo_operation.handler(redo_operation.target_object, redo_operation.intermediary_object, *redo_operation.args)


