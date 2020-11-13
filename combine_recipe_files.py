import json

files = ['recipes/recipes.json', 'recipes/recipes1.json', 'recipes/recipes2.json', 'recipes/recipes3.json', 'recipes/recipes4.json', 'recipes/recipes5.json', 'recipes/recipes6.json', 'recipes/recipes7.json', 'recipes/recipes8.json', 'recipes/recipes9.json', 'recipes/recipes10.json']

recipes = []
urls = []

dup_count = 0

for file in files:
    with open(file, "r") as input:
        obj = json.load(input)
        for r in obj:
            if r['data']['recipe']['url'] not in urls:
                urls.append(r['data']['recipe']['url'])
                recipes.append(r['data'])
            else:
                dup_count += 1
                #print("duplicate count: " + str(dup_count))
    

print("filtered out " + str(dup_count) + " duplicates")

output = []
id = 0
for recipe in recipes:
    r = {
        "id": id,
        "data": recipe
    }
    output.append(r)
    id += 1

with open("out.json", "w") as out:
    json.dump(output, out)