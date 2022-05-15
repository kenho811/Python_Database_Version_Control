"""Minimal setup file for tasks project."""

from typing import List, Dict
from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='database_version_control',
    version='0.1.3',
    license='proprietary',
    python_requires='>=3.7.*',
    description='A library for doing database version control',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ken Ho',
    author_email='kenho811@gmail.com',
    url='https://github.com/kenho811/Python_Database_Version_Control/tree/release',
    packages=(find_packages(where="src")),
    package_dir={"": "src"},
    # Include SQL files (seen as data by setup tools)
    package_data={'': ['*.sql']},
    include_package_data=True,
    install_requires=[
        'psycopg2',
        'typer[all]',
        'pyyaml',
    ],
    extras_require={
            'dev': [
                'pytest',
                'sphinx',
            ]
    },
    entry_points='''
    [console_scripts]
    dvc=dvc.app.cli:app
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
