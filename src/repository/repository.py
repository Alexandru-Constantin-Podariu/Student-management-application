from src.domain.Exceptions import StudentManagementException
from src.domain.domain import Grade, Discipline, Student
from src.repository.iterable_sort_and_filter import Data
import pickle


class RepositoryException(StudentManagementException):
    pass


class Repository:
    def __init__(self):
        self._entities = Data()

    def find_by_id(self, entity_id):
        '''
        Function that finds an entity by id
        :param entity_id: The id of that entity
        :return: The entity we need if it is found, None otherwise
        '''
        for entity in self._entities:
            if entity:
                if int(entity._id) == int(entity_id):
                    return entity
        return None

    def add(self, entity):
        '''
        Function that saves an entity in the dictionary
        :param entity: The entity to save
        :return: Does not return anything, just saves
        '''
        if self.find_by_id(entity._id) is not None:
            raise RepositoryException("The id is used")
        else:
            self._entities.append(entity)

    def update_name(self, entity_id, new_name):
        '''
        Function that updates the name of an entity
        :param entity_id: The id of the entity
        :param new_name: The new name for that entity
        :return:Does not return anything, just updates
        '''
        if self.find_by_id(int(entity_id)) is None:
            raise RepositoryException("Id does not exist!")
        else:
            for entity in self._entities:
                if entity.id == entity_id:
                    entity._name = new_name

    def delete_by_id(self, entity_id):
        '''
        Function that deletes an entity based on its id
        :param entity_id: The id of the entity
        :return: Does not return anything, just deletes
        '''
        if self.find_by_id(int(entity_id)) is None:
            raise RepositoryException("Id does not exist!")
        else:
            entity = self.find_by_id(entity_id)
            self._entities.remove(entity)


    def get_all(self):
        '''
        Function that returns a list of all the entities
        :return: Returns a list
        '''
        return self._entities.list()

    def search_by_name(self, string):
        new_list = []
        for x in self._entities:
            if x and string.lower() in x.name.lower():
                new_list.append(x)
        return new_list

    def search_by_id(self, string):
        new_list = []
        for x in self._entities:
            if x and string in str(x.id):
                new_list.append(x)
        return new_list


class TextFileRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rt")  # rt -> read, text-mode
        if self._file_name == "students.txt":
            for line in f.readlines():
                _id, name = line.split(maxsplit=1, sep=' ')
                self.add(Student(int(_id), name.rstrip()))
        elif self._file_name == "disciplines.txt":
            for line in f.readlines():
                _id, name = line.split(maxsplit=1, sep=' ')
                self.add(Discipline(int(_id), name.rstrip()))
        else:
            for line in f.readlines():
                _id, student_id, discipline_id, value = line.split(maxsplit=3, sep=' ')
                self.add(Grade(int(_id), int(student_id), int(discipline_id), int(value)))
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")  # wt -> write, text-mode
        if self._file_name == "grades.txt":
            for x in self._entities:
                if x:
                    f.write(str(x.get_id) + ' ' + str(x.get_student_id) + ' ' + str(x.get_discipline_id) + ' ' + str(x.get_grade_value) + ' '"\n")
        else:
            for x in self._entities:
                if x:
                    f.write(str(x.id) + ' ' + x.name + "\n")

        f.close()

    def add(self, entity):
        """
        Save the entity to file
        """
        super(TextFileRepository, self).add(entity)
        self._save_file()

    def delete_by_id(self, delete_id):
        super(TextFileRepository, self).delete_by_id(delete_id)
        self._save_file()

    def update_name(self, _id, new_name):
        super(TextFileRepository, self).update_name(_id, new_name)
        self._save_file()


class BinFileRepository(Repository):
    def __init__(self, file_name):
        super().__init__()

        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rb")  # rt -> read, binary
        self._entities = pickle.load(f)
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wb")  # wb -> write, binary
        pickle.dump(self._entities, f)
        f.close()

    def add(self, entity):
        """
        Save the entity to file
        """
        super(BinFileRepository, self).add(entity)
        self._save_file()

    def delete_by_id(self, delete_id):
        super(BinFileRepository, self).delete_by_id(delete_id)
        self._save_file()

    def update_name(self, _id, new_name):
        super(BinFileRepository, self).update_name(_id, new_name)
        self._save_file()
