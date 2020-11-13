import urllib.request   #library for making requests to the api
import json             #library for decoding/encoding json
import time             #for waiting between calls to not break the limit


#a list of queries to run through
#queries = ["&q=chicken", "&q=fish", "&q=pork", "&q=pasta", "&q=spinach"]
#queries = ["&q=peanut", "&q=salad", "&q=cake", "&q=pie", "&q=lemon", "&q=chocolate", "&q=beef", "&q=seafood", "&q=curry", "&q=bread", "&q=soup", "&q=egg", "&q=cookies"]
#queries = ["&q=stew", "&q=casserole", "&q=cheese", "&q=burger", "&q=pizza", "&q=sandwich", "&q=potato"]
#queries = ["&q=sushi", "&q=chowder", "&q=fried", "&q=bagel", "&q=turkey", "&q=rice"]
#queries = ["&q=vegetarian", "&q=vegan", "&q=brownie", "&q=stir_fry", "&q=smoked", "&q=barbeque"]
#queries = ["&q=gumbo", "&q=jambalaya", "&q=chinese", "&q=korean", "&q=spaghetti", "&q=parfait"]
#queries = ["&q=strawberry", "&q=apple", "&q=pumpkin", "&q=enchilada", "&q=tamale", "&q=fajitas"]
#queries = ["&q=salmon", "&q=lobster", "&q=shrimp", "&q=muffin", "&q=pudding", "&q=flan"]
#queries = ["&q=teriyaki", "&q=sour", "&q=waffle", "&q=french", "&q=omelette", "&q=hash"]
#queries = ["&q=mozzarella", "&q=lasagna", "&q=fruit", "&q=berry", "&q=dip", "&q=taco"]
#queries = ["&q=thai", "&q=indian", "&q=mexican", "&q=italian", "&q=japanese", "&q=rustic", "&q=pastry", "&q=classic", "&q=sweet", "&q=pickle", "&q=dough", "&q=bacon", "&q=nut", "&q=hawaiian", "&q=cream", "&q=caramel", "&q=spicy", "&q=salt", "&q=slow", "&q=healthy", "&q=avocado", "&q=oil", "&q=olive", "&q=drink", "&q=dessert", "&q=appetizer", "&q=breakfast", "&q=lunch", "&q=dinner", "&q=side", "&q=chili", "&q=melon", "&q=onion", "&q=air", "&q=butter", "&q=frozen", "&q=quinoa", "&q=quick", "&q=crisp", "&q=ice", "&q=gravy", "&q=seed", "&q=pancake", "&q=bean", "&q=roast", "&q=bake", "&q=simple", "&q=fall", "&q=spring", "&q=summer", "&q=winter", "&q=autumn", "&q=sauce", "&q=juicy", "&q=dressing", "&q=potatoes", "&q=party", "&q=holiday", "&q=crunchy", "&q=bars", "&q=gluten", "&q=sugar", "&q=frosting", "&q=roll", "&q=mediterranean", "&q=greek", "&q=steak", "&q=gyro", "&q=lamb", "&q=basic", "&q=tender", "&q=easy", "&q=festive", "&q=bark", "&q=garlic", "&q=ramen", "&q=corn", "&q=tomato", "&q=ginger", "&q=ravioli", "&q=alfredo", "&q=cocktail", "&q=tart", "&q=tortellini", "&q=skillet", "&q=breaded", "&q=meat", "&q=dairy", "&q=comfort", "&q=spanish", "&q=swedish", "&q=glazed", "&q=ham", "&q=citrus", "&q=macaroni", "&q=paella", "&q=fettuccine", "&q=wine"]


# our url, formatted to request the edamam api using our credentials
base_url = "https://api.edamam.com/search?app_id=51f2afbd&app_key=6e44f521c39a2b8c69e64fd1d9d8b1bf"

recipes = []

recipe_count = 0
dump_count = 0
query_count = 0

for q in queries:
    for i in range(21):
        query_count += 1
        if query_count%4 == 3:
            print("sleeping 2 minutes...")
            time.sleep(120)
        url_range = "&from=" + str(i*100) + "&to=" + str(((i+1)*100)-1)
        url = base_url+q+url_range

        print("requesting payload number " + str(i) + " of query " + q)

        try:
            response = urllib.request.urlopen(url)  #make a request
            print("response recieved")
            obj = json.load(response)               #convert it to a dict we can use
            print("response converted")

            for r in obj['hits']:
                recipes.append({"data": r, "id": recipe_count})
                recipe_count += 1

            if obj['more'] == False:
                break

        except Exception:
            dump_count += 1
            filename = "dump" + str(dump_count) + ".json"
            print("ran into an issue... dumping json to " + filename)
            with open(filename, 'w') as out:
                json.dump(recipes, out)

print("made all requests, writing to file")
with open("recipes.json", "w") as out:
    json.dump(recipes, out)