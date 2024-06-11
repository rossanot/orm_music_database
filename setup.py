"""Adapted from Real Python 
https://realpython.com/python-sqlite-sqlalchemy/#working-with-sqlalchemy-and-python-objects"""

from setuptools import setup, find_packages

setup(
    name="project",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.2",
        "numpy==1.26.4",
        "SQLAlchemy==1.3.13",
        "pyyaml==6.0.1"
        "kaggle==1.6.12"
    ],
)
