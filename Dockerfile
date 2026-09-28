FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY config ./config
COPY tests ./tests
COPY pytest.ini .

RUN mkdir -p data/raw data/processed data/dashboard

CMD ["python", "-m", "src.extract"]