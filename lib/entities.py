from dataclasses import dataclass, asdict
from typing import Dict, Any, Protocol


class PrimaryKey(int):
    """ Тип данных, обозначающий первичный ключ """
    ...


@dataclass
class DataProtocol(Protocol):
    """ Интерфейс для сущностей """
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataProtocol":
        """ сериализация """
        ...

    def as_dict(self) -> Dict[str, Any]:
        """ десериализация """
        ...


@dataclass
class Student(DataProtocol):
    """ Реализация интерфейса DataProtocol для сущности студента """
    record_id: PrimaryKey
    first_name: str
    last_name: str
    birthday_date: str

    def __str__(self):
        """ Строчное представление сущности """
        return f'Номер зачетной книжки: {self.record_id}\n' \
               f'Имя: {self.first_name}\n' \
               f'Фамилия: {self.last_name}\n' \
               f'Дата рождения: {self.birthday_date}\n'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        return cls(
            record_id=PrimaryKey(data["record_id"]),
            first_name=data["first_name"],
            last_name=data["last_name"],
            birthday_date=data["birthday_date"],
        )

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)
