#!/bin/bash

echo "Make new migrations"
python manage.py makemigrations

echo "Apply migrations"
python manage.py migrate

echo "Seeding Database"
python manage.py seed_data

echo "Run Server"
python manage.py runserver 0.0.0.0:8000