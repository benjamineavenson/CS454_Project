import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh import qparser
import json

class RecipeWhooshSearch(object):
	"""RecipeWhooshSearch creates an object that can 
	take in a given json data set and create a schema, 
	index it and process searches"""

	def __init__(self):
		super(RecipeWhooshSearch, self).__init__()

	def search(self, given_query, limit=10):
		keys = ['name', 'ingredients', 'cautions', 'dietLabel']
		ids = list()

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
			results = searcher.search(query, limit=limit)
			print(results)
			for x in results:
				ids.append(x['id'])
				

		return ids


	def index(self):
		# (Id, Name, ingredients, cautions, dietLabel)
		schema = Schema(id=ID(stored=True),
						name=TEXT(stored=True), 
						ingredients=TEXT(stored=True),
						cautions=TEXT(stored=True),
						dietLabel=TEXT(stored=True))
		indexer = create_in('WhooshIndex', schema)
		writer = indexer.writer()
		doc_json = json.load(open('recipes/recipe_master_list.json','r'))
		for entry in doc_json:
			recipe = entry['data']['recipe']
			writer.add_document(id=str(entry['id']),
								name=str(recipe['label'] if 'label' in recipe else '0'), 
								ingredients=str(recipe['ingredients'] if 'ingredients' in recipe else '0'),
								cautions=str(recipe['cautions'] if 'cautions' in recipe else '0'),
								dietLabel=str(recipe['dietLabel'] if 'dietLabel' in recipe else '0'))
		writer.commit()

		print("index built")