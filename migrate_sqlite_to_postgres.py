#!/usr/bin/env python
"""Migrate data from SQLite to PostgreSQL"""

import sqlite3
import psycopg2
import os
from datetime import datetime

def migrate_data():
    # Database connections
    sqlite_db = 'db.sqlite3'
    pg_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'storeloop',
        'user': 'postgres',
        'password': 'pushpen3#'
    }
    
    if not os.path.exists(sqlite_db):
        print(f"SQLite database {sqlite_db} not found!")
        return
    
    # Connect to databases
    sqlite_conn = sqlite3.connect(sqlite_db)
    sqlite_conn.row_factory = sqlite3.Row
    
    pg_conn = psycopg2.connect(**pg_config)
    pg_cursor = pg_conn.cursor()
    
    print("Connected to both databases")
    
    # Migrate auth_user
    print("Migrating users...")
    sqlite_cursor = sqlite_conn.execute("SELECT * FROM auth_user")
    users = sqlite_cursor.fetchall()
    
    for user in users:
        user_data = list(user)
        # Convert SQLite integers to PostgreSQL booleans
        user_data[3] = bool(user_data[3])  # is_superuser
        user_data[8] = bool(user_data[8])  # is_staff
        user_data[9] = bool(user_data[9])  # is_active
        # Handle empty datetime fields
        if not user_data[2]:  # last_login
            user_data[2] = None
        if not user_data[10]:  # date_joined
            user_data[10] = datetime.now()
        
        pg_cursor.execute("""
            INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, 
                                 last_name, email, is_staff, is_active, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, tuple(user_data))
    
    # Migrate stores_store
    print("Migrating stores...")
    sqlite_cursor = sqlite_conn.execute("SELECT * FROM stores_store")
    stores = sqlite_cursor.fetchall()
    
    for store in stores:
        store_data = list(store)
        # Convert SQLite integers to PostgreSQL booleans
        store_data[15] = bool(store_data[15])  # onboarding_completed
        store_data[16] = bool(store_data[16])  # is_published
        
        pg_cursor.execute("""
            INSERT INTO stores_store (id, name, slug, logo, description, theme, primary_color,
                                    secondary_color, font_family, custom_domain, subdomain,
                                    razorpay_key_id, razorpay_key_secret, gst_number, business_address,
                                    onboarding_completed, is_published, created_at, updated_at, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, tuple(store_data))
    
    # Migrate stores_product
    print("Migrating products...")
    sqlite_cursor = sqlite_conn.execute("SELECT * FROM stores_product")
    products = sqlite_cursor.fetchall()
    
    for product in products:
        product_data = list(product)
        # Convert SQLite integers to PostgreSQL booleans
        product_data[14] = bool(product_data[14])  # is_active
        
        pg_cursor.execute("""
            INSERT INTO stores_product (id, name, slug, description, short_description, price, stock,
                                      category, image, image_url, material, region, style,
                                      ai_generated_description, is_active, created_at, updated_at, store_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, tuple(product_data))
    
    # Migrate other tables if they exist
    tables_to_migrate = [
        ('stores_order', 'stores_order'),
        ('stores_sellerprofile', 'stores_sellerprofile'),
        ('stores_customer', 'stores_customer'),
        ('stores_useraddress', 'stores_useraddress')
    ]
    
    for sqlite_table, pg_table in tables_to_migrate:
        try:
            sqlite_cursor = sqlite_conn.execute(f"SELECT * FROM {sqlite_table}")
            rows = sqlite_cursor.fetchall()
            
            if rows:
                print(f"Migrating {sqlite_table}...")
                columns = [description[0] for description in sqlite_cursor.description]
                placeholders = ', '.join(['%s'] * len(columns))
                
                for row in rows:
                    pg_cursor.execute(f"""
                        INSERT INTO {pg_table} ({', '.join(columns)})
                        VALUES ({placeholders})
                        ON CONFLICT (id) DO NOTHING
                    """, tuple(row))
        except sqlite3.OperationalError:
            print(f"Table {sqlite_table} not found, skipping...")
    
    # Update sequences
    print("Updating sequences...")
    sequences = [
        ('auth_user', 'auth_user_id_seq'),
        ('stores_store', 'stores_store_id_seq'),
        ('stores_product', 'stores_product_id_seq')
    ]
    
    for table, sequence in sequences:
        pg_cursor.execute(f"SELECT setval('{sequence}', (SELECT MAX(id) FROM {table}) + 1)")
    
    # Commit and close
    pg_conn.commit()
    sqlite_conn.close()
    pg_conn.close()
    
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_data()