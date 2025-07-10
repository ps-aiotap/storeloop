#!/usr/bin/env python
"""Fix database issues by creating a fresh SQLite database"""

import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from django.core.management import call_command

def fix_database():
    """Create a fresh SQLite database"""
    
    # Close any existing connections
    connection.close()
    
    # Wait for connections to close
    time.sleep(2)
    
    # Try to delete the database file
    try:
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
            print("Removed existing database")
    except Exception as e:
        print(f"Could not remove database: {e}")
        print("Please stop the Django server and try again")
        return False
    
    # Run migrations
    print("Running migrations...")
    call_command('migrate')
    
    # Create superuser
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    
    # Create sample data
    print("Creating sample data...")
    try:
        call_command('seed_sample_data', users=2, stores=3, products=8)
    except Exception as e:
        print(f"Could not create sample data: {e}")
        print("Continuing without sample data")
    
    print("\nDatabase setup complete!")
    print("You can now login with:")
    print("  Username: admin")
    print("  Password: admin123")
    
    return True

if __name__ == "__main__":
    fix_database()