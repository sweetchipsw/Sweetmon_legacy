#!/bin/sh
echo "Starting ..."

echo ">> Deleting old migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete


# Optional
echo ">> Deleting database"
find . -name "db.sqlite3" -delete

echo ">> Running manage.py makemigrations"
python manage.py makemigrations

echo ">> Running manage.py migrate"
python manage.py migrate

echo ">> Done"
