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
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL NOT NULL,
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
    c.execute("SELECT date, description, amount, category FROM expenses")
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


@app.route('/savings', methods=['GET', 'POST'])
def savings():
    return redirect(url_for('view_goals'))

@app.route('/view_goals')
@login_required
def view_goals():
    user_id = current_user.id
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, goal_name, target_amount, current_amount FROM savings_goals WHERE user_id = ?', (user_id,))
        goals = cur.fetchall()

    goals_data = []
    for goal in goals:
        goal_id, goal_name, target_amount, current_amount = goal
        current_amount = max(current_amount, 0)
        target_amount = max(target_amount, 0)
        remaining_amount = max(target_amount - current_amount, 0)

        fig, ax = plt.subplots()
        sizes = [current_amount, remaining_amount]
        colors = ['blue', 'red']
        labels = ['Current Amount', 'Remaining']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        plt.title(goal_name)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close()
        
        goals_data.append((goal_id, goal_name, image_base64))
    
    return render_template('view_goals.html', goals_data=goals_data)

@app.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    if request.method == 'POST':
        goal_name = request.form['goal_name']
        target_amount = float(request.form['target_amount'])
        current_amount = float(request.form['current_amount'])
        user_id = current_user.id
        
        with sqlite3.connect('track_it.db') as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO savings_goals (user_id, goal_name, target_amount, current_amount) VALUES (?, ?, ?, ?)',
                        (user_id, goal_name, target_amount, current_amount))
            conn.commit()
        return redirect(url_for('view_goals'))
    
    return render_template('add_goal.html')

if __name__ == '__main__':
    app.run(debug=True)
