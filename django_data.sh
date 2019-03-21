#!/bin/bash

# This bash script cleans out migrations, reruns them, and runs seeder file to fill database with fake data

find ./$1/migrations/ -type f -name "*.py" -delete; #deletes all of the .py files in the migrations directory except for the __init__.py file.
find ./$1/migrations/ -type f -name "*.pyc" -delete; #deletes all of the .pyc files in the migrations directory.
rm db.sqlite3; #deletes the database file.
python manage.py makemigrations $1; #creates the migration.
python manage.py migrate; #runs the migration.
python manage.py loaddata $2 #runs the file we created above to seed the new db