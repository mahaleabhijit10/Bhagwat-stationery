from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("store.db")

# Home Page
@app.route('/')
def home():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template('index.html', products=products)

# Add to Cart
@app.route('/add/<int:id>')
def add_to_cart(id):
    db = get_db()
    db.execute("INSERT INTO cart (product_id) VALUES (?)", (id,))
    db.commit()
    return redirect('/cart')

# View Cart
@app.route('/cart')
def cart():
    db = get_db()
    items = db.execute("""
        SELECT products.id, products.name, products.price 
        FROM cart 
        JOIN products ON cart.product_id = products.id
    """).fetchall()

    total = sum(item[2] for item in items)
    return render_template('cart.html', cart=items, total=total)

# Checkout
@app.route('/checkout', methods=['POST'])
def checkout():
    payment = request.form['payment']

    db = get_db()
    db.execute("DELETE FROM cart")
    db.commit()

    if payment == 'COD':
        return "✅ Order placed successfully (Cash on Delivery)"
    else:
        return render_template('checkout.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()

        return redirect('/login')

    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "❌ Invalid Login"

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)