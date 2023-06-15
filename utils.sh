#!/bin/bash

function setup_migrations() {
  python manage.py makemigrations
}

function migrate() {
  python manage.py migrate
}

function run_server() {
  python manage.py runserver
}

case "$1" in
  "setup")
    setup_migrations
    ;;
  "migrate")
    migrate
    ;;
  "run")
    run_server
    ;;
  *)
    echo "Usage: $0 {setup_migrations|migrate|run}"
    exit 1
    ;;
esac