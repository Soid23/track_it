from flask import  render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from models import User, add_user
import sqlite3

def register_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            with sqlite3.connect('track_it.db') as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE email = ?', (email,))
                user = cur.fetchone()

            
                if user and user[3] == password:
                    user_obj = User(*user)
                    login_user(user_obj)
                    print('Logged in')
                    return redirect(url_for('homepage'))
                else:
                    flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            add_user(username, email, password)  # Hashing handled in the model
            return redirect(url_for('login'))
        return render_template('register.html')



