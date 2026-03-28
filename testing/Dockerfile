FROM python:3.12-slim

WORKDIR /app

RUN pip install locust bs4

COPY locustfile.py .
COPY test.jpg .

CMD ["locust", "-f", "locustfile.py", "--host=https://felhoalapu-elosztott-rendszerek-laboratorium-django.apps.okd.fured.cloud.bme.hu", "--web-host=0.0.0.0"]