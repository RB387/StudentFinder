from lib.entities import Student, PrimaryKey
from lib.file_data_client import FileDataClient


class TestFileDataClient:
    def test_field_names(self):
        client = FileDataClient('students_test.txt', Student)
        assert client._field_names == ['record_id', 'first_name', 'last_name', 'birthday_date']

    def test_read_at_position(self):
        client = FileDataClient('students_test.txt', Student)
        assert client.read_at_position(45) == Student(
            record_id=PrimaryKey(1),
            first_name='first',
            last_name='last',
            birthday_date='12-02-2000',
        )

    def test_iter_read(self):
        client = FileDataClient('students_test.txt', Student)
        students = [
            (Student(record_id=PrimaryKey(1), first_name='first', last_name='last', birthday_date='12-02-2000'), 45),
            (Student(record_id=PrimaryKey(3), first_name='dsa', last_name='ddd', birthday_date='12-01-2000'), 69),
            (Student(record_id=PrimaryKey(2), first_name='dssss', last_name='ccc', birthday_date='12-03-2000'), 90),
        ]
        assert [student for student in client.iter_read()] == students

    def test_load_entity(self):
        client = FileDataClient('students_test.txt', Student)
        assert client._load_entity('1,first,last,12-02-2000\n') == Student(
            record_id=PrimaryKey(1),
            first_name='first',
            last_name='last',
            birthday_date='12-02-2000',
        )

    def test_dump_entity(self):
        client = FileDataClient('students_test.txt', Student)

        student = Student(
            record_id=PrimaryKey(1),
            first_name='first',
            last_name='last',
            birthday_date='12-02-2000',
        )

        assert client._dump_entity(student) == '1,first,last,12-02-2000'
