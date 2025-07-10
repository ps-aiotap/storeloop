#!/bin/bash

echo "========================================"
echo "StoreLoop 1-Click Deployment Script"
echo "========================================"
echo

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "ERROR: manage.py not found. Please run this script from the StoreLoop root directory."
    exit 1
fi

echo "[1/8] Reading configuration and checking local PostgreSQL..."
# Read database settings from .env file
DB_PASSWORD="postgres"
DB_NAME="storeloop"
DB_USER="postgres"
DB_PORT="5432"
if [ -f ".env" ]; then
    export $(grep -E '^(DB_PASSWORD|DB_NAME|DB_USER|DB_PORT)=' .env | xargs)
fi
echo "Using local PostgreSQL with DB: $DB_NAME, User: $DB_USER, Port: $DB_PORT"

echo
echo "[2/8] Checking PostgreSQL connection..."
echo "Please ensure PostgreSQL is running locally on port $DB_PORT"

echo
echo "[3/8] Activating virtual environment..."
if [ -f "storeloop-venv/bin/activate" ]; then
    source storeloop-venv/bin/activate
else
    echo "WARNING: Virtual environment not found. Using system Python."
fi

echo
echo "[4/8] Installing/updating dependencies..."
pip install -r requirements.txt --quiet

echo
echo "[5/8] Setting up database..."
python manage.py makemigrations
python manage.py migrate

echo
echo "[6/8] Creating admin user and sample data..."
python manage.py reset_admin
python manage.py seed_sample_data --users 2 --stores 3 --products 8

echo
echo "[7/8] Starting Celery worker in background..."
celery -A core worker --loglevel=info &

echo
echo "[8/8] Starting Django development server..."
echo
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo
echo "Access your application at:"
echo "- Main site: http://localhost:8000"
echo "- Admin: http://localhost:8000/admin"
echo "- Login: admin / admin123"
echo "- PostgreSQL: $DB_NAME on localhost:$DB_PORT (User: $DB_USER)"
echo
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo

python manage.py runserver