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
            results = rws.search(given_query=query, page=int(page))
            page = int(page)
        else:
            results = rws.search(query)
            page = 1
       
        total_pages = math.ceil(results['total']/10)
       
        return render_template('results.html', 
                                query=query, 
                                results=results['entries'], 
                                total_pages=total_pages, 
                                curr_page=page)
    return render_template('landing_page.html')

@app.route('/test')
def test():
    return render_template('template.html')

@app.route('/advanced_search', methods=['GET'])
def advanced():
    print(request.args)
    rws = RecipeWhooshSearch()
    # Get all the input from the user
    query = request.args.get('keywords')
    include = request.args.get('included_ingredients')
    exclude = request.args.get('excluded_ingredients')
    diets   = request.args.getlist('diets')
    cautions= request.args.getlist('cautions')
    page = request.args.get('page')
    page = int(page) if(page != None) else 1
    # test allergens
    if((query == None) and 
        (include == None) and 
        (exclude == None) and
        (diets == None) and
        (cautions == None)):
        return render_template('advanced.html')
    
    results = rws.search(given_query=query, 
                        in_query=include, 
                        ex_query=exclude, 
                        diets=diets, 
                        allergies=cautions, 
                        page=page)
    total_pages = math.ceil(results['total']/10)
    return render_template('results.html', 
                            query=query, 
                            results=results['entries'], 
                            total_pages=total_pages, 
                            curr_page=page)

@app.route('/recipe_page', methods=['GET'])
def recipe_page():
    rws = RecipeWhooshSearch()
    
    if request.args.get('id') != None:
        recipe = rws.lookup(request.args.get('id'))[0]
        ingredients = recipe['ingredients'].strip('[').strip(']').split("'")

        temp = []
        for i in ingredients:
            i = i.replace('\u00c2', '')
            if len(i) > 2:
                temp.append(i)
        ingredients = temp


        cautions = recipe['cautions'].strip('[').strip(']').replace("'", '').split(',')

        temp = []
        for c in cautions:
            c = c.strip()
            temp.append(c)
        cautions = temp

        dietInfo = recipe['dietInfo'].strip('[').strip(']').replace("'", '').split(',')

        temp = []
        for d in dietInfo:
            d = d.strip()
            temp.append(d)
        dietInfo = temp

        nutrition = recipe['nutrition'].strip('[').strip(']').replace("'", '').split(',')
    else:
        return render_template('landing_page.html')
    
    return render_template('recipe_page.html', recipe = recipe, ingredients = ingredients, cautions = cautions, dietInfo = dietInfo, nutrition = nutrition)

@app.route('/results_page', methods=['GET'])
def results_page():
    return render_template('results_page.html')

if __name__ == "__main__":
    app.run(debug=True)
