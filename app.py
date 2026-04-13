from flask import Flask, render_template, request, redirect
import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- EMAIL ----------------
def send_email_admin(name, phone, address, total):
    sender = "mahaleabhijit10@gmail.com"
    password = "pykl rsti ksxq cwpw"
    receiver = "mahaleabhijit10@gmail.com"

    subject = "🛒 New Order Received"

    body = f"""
NEW ORDER

Name: {name}
Phone: {phone}
Address: {address}
Total: ₹{total}
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

# ---------------- SMS ----------------
def send_sms_admin(message):
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "v3",
        "sender_id": "TXTIND",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": "919518381046"
    }

    headers = {
        "authorization": "WZQyX8DqR0hnv92mja5xTf4iGECIJowuBNsM7b1ctOkVrzFg3KNVOtLcu8dMKXmJxBe49kaY0A7fCDQs",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    requests.post(url, headers=headers, data=payload)

# ---------------- HOME ----------------
@app.route('/')
def home():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("index.html", products=products)

# ---------------- ADD TO CART ----------------
@app.route('/add/<int:id>')
def add_to_cart(id):
    db = get_db()

    item = db.execute("SELECT * FROM cart WHERE product_id=?", (id,)).fetchone()

    if item:
        db.execute("UPDATE cart SET quantity = quantity + 1 WHERE product_id=?", (id,))
    else:
        db.execute("INSERT INTO cart (product_id, quantity) VALUES (?, ?)", (id, 1))

    db.commit()
    return redirect('/cart')

# ---------------- CART ----------------
@app.route('/cart')
def cart():
    db = get_db()

    items = db.execute("""
        SELECT cart.id, products.name, products.price, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
    """).fetchall()

    total = sum(i['price'] * i['quantity'] for i in items)

    return render_template("cart.html", cart=items, total=total)

# ---------------- REMOVE ----------------
@app.route('/remove/<int:id>')
def remove(id):
    db = get_db()
    db.execute("DELETE FROM cart WHERE id=?", (id,))
    db.commit()
    return redirect('/cart')

# ---------------- CHECKOUT ----------------
@app.route('/checkout', methods=['POST'])
def checkout():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']

    db = get_db()

    items = db.execute("""
        SELECT products.price, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
    """).fetchall()

    total = sum(i['price'] * i['quantity'] for i in items)

    db.execute("""
        INSERT INTO orders (customer_name, phone, address, total, status)
        VALUES (?, ?, ?, ?, ?)
    """, (name, phone, address, total, "Pending"))

    db.execute("DELETE FROM cart")
    db.commit()

    # ---------------- NOTIFICATIONS ----------------
    send_email_admin(name, phone, address, total)

    sms_msg = f"""
NEW ORDER
Name: {name}
Phone: {phone}
Total: ₹{total}
"""

    send_sms_admin(sms_msg)

    return render_template("order_success.html", name=name, total=total)

# ---------------- ADMIN LOGIN ----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']

        if password == "admin123":
            db = get_db()
            orders = db.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
            return render_template("admin.html", orders=orders)
        else:
            return "❌ Wrong Password"

    return '''
    <h2>Admin Login</h2>
    <form method="POST">
        <input type="password" name="password" placeholder="Password">
        <button>Login</button>
    </form>
    '''
@app.route('/deliver/<int:id>')
def deliver(id):
    db = get_db()
    db.execute(
        "UPDATE orders SET status = 'Delivered' WHERE id = ?",
        (id,)
    )
    db.commit()
    return redirect('/admin')
# ---------------- START ----------------
if __name__ == "__main__":
    app.run(debug=True)