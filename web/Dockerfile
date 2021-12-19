FROM python:3.8

ADD app.py .

WORKDIR /app

COPY requirements.txt /app
COPY app.py /app
COPY config.py /app
COPY templates /app/templates
COPY static /app/static

RUN pip install -r requirements.txt

CMD ["python", "./app.py"]