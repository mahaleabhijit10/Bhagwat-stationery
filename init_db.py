import sqlite3

conn = sqlite3.connect('store.db')
c = conn.cursor()

c.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)')
c.execute('CREATE TABLE cart (id INTEGER PRIMARY KEY, product_id INTEGER)')
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')

# Sample Products
c.execute("INSERT INTO products (name, price) VALUES ('Pen', 10)")
c.execute("INSERT INTO products (name, price) VALUES ('Notebook', 50)")
c.execute("INSERT INTO products (name, price) VALUES ('Pencil', 5)")

conn.commit()
conn.close()