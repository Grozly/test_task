FROM python:3.10.0-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./app /code/app
COPY ./main.py /code/main.py
CMD ["python", "main.py"]