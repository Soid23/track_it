from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_started')
def get_started():
    return render_template('getStarted.html')

@app.route('/expenditure')
def expenditure():
    return render_template('expenditure.html')

@app.route('/savings')
def savings():
    return render_template('savings.html')

if __name__ == '__main__':
    app.run(debug=True)
