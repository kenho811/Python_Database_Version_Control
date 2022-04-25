"""Minimal setup file for tasks project."""

from typing import List, Dict
from setuptools import find_packages, setup


setup(
    name='database_version_control',
    version='0.1.1',
    license='proprietary',
    python_requires='>=3.7.*',
    description='A library for doing database version control',
    author='Ken Ho',
    author_email='kenho811@gmail.com',
    url='N/A',
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
                'pytest-mock',
                'sphinx',
            ]
    },
    entry_points='''
    [console_scripts]
    dvc=dvc.app.cli:app
    ''',
)
