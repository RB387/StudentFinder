from dataclasses import dataclass, asdict
from typing import Dict, Any


class PrimaryKey(int):
    ...


@dataclass
class Student:
    record_id: PrimaryKey
    first_name: str
    last_name: str
    birthday_date: str

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
