
My Expense Tracker

Welcome to My Expense Tracker, a user-friendly web application designed to help you manage your bills and expenses efficiently. This app allows users to add, edit, and remove bills and expenses, ensuring you stay on top of your financial commitments.

Table of Contents
Features
Requirements
Installation
Usage
Contributing
License
Features
User Authentication: Secure login and user management.
Bill Management: Add, edit, and remove bills with ease.
Expense Tracking: Monitor your expenses by category and date.
Responsive Design: Mobile-friendly interface for access on any device.
Bootstrap Integration: Modern UI components for an enhanced user experience.
Requirements
To run this application, ensure you have the following dependencies installed:

Python 3.7 or higher
Flask web framework
You can install all required packages by running:

Copy code
npm install
Installation
Follow these steps to set up the application locally:

Clone the repository:

git clone https://github.com/Soid23/track_it.git
cd my-expense-tracker
Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate (On Windows use venv\Scripts\activate)
Install the required packages:

pip install -r requirements.txt
Set up the database:

flask db init
flask db migrate
flask db upgrade
Run the application:

flask run
Usage
Open your web browser and go to http://127.0.0.1:5000.
Register for a new account or log in if you already have one.
Start adding your bills and expenses through the intuitive interface.
Contributing
We welcome contributions! If you’d like to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them.
Push to your branch and create a pull request.
Contributors
Jimmy Mithamo
Hafiz Yusuf
Dorris
License
This project is licensed under the MIT License. See the LICENSE file for details.

