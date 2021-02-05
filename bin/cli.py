from dataclasses import dataclass

from simio_di import Provide, DependencyInjector, DependenciesContainer

from bin.config import get_config
from bin.student_input import StudentInputCli
from lib.data_access import StudentDataAccessProtocol
from lib.entities import Student
from lib.exceptions import RecordNotFound, DuplicateRecordId


@dataclass
class CliInterface:
    student_data_access: Provide[StudentDataAccessProtocol]
    _running: bool = True

    def start(self):
        selector = {
            "1": self.add_student,
            "2": self.find_student,
            "3": self.exit,
        }

        while self._running:
            print("Выберите действие:")
            print("1. Добавить студента")
            print("2. Найти студента по номеру зачетной книжки")
            print("3. Выход")
            print(">> ", end="")

            user_choice = selector.get(input())

            if user_choice is None:
                print("Такого варианта ответа нет\n")

            user_choice()

    def add_student(self):
        record_id = StudentInputCli.input_record_id()
        first_name = StudentInputCli.input_first_name()
        last_name = StudentInputCli.input_last_name()
        birthday_date = StudentInputCli.input_birthday()

        student = Student(
            record_id=record_id,
            first_name=first_name,
            last_name=last_name,
            birthday_date=birthday_date,
        )
        try:
            self.student_data_access.add_student(student)
            print("Добавлено!\n")
        except DuplicateRecordId:
            print("Студент с таким номером записной книжки уже существует!\n")

    def find_student(self):
        record_id = StudentInputCli.input_record_id()
        print()

        try:
            student = self.student_data_access.get_student(record_id)
            print("Студент найден")
            print(student)
        except RecordNotFound:
            print("Студент не найден")

        print()

    def exit(self):
        self._running = False


def main():
    config = get_config()

    injector = DependencyInjector(config, deps_container=DependenciesContainer())
    cli = injector.inject(CliInterface)()

    cli.start()


if __name__ == "__main__":
    main()
