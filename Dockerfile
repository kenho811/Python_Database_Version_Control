FROM python:3.10

WORKDIR /usr/src/app

# Install the tool
COPY ./src ./src
COPY ./setup.cfg ./setup.cfg
COPY ./setup.py ./setup.py
COPY ./README.md ./README.md

RUN pip install .

# other commands

ENTRYPOINT ["dvc"]