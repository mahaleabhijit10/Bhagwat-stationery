import sqlite3

conn = sqlite3.connect('store.db')
c = conn.cursor()

# PRODUCTS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER,
    image TEXT
)
""")

# CART TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER DEFAULT 1
)
""")

# ORDERS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT,
    phone TEXT,
    address TEXT,
    total INTEGER,
    status TEXT DEFAULT 'Pending'
)
""")

# CLEAR OLD DATA
c.execute("DELETE FROM products")

# 10 PRODUCTS
products = [
    ("Blue Pen", 10, "https://cdn-icons-png.flaticon.com/512/1087/1087840.png"),
    ("Black Pen", 10, "https://cdn-icons-png.flaticon.com/512/1087/1087840.png"),
    ("Notebook", 50, "https://cdn-icons-png.flaticon.com/512/3143/3143460.png"),
    ("Pencil", 5, "https://cdn-icons-png.flaticon.com/512/1087/1087847.png"),
    ("Eraser", 5, "https://cdn-icons-png.flaticon.com/512/2910/2910768.png"),
    ("Sharpener", 8, "https://cdn-icons-png.flaticon.com/512/1041/1041916.png"),
    ("Geometry Box", 120, "https://cdn-icons-png.flaticon.com/512/1670/1670915.png"),
    ("Scale", 15, "https://cdn-icons-png.flaticon.com/512/1828/1828970.png"),
    ("Color Set", 90, "https://cdn-icons-png.flaticon.com/512/3048/3048122.png"),
    ("Marker Pen", 25, "https://cdn-icons-png.flaticon.com/512/1087/1087843.png")
]

c.executemany(
    "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
    products
)

conn.commit()
conn.close()

print("Database ready!")