#/bin/bash
if [ -z ${PG_PORT+x} ]; then PORT=5432; else  PORT=$PG_PORT; fi

psql -p $PORT -c 'drop database devjektest;'
psql -p $PORT -c 'create database devjektest;'

export DB_URI=postgresql://localhost:$PORT/devjektest
export APP_ENV=test

python manage.py db upgrade

if [ $# -eq 0 ]
  then
    nosetests unit_tests/
else
    nosetests $1
fi
