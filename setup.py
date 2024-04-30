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
        "Flask==1.1.1",
        "SQLAlchemy==1.3.13",
        "Flask-SQLAlchemy==2.4.1",
        "Flask-Cors==3.0.8",
        "Flask-Bootstrap4==4.0.2",
        "Flask-WTF==0.14.3",
        "python-dateutil==2.9",
        "python-dotenv==0.10.5",
        "treelib",
        "requests==2.31.0"
        "pyyaml==6.0.1"
        "kaggle==1.6.12"
    ],
)
