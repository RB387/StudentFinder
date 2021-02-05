import re
from datetime import date

from lib.entities import PrimaryKey


class StudentInputCli:
    @staticmethod
    def input_record_id() -> PrimaryKey:
        while True:
            print("Введите номер зачетной книжки: ", end="")

            try:
                return PrimaryKey(input())
            except ValueError:
                print("Некорректный формат номера. Введите целое число")

    @staticmethod
    def input_first_name() -> str:
        while True:
            print("Введите имя студента: ", end="")

            result = re.compile("[а-яА-Я]+$").match(input())

            if result is None:
                print("Имя может содержать только буквы из русского алфавита")
            else:
                return result.string

    @staticmethod
    def input_last_name() -> str:
        while True:
            print("Введите фамилию студента: ", end="")

            result = re.compile("[а-яА-Я]+$").match(input())

            if result is None:
                print("Фамилия может содержать только буквы из русского алфавита")
            else:
                return result.string

    @staticmethod
    def input_birthday() -> str:
        while True:
            print("Введите день рождения студента в формате YYYY-MM-DD: ", end="")

            try:
                return date.fromisoformat(input()).isoformat()
            except ValueError:
                print("Неверный формат даты")
