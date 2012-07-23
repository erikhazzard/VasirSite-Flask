bind = "127.0.0.1:8000"
logfile = "/var/log/gunicorn/vasirsite.log"
workers=3
worker_class='gevent'
