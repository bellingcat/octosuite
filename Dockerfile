# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install build && python -m build
RUN pip install dist/*.whl

ENTRYPOINT ["octosuite"]
