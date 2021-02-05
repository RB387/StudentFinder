from dataclasses import dataclass, field
from typing import Protocol, List, Optional

from simio_di import Depends, DependencyInjector, DependenciesContainer

from lib.entities import PrimaryKey, Student
from lib.exceptions import DuplicateRecordId, RecordNotFound
from lib.file_data_client import FileDataClient


class StudentDataAccessProtocol(Protocol):
    def add_student(self, student: Student):
        ...

    def get_student(self, record_id: PrimaryKey) -> Student:
        ...


@dataclass
class FileStudentDataAccess(StudentDataAccessProtocol):
    file_client: Depends[FileDataClient]  # type: FileDataClient[Student]

    def add_student(self, student: Student):
        self.file_client.write(student)

    def get_student(self, record_id: PrimaryKey) -> Student:
        for student, _ in self.file_client.iter_read():
            if student.record_id == record_id:
                return student

        raise RecordNotFound(f"Student with id {record_id} not found")


@dataclass
class IndexFileStudentDataAccess(FileStudentDataAccess):
    _index_array: List[Optional[int]] = field(default_factory=list, init=False)

    def __post_init__(self):
        self._create_index()

    def add_student(self, student: Student):
        self._validate_record_id(student.record_id)
        position = self.file_client.write(student)
        self._index_array[student.record_id] = position

    def get_student(self, record_id: PrimaryKey) -> Student:
        position = self._get_position_by_key(record_id)
        return self.file_client.read_at_position(position)

    def _create_index(self):
        for student, position in self.file_client.iter_read():
            self._validate_record_id(student.record_id)
            self._index_array[student.record_id] = position

    def _validate_record_id(self, record_id: PrimaryKey):
        if record_id > len(self._index_array):
            self._expand_index_array(record_id)

        if self._index_array[record_id] is not None:
            raise DuplicateRecordId(f"Found duplicate record id {record_id}")

    def _get_position_by_key(self, key: PrimaryKey):
        try:
            position = self._index_array[key]
        except IndexError as exception:
            raise RecordNotFound(f"Student with id: {key} not found") from exception

        if position is None:
            raise RecordNotFound(f"Student with id: {key} not found")

        return position

    def _expand_index_array(self, record_id: PrimaryKey):
        expand_size = (record_id - len(self._index_array)) * 2
        for _ in range(expand_size):
            self._index_array.append(None)


if __name__ == "__main__":
    config = {
        FileDataClient: {
            "file_path": "test.txt",
            "entity_type": Student,
        }
    }

    injector = DependencyInjector(config, deps_container=DependenciesContainer())
    dao = injector.inject(IndexFileStudentDataAccess)()

    print(dao.get_student(PrimaryKey(1)))
    # dao.add_student(
    #     Student(
    #         record_id=PrimaryKey(10),
    #         first_name="DAS",
    #         last_name="sss",
    #         birthday_date="2020",
    #     )
    # )
    print(dao.get_student(PrimaryKey(10)))
