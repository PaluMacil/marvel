FROM python:3.8-slim
WORKDIR /app
COPY *.py ./
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y python3-dev libpq-dev gcc && \
    pip3 install -r requirements.txt
ENTRYPOINT ["python", "main.py", "Spectrum"]