#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating static directory..."
mkdir -p visualizer/static

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Build completed!"