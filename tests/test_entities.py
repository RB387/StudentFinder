from lib.entities import Student, PrimaryKey


class TestStudent:
    def test_from_dict(self):
        as_dict = {
            'record_id': '123',
            'first_name': 'first',
            'last_name': 'last',
            'birthday_date': '2020-03-03',
        }
        student = Student.from_dict(as_dict)

        assert student == Student(
            record_id=PrimaryKey(123),
            first_name='first',
            last_name='last',
            birthday_date='2020-03-03'
        )

    def test_as_dict(self):
        student = Student(
            record_id=PrimaryKey(123),
            first_name='first',
            last_name='last',
            birthday_date='2020-03-03'
        )
        assert student.as_dict() == {
            'record_id': 123,
            'first_name': 'first',
            'last_name': 'last',
            'birthday_date': '2020-03-03',
        }
