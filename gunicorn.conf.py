from gevent import monkey
from multiprocessing import cpu_count
monkey.patch_all()

bind = "0.0.0.0:8000"
workers = cpu_count() * 2 + 1
threads = cpu_count() * 2
backlog = 4096
worker_class = "sync"
worker_connections = 1000
timeout = 180
