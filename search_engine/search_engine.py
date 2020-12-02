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

	def search(self, given_query, page=1):
		keys = ['name', 'ingredients', 'cautions', 'dietLabel']

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


	def lookup(self, id):
		try:
			index = open_dir('WhooshIndex')
		except Exception:
			self.index()
			index = open_dir('WhooshIndex')
		
		with index.searcher() as searcher:
			
			result = list(searcher.documents(id=id))
			print(result)
			

	def index(self):
		# (Id, Name, ingredients, cautions, dietLabel)
		schema = Schema(id=ID(stored=True),
						name=TEXT(stored=True), 
						ingredients=TEXT(stored=False),
						cautions=TEXT(stored=False),
						dietLabel=TEXT(stored=False),
						image=TEXT(stored=True))
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
									dietLabel=str(recipe['dietLabel'] if 'dietLabel' in recipe else '0'),
									image=str(recipe['image'] if 'image' in recipe else '0'))
			writer.commit()
		print("index built")