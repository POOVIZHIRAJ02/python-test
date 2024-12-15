# Dockerfile for Python backend
FROM python:3.9

RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade Flask
RUN pip install --upgrade flask-cors
RUN pip install --upgrade werkzeug



COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
