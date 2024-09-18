import sqlite3
from flask_bcrypt import Bcrypt

# Initialize Flask-Bcrypt (if you're using it for password hashing)
bcrypt = Bcrypt()


# Function to add a new user
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

# Example usage
add_user('example_user', 'user@example.com', 'securepassword')