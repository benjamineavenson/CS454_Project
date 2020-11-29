from flask import Flask
from flask import render_template, request
import json
from search_engine.search_engine import RecipeWhooshSearch

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    query = request.args.get('search')
    if query != None:
        page = request.args.get('page')
        rws = RecipeWhooshSearch()
        if page != None:
            results = rws.search(query, int(page))
        else:
            results = rws.search(query)
       
        return render_template('results.html', results = results['entries'], total = results['total'])
    return render_template('landing_page.html')

@app.route('/test')
def test():
    return render_template('template.html')

@app.route('/advanced_search', methods=['GET'])
def advanced():
    print(request.args)

    return render_template('advanced.html')

@app.route('/recipe_page', methods=['GET'])
def recipe_page():
    return render_template('recipe_page.html')

if __name__ == "__main__":
    app.run(debug=True)
