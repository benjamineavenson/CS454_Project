from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing_page.html')

@app.route('/test')
def test():
    return render_template('template.html')

@app.route('/advanced_search')
def advanced():
    return render_template('advanced.html')

if __name__ == "__main__":
    app.run(debug=True)