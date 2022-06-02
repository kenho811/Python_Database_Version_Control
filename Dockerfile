FROM python:3.10

WORKDIR /usr/src/app

# Install psql CLI
USER root
RUN apt-get update && apt-get install --assume-yes postgresql

# Install the tool
COPY ./src ./src
COPY ./setup.py ./setup.py
COPY ./README.md ./README.md

RUN pip install .

# other commands

CMD tail -f /dev/null