from dataclasses import dataclass, field
from typing import Protocol, List, Optional, IO

from lib.entities import PrimaryKey, Student
from lib.exceptions import DuplicateRecordId, RecordNotFound


class StudentDataAccessProtocol(Protocol):
    def add_student(self, student: Student):
        ...

    def get_student(self, record_id: PrimaryKey) -> Student:
        ...


@dataclass
class FileStudentDataAccess(StudentDataAccessProtocol):
    file_path: str
    delimiter: str = ","
    new_line: str = "\n"
    _field_names: List[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        with open(self.file_path, "r") as file:
            self.prepare_metadata(file)

    def prepare_metadata(self, file: IO):
        self._load_field_names(file)

    def add_student(self, student: Student):
        with open(self.file_path, "a") as file:
            file.write(self._write_student(student))

    def get_student(self, record_id: PrimaryKey) -> Student:
        with open(self.file_path) as file:
            for student_raw_line in file.readlines():
                student = self._read_student(student_raw_line)
                if student.record_id == record_id:
                    return student

        raise RecordNotFound(f"Student with id {record_id} not found")

    def _load_field_names(self, file: IO):
        self._field_names = file.readline().rstrip(self.new_line).split(self.delimiter)

    def _read_student(self, student_raw_line: str) -> Student:
        student_raw_line = student_raw_line.rstrip(self.new_line)

        student_data = {}

        for idx, col in enumerate(student_raw_line.split(self.delimiter)):
            field_name = self._field_names[idx]
            student_data[field_name] = col

        return Student.from_dict(student_data)

    def _write_student(self, student: Student) -> str:
        student_raw = []
        student_dict = student.as_dict()

        for field_name in self._field_names:
            student_raw.append(str(student_dict[field_name]))

        return self.delimiter.join(student_raw)


@dataclass
class IndexFileStudentDataAccess(FileStudentDataAccess):
    _index_array: List[Optional[int]] = field(default_factory=list, init=False)

    def prepare_metadata(self, file: IO):
        super().prepare_metadata(file)
        self._create_index(file)

    def add_student(self, student: Student):
        self._validate_record_id(student.record_id)

        with open(self.file_path, "a+") as file:
            file.seek(file.tell() - 1)

            last_character = file.read(1)
            if last_character != self.new_line:
                file.write(self.new_line)

            self._index_array[student.record_id] = file.tell()
            file.write(self._write_student(student))

    def get_student(self, record_id: PrimaryKey) -> Student:
        with open(self.file_path) as file:
            file_position = self._get_position_by_key(record_id)
            file.seek(file_position)

            return self._read_student(file.readline())

    def _create_index(self, file: IO):
        file_positions = file.tell()

        for student_raw_line in file.readlines():
            student = self._read_student(student_raw_line)

            self._validate_record_id(student.record_id)

            self._index_array[student.record_id] = file_positions
            file_positions = file.tell()

    def _validate_record_id(self, record_id: PrimaryKey):
        if record_id > len(self._index_array):
            self._expand_index_array(record_id)

        if self._index_array[record_id] is not None:
            raise DuplicateRecordId(
                f"Error while creating index. Found duplicate record id {record_id}"
            )

    def _get_position_by_key(self, key: PrimaryKey):
        try:
            position = self._index_array[key]
        except IndexError as e:
            raise RecordNotFound(f"Student with id: {key} not found") from e

        if position is None:
            raise RecordNotFound(f"Student with id: {key} not found")

        return position

    def _expand_index_array(self, record_id: PrimaryKey):
        expand_size = (record_id - len(self._index_array)) * 2
        for _ in range(expand_size):
            self._index_array.append(None)


if __name__ == "__main__":
    dao = IndexFileStudentDataAccess("test.txt")
    print(dao.get_student(PrimaryKey(1)))
    dao.add_student(
        Student(
            record_id=PrimaryKey(10),
            first_name="DAS",
            last_name="sss",
            birthday_date="2020",
        )
    )
    print(dao.get_student(PrimaryKey(10)))
