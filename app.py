from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- HOME ----------------
@app.route('/')
def home():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template('index.html', products=products)

# ---------------- ADD TO CART ----------------
@app.route('/add/<int:id>')
def add_to_cart(id):
    db = get_db()
    db.execute("INSERT INTO cart (product_id, user_id) VALUES (?, ?)", (id, 1))
    db.commit()
    return redirect('/cart')

# ---------------- CART ----------------
@app.route('/cart')
def cart():
    db = get_db()

    items = db.execute("""
        SELECT products.name, products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
    """).fetchall()

    total = sum(i['price'] for i in items)
    return render_template('cart.html', cart=items, total=total)

# ---------------- CHECKOUT (COD ONLY) ----------------
@app.route('/checkout', methods=['POST'])
def checkout():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']

    db = get_db()

    items = db.execute("""
        SELECT products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
    """).fetchall()

    total = sum(i['price'] for i in items)

    db.execute("""
        INSERT INTO orders (customer_name, phone, address, total, status)
        VALUES (?, ?, ?, ?, ?)
    """, (name, phone, address, total, "Pending"))

    db.execute("DELETE FROM cart")
    db.commit()

    return "<h2>✅ Order Placed Successfully (COD)</h2>"

# ---------------- ADMIN PANEL ----------------
@app.route('/admin')
def admin():
    db = get_db()
    orders = db.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    return render_template('admin.html', orders=orders)

# ---------------- MARK DELIVERED ----------------
@app.route('/deliver/<int:id>')
def deliver(id):
    db = get_db()
    db.execute("UPDATE orders SET status='Delivered' WHERE id=?", (id,))
    db.commit()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)