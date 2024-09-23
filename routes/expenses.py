# routes/expenses.py
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import add_expense
import sqlite3
def register_routes(app):
    @app.route('/my_expenses', methods=['GET'])
    @login_required
    def expenses():
        with sqlite3.connect('track_it.db') as conn:
            c = conn.cursor()
            c.execute("SELECT date, description, amount, category FROM expenses WHERE user_id = ?", (current_user.id,))
            expenses = c.fetchall()
        return render_template('my_expenses.html', expenses=expenses)

    @app.route('/add_expense', methods=['POST'])
    @login_required
    def add_expense():
        date = request.form['date']
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']

        with sqlite3.connect('track_it.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO expenses (date, description, amount, category, user_id) VALUES (?, ?, ?, ?, ?)",
                    (date, description, amount, category, current_user.id))
            conn.commit()
        return redirect(url_for('expenses'))
