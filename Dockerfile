FROM python:latest
RUN pip install pipenv
WORKDIR /app/
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy
COPY . /app/