FROM python:3-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY code/requirements.txt /code/

RUN apk add build-base
RUN apk add libffi-dev
RUN apk add opus-tools
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

RUN apk add  --no-cache ffmpeg

COPY . /code/

EXPOSE 8080