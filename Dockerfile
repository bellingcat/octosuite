# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /app

COPY . .

RUN python setup.py sdist bdist_wheel
RUN pip install dist/*.whl

ENTRYPOINT ["octosuite"]


