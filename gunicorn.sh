#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/VasirSite-Flask.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=your_unix_user
GROUP=your_unix_group
#source ../bin/activate
. env/bin/activate
exec gunicorn app:app -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
