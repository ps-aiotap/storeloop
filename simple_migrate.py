#!/usr/bin/env python
"""Simple SQLite to PostgreSQL migration"""

import sqlite3
import psycopg2
from datetime import datetime

def migrate_data():
    # Connect to SQLite
    sqlite_conn = sqlite3.connect('db.sqlite3')
    sqlite_conn.row_factory = sqlite3.Row
    
    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='storeloop',
        user='postgres',
        password='pushpen3#'
    )
    pg_cursor = pg_conn.cursor()
    
    print("Migrating data...")
    
    # Clear existing data
    pg_cursor.execute("TRUNCATE auth_user CASCADE")
    pg_cursor.execute("TRUNCATE stores_store CASCADE")
    pg_cursor.execute("TRUNCATE stores_product CASCADE")
    
    # Migrate users with safe defaults
    sqlite_cursor = sqlite_conn.execute("SELECT * FROM auth_user")
    for user in sqlite_cursor.fetchall():
        pg_cursor.execute("""
            INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, 
                                 last_name, email, is_staff, is_active, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user['id'],
            user['password'],
            None if not user['last_login'] else user['last_login'],
            bool(user['is_superuser']),
            user['username'],
            user['first_name'],
            user['last_name'],
            user['email'],
            bool(user['is_staff']),
            bool(user['is_active']),
            datetime.now() if not user['date_joined'] or user['date_joined'] == 'Store' else user['date_joined']
        ))
    
    # Migrate stores
    sqlite_cursor = sqlite_conn.execute("SELECT * FROM stores_store")
    for store in sqlite_cursor.fetchall():
        pg_cursor.execute("""
            INSERT INTO stores_store (id, name, slug, logo, description, theme, primary_color,
                                    secondary_color, font_family, custom_domain, subdomain,
                                    razorpay_key_id, razorpay_key_secret, gst_number, business_address,
                                    onboarding_completed, is_published, created_at, updated_at, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            store['id'], store['name'], store['slug'], store['logo'], store['description'],
            store['theme'], store['primary_color'], store['secondary_color'], store['font_family'],
            store['custom_domain'], store['subdomain'], store['razorpay_key_id'], store['razorpay_key_secret'],
            store['gst_number'], store['business_address'], bool(store['onboarding_completed']),
            bool(store['is_published']), store['created_at'], store['updated_at'], store['owner_id']
        ))
    
    # Migrate products
    sqlite_cursor = sqlite_conn.execute("SELECT * FROM stores_product")
    for product in sqlite_cursor.fetchall():
        pg_cursor.execute("""
            INSERT INTO stores_product (id, name, slug, description, short_description, price, stock,
                                      category, image, image_url, material, region, style,
                                      ai_generated_description, is_active, created_at, updated_at, store_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            product['id'], product['name'], product['slug'], product['description'], product['short_description'],
            product['price'], product['stock'], product['category'], product['image'], product['image_url'],
            product['material'], product['region'], product['style'], product['ai_generated_description'],
            bool(product['is_active']), product['created_at'], product['updated_at'], product['store_id']
        ))
    
    # Update sequences
    pg_cursor.execute("SELECT setval('auth_user_id_seq', (SELECT MAX(id) FROM auth_user) + 1)")
    pg_cursor.execute("SELECT setval('stores_store_id_seq', (SELECT MAX(id) FROM stores_store) + 1)")
    pg_cursor.execute("SELECT setval('stores_product_id_seq', (SELECT MAX(id) FROM stores_product) + 1)")
    
    pg_conn.commit()
    sqlite_conn.close()
    pg_conn.close()
    
    print("Migration completed!")

if __name__ == "__main__":
    migrate_data()