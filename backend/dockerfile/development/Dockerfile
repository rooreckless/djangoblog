FROM python:3.12-slim

# Pythonが .pyc ファイル（バイトコードキャッシュ）を生成しないようにする
ENV PYTHONDONTWRITEBYTECODE=1
# Pythonの出力をバッファリングしない（= 常に即時出力する=docker logsに即時反映される）
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./backend/requirements/development.txt /app/requirements/development.txt

RUN pip install --upgrade pip && pip install -r /app/requirements/development.txt

# gunicornのインストールは requirements に含めてください

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
