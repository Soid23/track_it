# routes/savings.py
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import add_goal, add_contribution
import sqlite3

def register_routes(app):
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
