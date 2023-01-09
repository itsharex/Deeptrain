FROM python:3.7

ENV PYTHONUNBUFFERED 1

MAINTAINER zmh-program

RUN mkdir /opt/Zh-Website
WORKDIR /opt/Zh-Website
ADD . /opt/Zh-Website


RUN /usr/local/bin/python -m pip install --upgrade pip \
  && pip install -r requirements.txt -i https://pypi.douban.com/simple/ \
  && python manage.py collectstatic --noinput \
  && python manage.py makemigrations \
  && python manage.py migrate
EXPOSE 8000 8000

CMD ["python", "manage.py", "runserver"]
