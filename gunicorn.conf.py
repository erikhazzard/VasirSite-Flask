bind = "127.0.0.1:8000"
logfile = "/var/log/gunicorn/vasirsite.log"
pid="/var/run/gunicorn_vasirsite.pid"
workers=3
worker_class='gevent'
