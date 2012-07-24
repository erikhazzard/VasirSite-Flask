#!/bin/bash
#Run gunicorn
PID_FILE=/var/run/gunicorn_vasirsite.pid

cd ../
. env/bin/activate
gunicorn app:app -c deploy/gunicorn.conf.py --pid=$PID_FILE
