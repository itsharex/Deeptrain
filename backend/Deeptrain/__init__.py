import pymysql
from .celery import app

pymysql.install_as_MySQLdb()
__all__ = ['app']
