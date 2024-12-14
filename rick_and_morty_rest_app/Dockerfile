FROM python:3

MAINTAINER Matan Moshe

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN echo ${BUILD_NUMBER} && pip install --no-cache-dir -r requirements.txt

EXPOSE 5010

ARG BUILD_NUMBER
ENV ENVIRONMENT=DEV

ENTRYPOINT ["python", "app.py"]
