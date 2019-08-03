FROM python:3.7-stretch
ENV PYTHONUNBUFFERED 1
ENV REDIS_URL "redis"
RUN mkdir /selfies
WORKDIR /selfies
ADD . /selfies/
RUN pip install -r requirements.txt
