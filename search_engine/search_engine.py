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
		keys = ['label', 'ingredientLines', 'cautions', 'dietLabels']
		names 			= list()
		ingredients		= list()
		cautions 		= list()
		dietLabels 		= list()
		ingredientLines = list()

		with self.indexer.searcher() as search:
			if given_query[0] == '"' and given_query[-1] == '"':
				given_query = given_query[1:-1]
				query = MultifieldParser(keys, schema=self.indexer.schema)
			else:
				query = MultifieldParser(keys, schema=self.indexer.schema, group=OrGroup)
			query = query.parse(given_query)
			results = search.search(query, limit=limit)

			for x in results:
				# ids.append(i)
				names.append(x[keys[0]])
				ingredients.append([k for k in x[keys[1]]])
				cautions.append(x[keys[2]])
				dietLabels.append(x[keys[3]])

		return list(zip(names, ingredients, cautions, dietLabels))


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
		for doc in doc_json:
			for i, recipe in enumerate(doc_json[doc]):
				writer.add_document(id=str(i),
									name=str(recipe['name'] if 'name' in recipe else '0'), 
									ingredients=str(recipe['ingredients'] if 'ingredients' in recipe else '0'),
									cautions=str(recipe['cautions'] if 'cautions' in recipe else '0'),
									dietLabel=str(recipe['dietLabel'] if 'dietLabel' in recipe else '0'))
		writer.commit()

		self.indexer = indexer
