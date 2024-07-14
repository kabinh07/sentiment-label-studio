FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --default-timeout=100 future
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "main.py"]