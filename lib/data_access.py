from dataclasses import dataclass, field
from typing import Protocol, List, Optional

from simio_di import Depends

from lib.entities import PrimaryKey, Student
from lib.exceptions import DuplicateRecordId, RecordNotFound
from lib.file_data_client import FileDataClient


class StudentDataAccessProtocol(Protocol):
    """ Интефейс для коммуникации с БД с данными о студентах """
    def add_student(self, student: Student):
        ...

    def get_student(self, record_id: PrimaryKey) -> Student:
        ...


@dataclass
class FileStudentDataAccess(StudentDataAccessProtocol):
    """
        Реализация интерфейса StudentDataAccessProtocol, где в качестве БД используется файл
        Данная реализация использует линейный поиск. Сложность O(n)
    """
    file_client: Depends[FileDataClient]  # type: FileDataClient[Student]

    def add_student(self, student: Student):
        self.file_client.write(student)

    def get_student(self, record_id: PrimaryKey) -> Student:
        for student, _ in self.file_client.iter_read():
            # Проходимся по всем записям, ищем нужного студента
            if student.record_id == record_id:
                return student

        # Если не нашли, выкидываем ошибку
        raise RecordNotFound(f"Student with id {record_id} not found")


@dataclass
class IndexFileStudentDataAccess(FileStudentDataAccess):
    """
        Реализация интерфейса StudentDataAccessProtocol, где в качестве БД используется файл
        Данная реализация использует поиск с помощью индексного массива. Сложность O(1)
    """
    _index_array: List[Optional[int]] = field(default_factory=list, init=False)

    def __post_init__(self):
        # при инициализации строим индекс
        self._create_index()

    def add_student(self, student: Student):
        self._validate_record_id(student.record_id)  # проверяем id
        position = self.file_client.write(student)  # записываем в файл
        self._index_array[student.record_id] = position  # обновляем индекс

    def get_student(self, record_id: PrimaryKey) -> Student:
        position = self._get_position_by_key(record_id)  # получаем позицию в файле из индекса
        return self.file_client.read_at_position(position)

    def _create_index(self):
        for student, position in self.file_client.iter_read():
            self._validate_record_id(student.record_id)  # проверяем id
            self._index_array[student.record_id] = position  # сохраняем в массиве позицию в файле

    def _validate_record_id(self, record_id: PrimaryKey):
        if record_id >= len(self._index_array):
            # если id больше текущего, то расширяем его
            self._expand_index_array(record_id)

        if self._index_array[record_id] is not None:
            # Если такой индес уже есть, выкидываем ошибку, данные некорректны
            raise DuplicateRecordId(f"Found duplicate record id {record_id}")

    def _get_position_by_key(self, key: PrimaryKey):
        try:
            position = self._index_array[key]
        except IndexError as exception:
            # Если вышли за пределы массива, значит такой записи нет
            raise RecordNotFound(f"Student with id: {key} not found") from exception

        if position is None:
            # Для этого ключа не нашли значения, значит такой записи нет
            raise RecordNotFound(f"Student with id: {key} not found")

        return position

    def _expand_index_array(self, record_id: PrimaryKey):
        """ Расширяет массив в два раза значениями None """
        expand_size = (record_id - (len(self._index_array) - 1)) * 2
        for _ in range(expand_size):
            self._index_array.append(None)
