import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Define database path in datasets/ ---
DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'datasets')
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, 'sales.db')

# Optional: delete existing DB for a clean reset
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# --- 2. Connect to the DB file ---
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- 3. Create table ---
cursor.execute('''
CREATE TABLE sales (
    sale_id INTEGER,
    customer_id INTEGER,
    product TEXT,
    quantity INTEGER,
    price_per_unit REAL,
    sale_date TEXT
)
''')

# --- 4. Insert data ---
sales_data = [
    (1, 101, 'Apple', 2, 0.5, '2023-07-01'),
    (2, 102, 'Banana', 5, 0.2, '2023-07-01'),
    (3, 101, 'Apple', 1, 0.5, '2023-07-02'),
    (4, 103, 'Carrot', 10, 0.1, '2023-07-02'),
    (5, 104, 'Apple', 3, 0.5, '2023-07-03')
]

cursor.executemany('''
INSERT INTO sales (sale_id, customer_id, product, quantity, price_per_unit, sale_date)
VALUES (?, ?, ?, ?, ?, ?)
''', sales_data)

conn.commit()

# --- 5. Query revenue by product ---
query = '''
SELECT 
    product,
    SUM(quantity * price_per_unit) AS total_revenue
FROM sales
GROUP BY product
'''

df = pd.read_sql_query(query, conn)

# --- 6. Print and plot ---
print("Total revenue by product:")
print(df)

plt.bar(df['product'], df['total_revenue'], color='orange')
plt.title('Total Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue (€)')
plt.tight_layout()
plt.show()

# --- 7. Close connection ---
conn.close()