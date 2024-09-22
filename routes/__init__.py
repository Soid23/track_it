from flask import render_template
from flask_login import login_required
from .auth import register_routes as register_auth_routes
from .bills import register_routes as register_bills_routes
from .expenses import register_routes as register_expenses_routes
from .savings import register_routes as register_savings_routes

def register_routes(app):
    register_auth_routes(app)
    register_bills_routes(app)
    register_expenses_routes(app)
    register_savings_routes(app)

    @app.route('/homepage')
    @login_required
    def homepage():
        return render_template('homepage.html')

    @app.route('/')
    def index():
        return render_template('index.html')
    
