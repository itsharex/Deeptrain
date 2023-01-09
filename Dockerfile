FROM python:3.7

ENV PYTHONUNBUFFERED 1

MAINTAINER zmh-program

RUN mkdir /opt/Zh-Website
WORKDIR /opt/Zh-Website
ADD . /opt/Zh-Website

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN /usr/local/bin/python -m pip install --upgrade pip \
  && pip install opencv-python-headless \
  && pip install -r requirements.txt -i https://pypi.douban.com/simple/
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000 8000

CMD ["python", "manage.py", "runserver"]
