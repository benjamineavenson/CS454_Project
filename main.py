from flask import Flask
from flask import render_template, request
from search_engine.search_engine import RecipeWhooshSearch

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    query = request.args.get('search')
    if query != None:
        rws = RecipeWhooshSearch()
        print(rws.search(query))
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
