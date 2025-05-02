FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# COPY backend/ /app/
COPY ./backend/requirements/development.txt /app/requirements/development.txt

RUN pip install --upgrade pip && pip install -r /app/requirements/development.txt

# gunicornのインストールは requirements に含めてください

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
