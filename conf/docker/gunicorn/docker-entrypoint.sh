#!/bin/sh
# vim:sw=4:ts=4:et

set -e

if [ "$1" = "apiserver" ]; then
    if [ -e /usr/local/server/main.py ]; then
        cd /usr/local/server
        gunicorn main:app --workers 2 --reload -b 0.0.0.0:80
    else
        echo "Flask entrypoint not find."
    fi
else
    exec "$@"
fi
