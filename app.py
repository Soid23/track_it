from flask import Flask
from flask_login import LoginManager
from config import Config
from database.init_db import init_db
from routes import register_routes
from models import User  # Make sure to import the User class
import sqlite3

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect('track_it.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cur.fetchone()
        if user:
            return User(*user)  # Create a User object if found
    return None

init_db()  # Initialize the database

# Register routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
