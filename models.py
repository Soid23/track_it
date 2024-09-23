# models.py
from flask_login import UserMixin, LoginManager
from flask_bcrypt import Bcrypt
import sqlite3
from database.init_db import init_db


# Initialize Flask-Bcrypt
bcrypt = Bcrypt()
login_manager = LoginManager()

init_db()

def add_user(username, email, password):
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Connect to the SQLite database
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        # Insert the new user into the users table
        cur.execute('INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)',
                    (username, email, hashed_password))
        # Commit the transaction
        conn.commit()

def get_user(email):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cur.fetchone()

class User(UserMixin):
    def __init__(self, id, username, email, hashed_password):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

def add_bill(bill_name, amount, due_date, user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO bills (bill_name, amount, due_date, user_id) VALUES (?, ?, ?, ?)',
                    (bill_name, amount, due_date, user_id))
        conn.commit()

def add_expense(date, description, amount, category, user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO expenses (date, description, amount, category, user_id) VALUES (?, ?, ?, ?, ?)',
                    (date, description, amount, category, user_id))
        conn.commit()

def add_goal(goal_name, target_amount, due_date, user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO savings_goals (goal_name, target_amount, due_date, user_id) VALUES (?, ?, ?, ?)',
                    (goal_name, target_amount, due_date, user_id))
        conn.commit()

def add_contribution(goal_id, amount, date, user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO savings_contributions (goal_id, amount, date, user_id) VALUES (?, ?, ?, ?)',
                    (goal_id, amount, date, user_id))
        cur.execute('UPDATE savings_goals SET amount_saved = amount_saved + ? WHERE id = ?', (amount, goal_id))
        conn.commit()

def add_contribution(goal_id, amount, date, user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO savings_contributions (goal_id, amount, date, user_id) VALUES (?, ?, ?, ?)', 
                    (goal_id, amount, date, user_id))
        cur.execute('UPDATE savings_goals SET amount_saved = amount_saved + ? WHERE id = ?', (amount, goal_id))
        conn.commit()