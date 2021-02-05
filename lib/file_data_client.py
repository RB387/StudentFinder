from dataclasses import dataclass, field
from typing import Type, List, Iterable, Tuple, TypeVar, Generic

from lib.entities import DataProtocol

EntityType = TypeVar("EntityType", bound=DataProtocol)  # Дженерик


@dataclass
class FileDataClient(Generic[EntityType]):
    """ Клиент для чтения сущностей из файла """
    file_path: str
    # тип сущности, в который записи будут приводится.
    # Должен соответсвовать интерфейсу DataProtocol
    entity_type: Type[EntityType]

    delimiter: str = ","   # разделитель в файле
    new_line: str = "\n"   # символ, обозначабщий новую строку

    _field_names: List[str] = field(default_factory=list, init=False)  # приватное свойство с названиями колонок в файле

    def __post_init__(self):
        with open(self.file_path, "r") as file:
            # Читаем первую линию (это названия колонок)
            # Сначала чистим строку от спец символов, затем разбиваем по разделителю
            self._field_names = (
                file.readline().rstrip(self.new_line).split(self.delimiter)
            )

    def iter_read(self) -> Iterable[Tuple[EntityType, int]]:
        """
            Генератор, итерирующийся по записям в файле
            Отдает сущность и ее позицию в файле
         """
        with open(self.file_path, "r") as file:
            file.readline()  # пропускаем первую строку (это заголовки)
            position = file.tell()  # Запоминаем позицию файла

            while True:  # Читаем пока не дойдем до конца
                line = file.readline()

                if not line:  # если считанной линии нет, значит дошли до конца файла
                    return

                yield self._load_entity(line), position  # десериализованная запись, ее позицию в файле
                position = file.tell()  # обновляем позицию в файле

    def read_at_position(self, position: int) -> EntityType:
        with open(self.file_path, "r") as file:
            file.seek(position)  # перемещаем курсор файла на нужную позицию
            return self._load_entity(file.readline())  # десериализуем считанную линию

    def write(self, entity: EntityType) -> int:
        with open(self.file_path, "a") as file:
            position = file.tell()  # получили текущую позицию в файле
            file.write(self._dump_entity(entity) + self.new_line)  # сериализовали сущность и записали в файл
            return position  # отдаем позицию записи в файле

    def _load_entity(self, raw_line: str) -> EntityType:
        raw_line = raw_line.rstrip(self.new_line)  # очищаем строку от спец символа

        entity_as_dict = {}

        for idx, col in enumerate(raw_line.split(self.delimiter)):  # разбиваем строку по разделителю
            field_name = self._field_names[idx]  # получаем имя столбца
            entity_as_dict[field_name] = col  # кладем в словарь, где ключ - столбец

        return self.entity_type.from_dict(entity_as_dict)  # десериализуем

    def _dump_entity(self, entity: EntityType) -> str:
        raw_data = []
        entity_as_dict = entity.as_dict()  # сериализуем

        for field_name in self._field_names:
            raw_data.append(str(entity_as_dict[field_name]))  # приводим все к строкам в нужном порядке

        return self.delimiter.join(raw_data)  # Все элементы списка конкатенируем разделителем
