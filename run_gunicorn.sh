#!/bin/bash
#Run gunicorn
PID_FILE=/var/run/gunicorn_vasirsite.pid
WORKERS=2
BIND_ADDRESS=127.0.0.1:8000
WORKER_CLASS=gevent
LOGFILE=/var/log/gunicorn/vasirsite.log

cd /home/erik/Code/VasirSite-Flask/
source /home/erik/Code/VasirSite-Flask/env/bin/activate

gunicorn app:app --pid=$PID_FILE --debug --log-level=debug --workers=$WORKERS --error-logfile=$LOGFILE --bind=$BIND_ADDRESS --worker-class=$WORKER_CLASS
