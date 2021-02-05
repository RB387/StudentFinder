from lib.data_access import StudentDataAccessProtocol, IndexFileStudentDataAccess
from lib.entities import Student
from lib.file_data_client import FileDataClient


def get_config():
    """ Конфиг зависимостей """
    return {
        # Конфиг зависимости
        FileDataClient: {
            "file_path": "test.txt",
            "entity_type": Student,
        },
        # Бинд провайдера
        StudentDataAccessProtocol: IndexFileStudentDataAccess,
    }
