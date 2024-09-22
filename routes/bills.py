# routes/bills.py
from flask import render_template, request, redirect, jsonify
from flask_login import login_required, current_user
from models import add_bill
import sqlite3

def register_routes(app):
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
