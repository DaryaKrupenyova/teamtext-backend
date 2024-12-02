FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
RUN apt-get update && apt-get install -y git gcc python3-dev default-libmysqlclient-dev build-essential pkg-config\
    && pip install -r requirements.txt

RUN touch db.sqlite3

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
