#!/bin/sh
# vim:sw=4:ts=4:et

set -e

if [ "$1" = "apiserver" ]; then
    if [ -e /usr/local/server/main.py ]; then
        cd /usr/local/server
        gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 2 -b 0.0.0.0:80
    else
        echo "FastAPI entrypoint not find."
    fi
elif [ "$1" = "dev" ]; then
    if [ -e /usr/local/server/main.py ]; then
        cd /usr/local/server
        uvicorn main:app --workers 1 --reload --host 0.0.0.0 --port 8000
    else
        echo "FastAPI entrypoint not find."
    fi
else
    exec "$@"
fi
