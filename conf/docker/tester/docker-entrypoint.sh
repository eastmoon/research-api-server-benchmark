#!/bin/sh
# vim:sw=4:ts=4:et

set -e

if [ "$1" = "dev" ]; then
    sleep infinity
else
    k6 "$@"
fi
