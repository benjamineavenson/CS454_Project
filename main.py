from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    query = request.args.get('search')
    if query != None:
        #call spencer's methods to get results, for now we will just print the query to the terminal
        print(query)
    return render_template('landing_page.html')

@app.route('/test')
def test():
    return render_template('template.html')

@app.route('/advanced_search', methods=['GET'])
def advanced():
    print(request.args)

    return render_template('advanced.html')

if __name__ == "__main__":
    app.run(debug=True)
