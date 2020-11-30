import json

with open('recipes/recipe_master_list.json', 'r') as db:
    db_json = json.load(db)
    names = list()
    dups = 0
    entries = 0
    out = list()
    for entry in db_json:
        if entry['data']['recipe']['label'] in names:
            dups = dups + 1
        else:
            names.append(entry['data']['recipe']['label'])
            out.append(entry)
            entries = entries + 1

print(dups)
print(entries)

with open('recipes/new_master_list.json', 'w') as output:
    json.dump(out, output)