from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/test')
def test():
    return render_template('template.html')

if __name__ == "__main__":
    app.run(debug=True)