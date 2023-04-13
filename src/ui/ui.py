from src.services.handlers import UndoHandlers
from src.services.undo_redo import UndoRedoManager


class UI:
    def __init__(self, student_serv, discipline_serv, grade_serv):
        self.__student_services = student_serv
        self.__discipline_services = discipline_serv
        self.__grade_services = grade_serv

    @staticmethod
    def print_second_menu():
        print("Which operation would you like to perform?")
        print("\t1: Add")
        print("\t2: List")
        print("\t3: Filter")
        print("\t4: Sort")
        print("\t5: Update, only for students or disciplines")
        print("\t6: Delete, only for students or disciplines")
        print("\t7: Search, only for students or disciplines")

    @staticmethod
    def print_first_menu():
        print("Hello, What would you like to do today?")
        print("\t1: Student services")
        print("\t2: Discipline services")
        print("\t3: Grade services")
        print("\t4: Statistics")
        print("\t5: Undo")
        print("\t6: Redo")
        print("\t7: Exit")

    def add_student(self):
        print("Add student: ")
        try:
            id = int(input("Id: "))
        except:
            print(ValueError("  Id Has to be a number!"))
            return
        name = input("Name: ")
        self.__student_services.add_student(id, name)
        UndoRedoManager.add_new_undo(self.__student_services, self.__grade_services, UndoHandlers.ADD_STUDENT, id, name)

    def add_discipline(self):
        print("Add Discipline: ")
        try:
            id = int(input("Id: "))
        except:
            print(ValueError("  Id Has to be a number!"))
            return

        name = input("Name: ")
        self.__discipline_services.add_discipline(id, name)
        UndoRedoManager.add_new_undo(self.__discipline_services, self.__grade_services, UndoHandlers.ADD_DISCIPLINE, id, name)

    def add_grade(self):
        print("Add Grade: ")
        student_id = int(input("Student Id: "))
        if not self.__student_services.check_student_id(student_id):
            print(" There is no Student with this id!")
            return
        discipline_id = int(input("Discipline Id: "))
        if not self.__discipline_services.check_discipline_id(discipline_id):
            print(" There is no Discipline with this id!")
            return
        try:
            value = int(input("Grade: "))
        except:
            print(ValueError("Grade has to be a number!"))
            return
        id = len(self.__grade_services._repository._entities)
        self.__grade_services.add_grade(id, student_id, discipline_id, value)
        UndoRedoManager.add_new_undo(self.__grade_services, self.__grade_services, UndoHandlers.ADD_GRADE, id,\
                                     student_id, discipline_id, value)

    def print_all_students(self):
        for i in self.__student_services.list_students():
            if i:
                print(" Id:", str(i.id) + ",", "Name:", i._name)

    def print_all_disciplines(self):
        for i in self.__discipline_services.list_disciplines():
            if i:
                print("Id:", str(i.id) + ",", "Name:", i._name)

    def print_all_grades(self):
        for i in self.__grade_services._repository._entities:
            if i:
                print("Student Id:", str(i.get_student_id) + ",", "Discipline Id:", str(i.get_discipline_id) + ",",
                      "Grade:", i.get_grade_value)

    def delete_student(self):
        del_id = int(input("The id of the student: "))
        student = self.__student_services.get_student(del_id)
        UndoRedoManager.add_new_undo(self.__student_services, self.__grade_services, UndoHandlers.DELETE_STUDENT,\
                                     student.id, student.name)
        self.__student_services.delete_student(del_id)
        self.__grade_services.save_student_grades_for_undo_redo(del_id)
        self.__grade_services.delete_grades_student(del_id)

    def delete_discipline(self):
        del_id = int(input("The id of the discipline: "))
        discipline = self.__discipline_services.get_discipline(del_id)
        UndoRedoManager.add_new_undo(self.__discipline_services, self.__grade_services, UndoHandlers.DELETE_DISCIPLINE,\
                                     discipline.id, discipline.name)
        self.__discipline_services.delete_discipline(del_id)
        self.__grade_services.delete_grades_discipline(del_id)

    def update_student(self):
        s_id = int(input("The id of the student: "))
        if self.__student_services.check_student_id(s_id):
            new_name = input("New Name: ")
            student = self.__student_services.get_student(s_id)
            UndoRedoManager.add_new_undo(self.__student_services, self.__grade_services, UndoHandlers.UPDATE_STUDENT,\
                                         s_id, student.name, new_name)
            self.__student_services.update_student_name(s_id, new_name)
        else:
            print("There is no student with this id!")
            return

    def update_discipline(self):
        d_id = int(input("The id of the discipline: "))
        if self.__discipline_services.check_discipline_id(d_id):
            new_name = input("New Name: ")
            discipline = self.__discipline_services.get_discipline(d_id)
            UndoRedoManager.add_new_undo(self.__discipline_services, self.__grade_services,\
                                                    UndoHandlers.UPDATE_DISCIPLINE, d_id, discipline.name, new_name)
            self.__discipline_services.update_discipline_name(d_id, new_name)
        else:
            print("There is no discipline with this id!")
            return

    def print_search_menu(self):
        print("1: Search by name")
        print("2: Search by id")

    def print_list(self, items):
        for i in items:
            print("Id:", str(i.id) + ",", "Name:", i.name)

    def search_student(self):
        self.print_search_menu()
        option = int(input("Command: "))
        if option == 1:
            name = input("Name: ")
            self.print_list(self.__student_services.search_student_by_name(name))
        else:
            id = input("Id: ")
            if id.isdigit():
                self.print_list(self.__student_services.search_student_by_id(id))
            else:
                print("Id has to be a number!")
                return

    def search_discipline(self):
        self.print_search_menu()
        option = int(input("Command: "))
        if option == 1:
            name = input("Name: ")
            self.print_list(self.__discipline_services.search_discipline_by_name(name))
        else:
            id = input("Id: ")
            if id.isdigit():
                self.print_list(self.__discipline_services.search_discipline_by_id(id))
            else:
                print("Id has to be a number!")
                return

    def print_statistics_menu(self):
        print("1: Failing Students")
        print("2: Top Students")
        print("3: Disciplines with at least one grade")

    def statistics(self, option):
        if option == 1:
            for x in self.__grade_services.failing_students():
                print("Student Id:", str(x.get_student_id) + ",", "Discipline Id:", str(x.get_discipline_id) + ",",
                      "Grade:", "{:.2f}".format(x.get_grade_value))
        elif option == 2:
            for x in self.__grade_services.best_student_averages():
                print("Student Id:", str(x.get_id) + ",", "Student Name:", x.get_name + ",",
                      "Grade:", "{:.2f}".format(x.get_grade_value))
        else:
            for x in self.__grade_services.discipline_average_grades():
                print("Discipline Id:", str(x.get_id) + ",", "Discipline Name:", x.get_name + ",",
                      "Grade:", "{:.2f}".format(x.get_grade_value))

    def filter_menu_students_disciplines(self):
        print("1: Filter by name")
        print("2: Filter by id greater than")
        print("3: Filter by id smaller than")
        print("4: Filter by id equal to")

    def filter_menu_grades(self):
        print("1: Filter by grade greater than")
        print("2: Filter by grade smaller than")
        print("3: Filter by grade equal to")

    def filter_students(self, mode, params):
        if int(mode) == 1:
            for i in self.__student_services.filter_students(int(mode), params):
                if i:
                    print(" Id:", str(i.id) + ",", "Name:", i._name)
        else:
            for i in self.__student_services.filter_students(int(mode), int(params)):
                if i:
                    print(" Id:", str(i.id) + ",", "Name:", i._name)

    def filter_disciplines(self, mode, params):
        if int(mode) == 1:
            for i in self.__discipline_services.filter_disciplines(int(mode), params):
                if i:
                    print("Id:", str(i.id) + ",", "Name:", i._name)
        else:
            for i in self.__discipline_services.filter_disciplines(int(mode), int(params)):
                if i:
                    print("Id:", str(i.id) + ",", "Name:", i._name)

    def filter_grades(self, mode, params):
        for i in self.__grade_services.filter_grades(int(mode), int(params)):
            if i:
                print("Student Id:", str(i.get_student_id) + ",", "Discipline Id:", str(i.get_discipline_id) + ",",
                      "Grade:", i.get_grade_value)

    def sort_menu_students_disciplines(self):
        print("1: Sort by name increasing")
        print("2: Sort by name decreasing")
        print("3: Sort by id increasing")
        print("4: Sort by id decreasing")

    def sort_menu_grades(self):
        print("1: Sort by grade increasing")
        print("2: Sort by grade decreasing")

    def sort_students(self, mode):
        for i in self.__student_services.sort_students(int(mode)):
            if i:
                print(" Id:", str(i.id) + ",", "Name:", i._name)

    def sort_disciplines(self, mode):
        for i in self.__discipline_services.sort_disciplines(int(mode)):
            if i:
                print("Id:", str(i.id) + ",", "Name:", i._name)

    def sort_grades(self, mode):
        for i in self.__grade_services.sort_grades(int(mode)):
            if i:
                print("Student Id:", str(i.get_student_id) + ",", "Discipline Id:", str(i.get_discipline_id) + ",",
                      "Grade:", i.get_grade_value)




    def start(self):

        while True:
            self.print_first_menu()

            kind = int(input("Command: "))
            if kind > 7:
                print ("There is no operation with this command!")
            elif kind == 7:
                return
            elif kind == 4:
                self.print_statistics_menu()
                option = int(input("Statistics type: "))
                self.statistics(option)
            elif kind == 5:
                UndoRedoManager.undo()
            elif kind  == 6:
                UndoRedoManager.redo()
            else:
                self.print_second_menu()
                operation = int(input("Operation: "))

                if operation == 1:
                    if kind == 1:
                        self.add_student()
                    elif kind == 2:
                        self.add_discipline()
                    else:
                        self.add_grade()

                if operation == 2:
                    if kind == 1:
                        self.print_all_students()
                    elif kind == 2:
                        self.print_all_disciplines()
                    else:
                        self.print_all_grades()

                if operation == 3:
                    if kind == 1:
                        self.filter_menu_students_disciplines()
                        type = int(input("Command: "))
                        params = input("Filter parameter: ")
                        self.filter_students(type, params)

                    elif kind == 2:
                        self.filter_menu_students_disciplines()
                        type = int(input("Command: "))
                        params = input("Filter parameter: ")
                        self.filter_disciplines(type, params)

                    else:
                        self.filter_menu_grades()
                        type = int(input("Command: "))
                        params = input("Filter parameter: ")
                        self.filter_grades(type, params)

                if operation == 4:
                    if kind == 1:
                        self.sort_menu_students_disciplines()
                        mode = int(input("Command: "))
                        self.sort_students(mode)

                    elif kind == 2:
                        self.sort_menu_students_disciplines()
                        mode = int(input("Command: "))
                        self.sort_disciplines(mode)

                    else:
                        self.sort_menu_grades()
                        mode = int(input("Command: "))
                        self.sort_grades(mode)

                if operation == 5:
                    if kind == 1:
                        self.update_student()
                    elif kind == 2:
                        self.update_discipline()
                    else:
                        print("Operation not available for Grade Services!")

                if operation == 6:
                    if kind == 1:
                        self.delete_student()
                    elif kind == 2:
                        self.delete_discipline()
                    else:
                        print("Operation not available for Grade Services!")

                if operation == 7:
                    if kind == 1:
                        self.search_student()
                    elif kind == 2:
                        self.search_discipline()
                    else:
                        print("Operation not available for Grade Services!")

