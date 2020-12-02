import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh import qparser
import json

# Wish List:
# 	- a function for advanced search
# 	- and also a function that takes an ID and returns that 
# 		recipe
# 	- schema is going to have to be updated for the latter, 
# 		its not currently storing everything that needs to be 
# 		returned

class RecipeWhooshSearch(object):
	"""RecipeWhooshSearch creates an object that can 
	take in a given json data set and create a schema, 
	index it and process searches"""

	def __init__(self):
		super(RecipeWhooshSearch, self).__init__()

	def search(self, given_query=None, 
				in_query=None, ex_query=None, 
				diets=None, allegies=None, page=1):
		# These are only for parsing not for filling the results
		keys = ['name', 'ingredients', 'cautions', 'dietLabels', 'healthLabels']

		try:
			index = open_dir('WhooshIndex')
		except Exception:
			self.index()
			index = open_dir('WhooshIndex')

		with index.searcher() as searcher:
			if given_query[0] == '"' and given_query[-1] == '"':
				given_query = given_query[1:-1]
				parser = MultifieldParser(keys, schema=index.schema)
			else:
				parser = MultifieldParser(keys, schema=index.schema, group=OrGroup)
			query = parser.parse(given_query)
			results = searcher.search_page(query, page)
			
			payload = {}
			payload_entries = list()
			for x in results:
				payload_entries.append({'name': 	x['name'], 
								'image':	x['image'],
								'id':		x['id']})
			payload['entries']  = payload_entries
			payload['total'] = len(results)

		return payload


	def index(self):
		# (Id, Name, ingredients, cautions, dietLabel, healthLabel, image, url)
		schema = Schema(id=ID(stored=True),
						name=TEXT(stored=True), 
						ingredients=TEXT(stored=False),
						cautions=TEXT(stored=False),
						dietLabel=TEXT(stored=False),
						healthLabel=TEXT(stored=False),
						image=TEXT(stored=True),
						url=TEXT(stored=True, unique=True))
		indexer = create_in('WhooshIndex', schema)
		writer = indexer.writer()
		with open('recipes/recipe_master_list.json','r') as db:
			doc_json = json.load(db)
			for entry in doc_json:
				recipe = entry['data']['recipe']
				writer.add_document(id=str(entry['id']),
									name=str(recipe['label'] if 'label' in recipe else '0'), 
									ingredients=str(recipe['ingredients'] if 'ingredients' in recipe else '0'),
									cautions=str(recipe['cautions'] if 'cautions' in recipe else '0'),
									dietLabels=str(recipe['dietLabels'] if 'dietLabels' in recipe else '0'),
									healthLabels=str(recipe['healthLabels'] if 'healthLabels' in recipe else '0'),
									image=str(recipe['image'] if 'image' in recipe else '0'),
									url=str(recipe['url'] if 'url' in recipe else '0'))
			writer.commit()
		print("index built")