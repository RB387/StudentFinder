import setuptools

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="student_finder",
    version="0.1.0",
    author="Nikita Zavadin",
    author_email="zavadin142@gmail.com",
    description="Лабораторная работа",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="https://github.com/RB387/StudentFinder",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=requirements,
    python_requires=">=3.8",
)
