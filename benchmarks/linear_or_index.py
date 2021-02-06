import random
from time import time

from lib.data_access import (
    FileStudentDataAccess,
    StudentDataAccessProtocol,
    IndexFileStudentDataAccess,
)
from lib.entities import Student, PrimaryKey
from lib.file_data_client import FileDataClient


FILE_SIZES = [500, 1000, 5000]
BENCHMARK_ITERATIONS_COUNT = 100
BENCHMARK_FILE_PATH_TEMPLATE = "benchmark_data_size_{size}.txt"
BENCHMARK_RESULTS_FILE_PATH_TEMPLATE = "benchmark_results_{size}.txt"


def benchmark(data_access_object: StudentDataAccessProtocol, id_to_find: PrimaryKey) -> float:
    start_time = time()

    for _ in range(BENCHMARK_ITERATIONS_COUNT):
        data_access_object.get_student(id_to_find)

    finish_time = time()

    return finish_time - start_time


def run_benchmark(size: int):
    file_client = FileDataClient(BENCHMARK_FILE_PATH_TEMPLATE.format(size=size), entity_type=Student)

    linear_dao = FileStudentDataAccess(file_client)
    index_dao = IndexFileStudentDataAccess(file_client)
    id_to_find = PrimaryKey(size - 1)

    with open(BENCHMARK_RESULTS_FILE_PATH_TEMPLATE.format(size=size), "w") as file:
        print("Benchmark test", file=file)
        print("\n", file=file)
        print(f"Test iterations count: {BENCHMARK_ITERATIONS_COUNT}", file=file)
        print(f"File size: {size}. Trying to find last student", file=file)
        print("\n", file=file)
        print(f"Linear search result: {benchmark(linear_dao, id_to_find)} seconds", file=file)
        print(f"Index search result: {benchmark(index_dao, id_to_find)} seconds", file=file)


if __name__ == "__main__":
    for size in FILE_SIZES:
        run_benchmark(size)
