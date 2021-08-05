#!/bin/sh
#call this script without parameters to start gunicorn webserver as daemons
#call this script with parameter kill to terminate the daemons

if [ $# -eq 0 ]; then
  export SECRET_KEY=$(head -c 500 /dev/urandom | tr -dc 'a-zA-Z0-9~!@#$%^&*_-' | head -c 16)
  echo "SECRET_KEY = $SECRET_KEY"
  "${PWD}"/venv/bin/gunicorn -D -w 2 --bind 0.0.0.0:443 --certfile=cert/bookstore.pem --key=cert/bookstore.key "app:create_app()"
  "${PWD}"/venv/bin/gunicorn -D -w 2 --bind 0.0.0.0:80 "app:create_app()"
fi

if [ "$1" = "kill" ] ; then
  for pid in $(pgrep gunicorn) ; do
    kill "$pid"
  done
fi
