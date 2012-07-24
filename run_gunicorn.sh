#!/bin/bash
#Run gunicorn
PID_FILE=/var/run/gunicorn_vasirsite.pid
. env/bin/activate
gunicorn app:app -c /home/erik/Code/VasirSite-Flask/gunicorn.conf.py --pid=$PID_FILE
