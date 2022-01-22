#!/bin/bash

echo "Apply migrations"
python manage.py migrate

echo "Run Server"
python manage.py runserver 0.0.0.0:8000