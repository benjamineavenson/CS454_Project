from flask import Flask
from flask import render_template, request
import json
import math
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
            page = int(page)
        else:
            results = rws.search(query)
            page = 1
       
        total_pages = math.ceil(results['total']/10)
       

        return render_template('results.html', query = query, results = results['entries'], total_pages = total_pages, curr_page = page)
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
