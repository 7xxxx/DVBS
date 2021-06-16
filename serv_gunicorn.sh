#!/bin/sh
#call this script without parameters to start gunicorn webserver as daemons
#call this script with parameter kill to terminate the daemons

if [ $# -eq 0 ]; then
#  "${PWD}"/venv/bin/gunicorn -D -w 2 --bind 0.0.0.0:443 --certfile=cert/bookstore.pem --key=cert/bookstore.key "app:create_app()"
#  "${PWD}"/venv/bin/gunicorn -D -w 2 --bind 0.0.0.0:80 "app:create_app()"
  gunicorn -D -w 2 --bind 0.0.0.0:443 --certfile=cert/bookstore.pem --key=cert/bookstore.key "app:create_app()"
  gunicorn -D -w 2 --bind 0.0.0.0:80 "app:create_app()"
fi

sleep 1

if [ "$1" = "kill" ] ; then
  for pid in $(pgrep gunicorn) ; do
    kill "$pid"
  done
fi
