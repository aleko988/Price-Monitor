import psycopg
import os
from dotenv import load_dotenv
from datetime import datetime
from dotenv import load_dotenv
import os

# Load .env from same folder as this file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASE_PUBLIC_URL")
print(f"DB URL: {DATABASE_URL}")
def get_conn():
    return psycopg.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            url TEXT,
            first_seen TEXT,
            last_seen TEXT,
            last_price TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized")

def save_products(products):
    conn = get_conn()
    cursor = conn.cursor()
    
    new_products = []
    price_changes = []
    
    for product in products:
        # Check if product exists
        cursor.execute("SELECT id, price FROM products WHERE id = %s", (product["id"],))
        existing = cursor.fetchone()
        
        if not existing:
            # New product
            cursor.execute("""
                INSERT INTO products (id, title, price, url, first_seen, last_seen, last_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                product["id"],
                product["title"],
                product["price"],
                product["url"],
                product["scraped_at"],
                product["scraped_at"],
                product["price"]
            ))
            new_products.append(product)
        else:
            old_price = existing[1]
            if old_price != product["price"]:
                # Price changed
                cursor.execute("""
                    UPDATE products 
                    SET price = %s, last_seen = %s, last_price = %s
                    WHERE id = %s
                """, (product["price"], product["scraped_at"], old_price, product["id"]))
                price_changes.append({
                    "title": product["title"],
                    "old_price": old_price,
                    "new_price": product["price"],
                    "url": product["url"]
                })
            else:
                # Price same - just update last_seen
                cursor.execute("""
                    UPDATE products SET last_seen = %s WHERE id = %s
                """, (product["scraped_at"], product["id"]))
    
    conn.commit()
    conn.close()
    return new_products, price_changes

def get_all_products():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY first_seen DESC")
    products = cursor.fetchall()
    conn.close()
    return products

if __name__ == "__main__":
    init_db()
    print(f"Total products in database: {len(get_all_products())}")