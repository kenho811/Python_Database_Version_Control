#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Setup.py for the DVC project."""


from setuptools import find_packages, setup
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('src/dvc/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='database_version_control',
    version=main_ns['__version__'],
    license='Apache License 2.0',
    python_requires='>=3.7.*',
    description='Version control your database!',
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
                'pytest-cov',
                'pytest-docker',
                'pytest-html',
                'pytest-html',
                'sphinx',
                'pyinstaller',
                'flake8',
            ]
    },
    entry_points={
        'console_scripts': [
            'dvc=dvc.app.cli.main:app',
        ]
    },
)
