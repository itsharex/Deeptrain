FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV CONTAINER 1

MAINTAINER zmh-program

RUN mkdir /opt/Zh-Website
WORKDIR /opt/Zh-Website
ADD . /opt/Zh-Website


COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip \
  && pip3 install -r requirements.txt -i https://pypi.douban.com/simple/ \
  && python manage.py collectstatic --noinput \
  && python manage.py makemigrations \
  && python manage.py migrate
COPY . .
EXPOSE 80 8000
