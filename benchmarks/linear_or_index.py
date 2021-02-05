import random
from time import time

from lib.data_access import (
    FileStudentDataAccess,
    StudentDataAccessProtocol,
    IndexFileStudentDataAccess,
)
from lib.entities import Student, PrimaryKey
from lib.file_data_client import FileDataClient

ID_TO_FIND = PrimaryKey(673)

BENCHMARK_ITERATIONS_COUNT = 100
BENCHMARK_FILE_PATH = "benchmark_data.txt"
BENCHMARK_RESULTS_FILE_PATH = "benchmark_results.txt"


def benchmark(data_access_object: StudentDataAccessProtocol) -> float:
    start_time = time()

    for _ in range(BENCHMARK_ITERATIONS_COUNT):
        data_access_object.get_student(ID_TO_FIND)

    finish_time = time()

    return finish_time - start_time


def main():
    file_client = FileDataClient(BENCHMARK_FILE_PATH, entity_type=Student)

    linear_dao = FileStudentDataAccess(file_client)
    index_dao = IndexFileStudentDataAccess(file_client)

    with open(BENCHMARK_RESULTS_FILE_PATH, "w") as file:
        print("Benchmark test", file=file)
        print("\n", file=file)
        print(f"Test iterations count: {BENCHMARK_ITERATIONS_COUNT}", file=file)
        print("\n", file=file)
        print(f"Linear search result: {benchmark(linear_dao)} seconds", file=file)
        print(f"Index search result: {benchmark(index_dao)} seconds", file=file)


if __name__ == "__main__":
    main()
