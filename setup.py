from setuptools import setup, find_packages

import sys
sys.path.append('./camogen')

setup(
    name = "Camogen",
    author="Gael Lederrey",
    license = "MIT License",
    version = "0.1",
    packages = find_packages(),
)
