from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'system.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_FILE):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS credit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                balance REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        conn.execute('INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
        conn.commit()
        return redirect(url_for('products'))
        
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/credit', methods=['GET', 'POST'])
def credit():
    conn = get_db_connection()
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        balance = request.form['balance']
        conn.execute('INSERT INTO credit (customer_name, balance) VALUES (?, ?)', (customer_name, balance))
        conn.commit()
        return redirect(url_for('credit'))
        
    credits = conn.execute('SELECT * FROM credit').fetchall()
    conn.close()
    return render_template('credit.html', credits=credits)

if __name__ == '__main__':
    app.run(debug=True)
