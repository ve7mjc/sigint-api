from setuptools import setup, find_packages

setup(
    name="sigint-api",
    version="0.1.0",
    packages=find_packages(include=["common", "common.*"]),
)

