from flask import Flask
from flask import render_template, request
import json
import math
from search_engine.search_engine import RecipeWhooshSearch

app = Flask(__name__)

def toList(ingredients):    #function for processing the ingredients string that whoosh returns for display
    #print(ingredients)
    index = 0
    output = []
    while True:
        singleQuote = ingredients.find("'", index, len(ingredients))
        doubleQuote = ingredients.find('"', index, len(ingredients))
        #print("single = " + str(singleQuote))
        #print("double = " + str(doubleQuote))
        if singleQuote == -1 and doubleQuote == -1:
            return output
        if singleQuote == -1:
            singleQuote = len(ingredients) + 1
        if doubleQuote == -1:
            doubleQuote = len(ingredients) + 1
        if(singleQuote < doubleQuote):
            end = ingredients.find("'", singleQuote+1, len(ingredients))
            output.append(ingredients[singleQuote+1:end])
        if(doubleQuote < singleQuote):
            end = ingredients.find('"', doubleQuote+1, len(ingredients))
            output.append(ingredients[doubleQuote+1:end])
        index = end + 1
        #print(index)
        


@app.route('/', methods=['GET'])
def home():
    query = request.args.get('search')
    if query != None:   #if we are given a search query, perform a search over it
        page = request.args.get('page')
        rws = RecipeWhooshSearch()
        if page != None:
            results = rws.search(given_query=query, page=int(page)) #if we are given a page number, search for that page
            page = int(page)
        else:
            results = rws.search(query) #if we arent given a page number, get page 1
            page = 1
       
        total_pages = math.ceil(results['total']/10)    #calculate the total number of results, so we know how many pages there are
       
        return render_template('results.html', #render results page
                                query=query, 
                                results=results['entries'], 
                                total_pages=total_pages, 
                                curr_page=page,
                                advanced=False)
    return render_template('landing_page.html') #if we arent given a query, render the landing page

@app.route('/advanced_search', methods=['GET'])
def advanced():
    rws = RecipeWhooshSearch()
    # Get all the input from the user
    query = request.args.get('search')
    include = request.args.get('included_ingredients')
    exclude = request.args.get('excluded_ingredients')
    diets   = request.args.getlist('diets')
    cautions= request.args.getlist('cautions')
    ranking = request.args.get('ranking_method')
    page = request.args.get('page')
    page = int(page) if(page != None) else 1
    
    if((query == None or query == '') and   #if there is no input, render the advanced search interface
        (include == None or include == '') and 
        (exclude == None or exclude == '') and
        (diets == []) and
        (cautions == [])):
        return render_template('advanced.html')
    
    include_list = include.split(',')   #the backend expects ingredients as lists
    exclude_list = exclude.split(',')

    results = rws.search(given_query=query,     #perform the search
                        in_query=include_list, 
                        ex_query=exclude_list, 
                        diets=diets, 
                        allergies=cautions, 
                        page=page,
                        ranking=ranking)
    total_pages = math.ceil(results['total']/10)
    return render_template('results.html',  #render the results
                            query=query,
                            in_query=include,
                            ex_query=exclude,
                            diets=diets,
                            cautions=cautions, 
                            results=results['entries'], 
                            total_pages=total_pages, 
                            curr_page=page,
                            ranking=ranking,
                            advanced=True)

@app.route('/recipe_page', methods=['GET'])
def recipe_page():
    rws = RecipeWhooshSearch()
    
    if request.args.get('id') != None: 
        recipe = rws.lookup(request.args.get('id'))[0]  #get the recipe with the given id
        ingredients = recipe['ingredients'].strip('[').strip(']')
        ingredients = toList(ingredients)   #make the ingredients a list

        temp = []
        for i in ingredients:
            i = i.replace('\u00c2', '') #this unicode character appeared a few times for no apparent reason... removing it
            if len(i) > 2:
                temp.append(i)
        ingredients = temp

#format the labels
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
        return render_template('landing_page.html') #default to the landing page if there's no id for whatever reason
    
    #render the recipe page
    return render_template('recipe_page.html', recipe = recipe, ingredients = ingredients, cautions = cautions, dietInfo = dietInfo, nutrition = nutrition)

if __name__ == "__main__":
    app.run(debug=True)
