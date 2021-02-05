from dataclasses import dataclass, field
from typing import Type, List, Iterable, Tuple, TypeVar, Generic

from lib.entities import DataProtocol

EntityType = TypeVar("EntityType", bound=DataProtocol)


@dataclass
class FileDataClient(Generic[EntityType]):
    file_path: str
    entity_type: Type[EntityType]

    delimiter: str = ","
    new_line: str = "\n"

    _field_names: List[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        with open(self.file_path, "r") as file:
            self._field_names = (
                file.readline().rstrip(self.new_line).split(self.delimiter)
            )

    def iter_read(self) -> Iterable[Tuple[EntityType, int]]:
        with open(self.file_path, "r") as file:
            file.readline()
            position = file.tell()

            while True:
                line = file.readline()

                if not line:
                    return

                yield self._load_entity(line), position
                position = file.tell()

    def read_at_position(self, position: int) -> EntityType:
        with open(self.file_path, "r") as file:
            file.seek(position)
            return self._load_entity(file.readline())

    def write(self, entity: EntityType) -> int:
        with open(self.file_path, "a") as file:
            position = file.tell()
            file.write(self._dump_entity(entity) + self.new_line)
            return position

    def _load_entity(self, raw_line: str) -> EntityType:
        raw_line = raw_line.rstrip(self.new_line)

        entity_as_dict = {}

        for idx, col in enumerate(raw_line.split(self.delimiter)):
            field_name = self._field_names[idx]
            entity_as_dict[field_name] = col

        return self.entity_type.from_dict(entity_as_dict)

    def _dump_entity(self, entity: EntityType) -> str:
        raw_data = []
        entity_as_dict = entity.as_dict()

        for field_name in self._field_names:
            raw_data.append(str(entity_as_dict[field_name]))

        return self.delimiter.join(raw_data)
