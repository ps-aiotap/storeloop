#!/usr/bin/env python
"""Migrate data from SQLite to PostgreSQL"""

import os
import sys
import django
import sqlite3
import psycopg2
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Temporarily force SQLite to read data
os.environ['USE_SQLITE'] = 'True'
django.setup()

def migrate_data():
    """Migrate all data from SQLite to PostgreSQL"""
    
    # Read data from SQLite
    from django.contrib.auth.models import User
    from stores.models import Store, Product, Order, SellerProfile, Customer, UserAddress
    
    print("Reading data from SQLite...")
    
    # Get all data
    users = list(User.objects.all().values())
    stores = list(Store.objects.all().values())
    products = list(Product.objects.all().values())
    orders = list(Order.objects.all().values())
    profiles = list(SellerProfile.objects.all().values())
    customers = list(Customer.objects.all().values())
    addresses = list(UserAddress.objects.all().values())
    
    print(f"Found: {len(users)} users, {len(stores)} stores, {len(products)} products")
    
    # Switch to PostgreSQL
    os.environ['USE_SQLITE'] = 'False'
    
    # Reload Django settings
    from importlib import reload
    from django.conf import settings
    reload(sys.modules['core.settings'])
    django.setup()
    
    print("Switching to PostgreSQL and inserting data...")
    
    # Clear existing data
    User.objects.all().delete()
    
    # Insert users first
    for user_data in users:
        User.objects.create(**user_data)
    
    # Insert stores
    for store_data in stores:
        Store.objects.create(**store_data)
    
    # Insert products
    for product_data in products:
        Product.objects.create(**product_data)
    
    # Insert other data
    for profile_data in profiles:
        SellerProfile.objects.create(**profile_data)
    
    for customer_data in customers:
        Customer.objects.create(**customer_data)
    
    for address_data in addresses:
        UserAddress.objects.create(**address_data)
    
    for order_data in orders:
        Order.objects.create(**order_data)
    
    print("Data migration completed!")
    print(f"PostgreSQL now has: {User.objects.count()} users, {Store.objects.count()} stores, {Product.objects.count()} products")

if __name__ == "__main__":
    migrate_data()