import os
import sys

from lib.data_access import StudentDataAccessProtocol, IndexFileStudentDataAccess
from lib.entities import Student
from lib.file_data_client import FileDataClient


def get_config():
    """ Конфиг зависимостей """
    path = getattr(sys, '_MEIPASS', os.getcwd())
    return {
        # Конфиг зависимости
        FileDataClient: {
            "file_path": os.path.join(path, "students.txt"),
            "entity_type": Student,
        },
        # Бинд провайдера
        StudentDataAccessProtocol: IndexFileStudentDataAccess,
    }
