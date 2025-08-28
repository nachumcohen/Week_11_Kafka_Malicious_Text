FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY Preprocessor/ .
COPY clean/ ./clean

CMD ["python3", "main.py"]