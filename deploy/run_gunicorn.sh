#!/bin/bash
#Run gunicorn
PID_FILE=/var/run/gunicorn_vasirsite.pid
. env/bin/activate
cd /home/erik/Code/VaisrSite-Flask/
gunicorn app:app -c /home/erik/Code/VasirSite-Flask/deploy/gunicorn.conf.py --pid=$PID_FILE
