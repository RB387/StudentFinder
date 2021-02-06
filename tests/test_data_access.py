from unittest.mock import MagicMock

import pytest

from lib.data_access import FileStudentDataAccess, IndexFileStudentDataAccess
from lib.entities import Student, PrimaryKey
from lib.exceptions import RecordNotFound, DuplicateRecordId
from tests.conftest import does_not_raise


class TestFileStudentDataAccess:
    def test_add_student(self):
        file_client = MagicMock()
        dao = FileStudentDataAccess(file_client)

        student = Student(
            record_id=PrimaryKey(1),
            first_name='first',
            last_name='last',
            birthday_date='2020-03-03'
        )
        dao.add_student(student)

        file_client.write.assert_called_once_with(student)

    @pytest.mark.parametrize(
        'students, record_id_to_find, expected_result, expected_exception',
        (
            (
                [
                    (Student(record_id=PrimaryKey(1), first_name='first', last_name='last', birthday_date='2020-03-03'), 0),
                    (Student(record_id=PrimaryKey(2), first_name='das', last_name='das', birthday_date='2020-03-03'), 1),
                    (Student(record_id=PrimaryKey(3), first_name='cccc', last_name='aaa', birthday_date='2020-03-03'), 2),
                ],
                PrimaryKey(2),
                Student(record_id=PrimaryKey(2), first_name='das', last_name='das', birthday_date='2020-03-03'),
                does_not_raise(),
            ),
            (
                [
                    (Student(record_id=PrimaryKey(1), first_name='first', last_name='last', birthday_date='2020-03-03'), 0),
                    (Student(record_id=PrimaryKey(2), first_name='das', last_name='das', birthday_date='2020-03-03'), 1),
                ],
                PrimaryKey(3),
                None,
                pytest.raises(RecordNotFound),
            ),
        ),
    )
    def test_get_student(self, students, record_id_to_find, expected_result, expected_exception):
        file_client = MagicMock()
        file_client.iter_read.return_value = students

        dao = FileStudentDataAccess(file_client)

        with expected_exception:
            result = dao.get_student(record_id_to_find)
            assert result == expected_result


class TestIndexFileStudentDataAccess:
    @pytest.mark.parametrize(
        'students, expected_index',
        (
            (
                [
                    (Student(record_id=PrimaryKey(1), first_name='first', last_name='last', birthday_date='2020-03-03'), 11),
                    (Student(record_id=PrimaryKey(3), first_name='das', last_name='das', birthday_date='2020-03-03'), 22),
                    (Student(record_id=PrimaryKey(8), first_name='cccc', last_name='aaa', birthday_date='2020-03-03'), 33),
                ],
                [None, 11, None, 22, None, None, None, None, 33, None, None, None, None, None],
            ),
        ),
    )
    def test_create_index(self, students, expected_index):
        file_client = MagicMock()
        file_client.iter_read.return_value = students

        dao = IndexFileStudentDataAccess(file_client)
        assert dao._index_array == expected_index

    @pytest.mark.parametrize(
        'current_index, record_id, expected_index, expected_exception',
        (
            (
                [], PrimaryKey(3), [None, None, None, None, None, None, None, None], does_not_raise()
            ),
            (
                [None, 123], PrimaryKey(1), [None, 123], pytest.raises(DuplicateRecordId)
            ),
        ),
    )
    def test_validate_record_id(self, current_index, record_id, expected_index, expected_exception):
        file_client = MagicMock()
        file_client.iter_read.return_value = ()

        dao = IndexFileStudentDataAccess(file_client)
        dao._index_array = current_index

        with expected_exception:
            dao._validate_record_id(record_id)
            assert dao._index_array == expected_index

    @pytest.mark.parametrize(
        'key, current_index, expected_result, expected_exception',
        (
            (PrimaryKey(2), [None, None, 12], 12, does_not_raise()),
            (PrimaryKey(1), [None, None, 12], None, pytest.raises(RecordNotFound)),
            (PrimaryKey(10), [None, None, 12], None, pytest.raises(RecordNotFound))
        ),
    )
    def test_get_position_by_key(self, key, current_index, expected_result, expected_exception):
        file_client = MagicMock()
        file_client.iter_read.return_value = ()

        dao = IndexFileStudentDataAccess(file_client)
        dao._index_array = current_index

        with expected_exception:
            result = dao._get_position_by_key(key)
            assert result == expected_result

    @pytest.mark.parametrize(
        'record_id, current_index, position, expected_index, expected_exception',
        (
            (PrimaryKey(2), [], 123, [None, None, 123, None, None, None], does_not_raise()),
            (PrimaryKey(1), [None, 222], 123, [None, 222], pytest.raises(DuplicateRecordId)),
        ),
    )
    def test_add_student(self, record_id, current_index, position, expected_index, expected_exception):
        file_client = MagicMock()
        file_client.iter_read.return_value = ()
        file_client.write.return_value = position

        dao = IndexFileStudentDataAccess(file_client)
        dao._index_array = current_index

        student = Student(
            record_id=record_id,
            first_name='123',
            last_name='123',
            birthday_date='123'
        )

        with expected_exception:
            dao.add_student(student)

        assert dao._index_array == expected_index
