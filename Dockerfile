FROM python:3.15-rc

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PGHOST=database \
    PGPORT=5432 \
    PORT=5003

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services ./services
COPY app.py .

EXPOSE 5003

CMD ["python", "app.py"]

