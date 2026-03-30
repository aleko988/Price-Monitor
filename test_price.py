import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(os.getenv("DATABASE_PUBLIC_URL"))
cursor = conn.cursor()
cursor.execute("UPDATE products SET price = '£10.00' WHERE title = 'Tipping the Velvet'")
conn.commit()
conn.close()
print("Price updated")