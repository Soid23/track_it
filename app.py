from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'jimmy'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize the database if it doesn't exist
def init_db():
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_name TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL,
                due_date TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        '''

        )
        cur.execute('''
                CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                amount_saved REAL DEFAULT 0,
                due_date TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
                )
                    ''')
        cur.execute('''
                CREATE TABLE  IF NOT EXISTS savings_contributions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(goal_id) REFERENCES savings_goals(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
                )
                    ''')
        conn.commit()

init_db()

class User(UserMixin):
    def __init__(self, id, username, email, hashed_password):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cur.fetchone()
        if user:
            return User(*user)
    return None

@app.route('/')
def index():
    return render_template('index.html')

def add_user(username, email, password):
    # Hash the password
    hashed_password = password

    # Connect to the SQLite database
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        # Insert the new user into the users table
        cur.execute('INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)',
                    (username, email, hashed_password))
        
        # Commit the transaction
        conn.commit()
def add_bill (bill_name, amount, due_date, user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO bills (bill_name, amount, due_date, user_id) VALUES (?, ?, ?, ?)',
                    (bill_name, amount, due_date, user_id))
        conn.commit()

def add_expense (expense_name, amount, expense_date, user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO expenses (expense_name, amount, expense_date, user_id) VALUES (?, ?, ?, ?)',
                    (expense_name, amount, expense_date, user_id))
        conn.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username and email and password:
            add_user(username, email, password)
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect('track_it.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cur.fetchone()
            print(user[3])
            print(password)
        
            if user and user[3] == password:
                user_obj = User(*user)
                login_user(user_obj)
                print('Logged in')
                return redirect(url_for('homepage'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/homepage')
@login_required
def homepage():
    return render_template('homepage.html')

@app.route('/my_bills', methods=['GET', 'POST'])
@login_required
def my_bills():
    if request.method == 'POST':
        bill_name = request.form['bill_name']
        amount = request.form['amount']
        due_date = request.form['due_date']
        user_id = current_user.id
        add_bill(bill_name, amount, due_date, user_id)
        return redirect(url_for('my_bills'))

    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM bills WHERE user_id = ?', (current_user.id,))
        bills = cur.fetchall()

    return render_template('my_bills.html', bills=bills)




@app.route('/remove_bill', methods=['POST'])
@login_required
def remove_bill():
    data = request.get_json()
    bill_id = data.get('bill_id')
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM bills WHERE id = ? AND user_id = ?', (bill_id, current_user.id))
        conn.commit()
    return jsonify({'status': 'success'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/my_expenses', methods=['GET'])
def expenses():
    conn = sqlite3.connect('track_it.db')
    c = conn.cursor()
    c.execute("SELECT date, description, amount, category FROM expenses where user_id = ?", (current_user.id,))
    expenses = c.fetchall()
    print(expenses)
    conn.close()
    return render_template('my_expenses.html', expenses=expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    date = request.form['date']
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']

    conn = sqlite3.connect('track_it.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, description, amount, category) VALUES (?, ?, ?, ?)",
              (date, description, amount, category))
    conn.commit()
    conn.close()
    return redirect(url_for('expenses'))



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

@app.route('/savings', methods=['GET', 'POST'])
@login_required
def savings():
    if request.method == 'POST':
        if 'goal_name' in request.form:
            # Adding new goal
            goal_name = request.form['goal_name']
            target_amount = request.form['target_amount']
            due_date = request.form['due_date']
            user_id = current_user.id
            add_goal(goal_name, target_amount, due_date, user_id)
        elif 'goal_id' in request.form:
            # Adding contribution to goal
            goal_id = request.form['goal_id']
            amount = request.form['amount']
            date = request.form['date']
            user_id = current_user.id
            add_contribution(goal_id, amount, date, user_id)
        return redirect(url_for('savings'))

    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, goal_name, target_amount, amount_saved, due_date FROM savings_goals WHERE user_id = ?', (current_user.id,))
        goals = cur.fetchall()

    return render_template('savings.html', goals=goals)


if __name__ == '__main__':
    app.run(debug=True)
