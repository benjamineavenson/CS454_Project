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
	take in a given data set and create a schema and process searches"""

	def __init__(self):
		super(RecipeWhooshSearch, self).__init__()

	def search(self, given_query, limit=10):
		keys = ['id', 'name', 'cardSet', 'type', 'race', 'rarity', 'cost',
				'attack', 'health', 'text', 'playerClass', 'img', 'mechanics']
		ids 	= list()
		names 	= list()
		cardSets= list()
		races 	= list()
		costs 	= list()
		attacks = list()
		healths = list()

		with self.indexer.searcher() as search:
			if given_query[0] == '"' and given_query[-1] == '"':
				given_query = given_query[1:-1]
				query = MultifieldParser(keys, schema=self.indexer.schema)
			else:
				query = MultifieldParser(keys, schema=self.indexer.schema, group=OrGroup)
			query = query.parse(given_query)
			results = search.search(query, limit=limit)

			for x in results:
				ids.append(x['id'])
				names.append(x['name'])
				cardSets.append(x['cardSet'])
				races.append(x['race'])
				costs.append(x['cost'])
				attacks.append(x['attack'])
				healths.append(x['health'])

		return list(zip(ids, names, cardSets, races, costs, attacks, healths))


	def index(self):
		schema = Schema(id=ID(stored=True),
						name=TEXT(stored=True), 
						cardSet=TEXT(stored=True),
						race=TEXT(stored=True),
						cost=TEXT(stored=True),
						attack=TEXT(stored=True),
						health=TEXT(stored=True))
		indexer = create_in('WhooshIndex', schema)
		writer = indexer.writer()
		doc_json = json.load(open("cards.json",'r'))
		for doc in doc_json:
			for card in doc_json[doc]:
				writer.add_document(id=str(card['dbfId'] if 'dbfId' in card else '0'),
									name=str(card['name'] if 'name' in card else '0'), 
									cardSet=str(card['cardSet'] if 'cardSet' in card else '0'),
									race=str(card['race'] if 'race' in card else '0'),
									cost=str(card['cost'] if 'cost' in card else '0'),
									attack=str(card['attack'] if 'attack' in card else '0'),
									health=str(card['health'] if 'health' in card else '0'))
		writer.commit()

		self.indexer = indexer
