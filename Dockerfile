# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install build
RUN python -m build
RUN pip install dist/*.whl

ENTRYPOINT ["octosuite"]
