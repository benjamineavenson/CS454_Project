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
				diets=None, allergies=None, page=1):
		# These are only for parsing not for filling the results
		keys = ['name', 'ingredients', 'cautions', 'dietLabels', 'healthLabels']

		try:
			index = open_dir('WhooshIndex')
		except Exception:
			self.index()
			index = open_dir('WhooshIndex')

		with index.searcher() as searcher:
			# given query parsing
			if given_query[0] == '"' and given_query[-1] == '"':
				given_query = given_query[1:-1]
				parser = MultifieldParser(keys, schema=index.schema)
			else:
				parser = MultifieldParser(keys, schema=index.schema, group=OrGroup)
			query = parser.parse(given_query)
			results = searcher.search_page(query, page)
			# include query parsing
			if in_query != None:
				in_parser = MultifieldParser('ingredients', schema=index.schema)
				in_q = parser.parse(in_query)
				in_r = searcher.search_page(query=in_q, page=page)
			# else:
				#in = *
				#results = results.filter(*)
			# exclude query parsing
			if ex_query != None:
				ex_parser = MultifieldParser('ingredients', schema=index.schema)
				ex_q = parser.parse(ex_query)
				ex_r = searcher.search_page(query=ex_q, page=page)
			# allergies query parsing
			if allergies != None:
				allergy_parser = MultifieldParser('cautions', schema=index.schema)
				allergy_q = parser.parse(allergies)
				allergy_r = searcher.search_page(query=allergy_q, page=page)
				results = results.filter(allergy_r)
			# diets query parsing
			if diets != None:
				diet_parser = MultifieldParser('dietInfo', schema=index.schema)
				diets_q = parser.parse(diets)
				diets_r = searcher.search_page(query=diets_q, page=page)
			# filtering results to get intersection
			# print(type(results))
			
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
		
		return result
			

	def index(self):
		# (Id, Name, ingredients, cautions, dietLabel, healthLabel, image, url)
		schema = Schema(id=ID(stored=True),
						url=TEXT(stored=True),
						name=TEXT(stored=True), 
						ingredients=TEXT(stored=True),
						cautions=KEYWORD(stored=True),
						dietInfo=KEYWORD(stored=True),
						nutrition=TEXT(stored=True),
						image=TEXT(stored=True))
		indexer = create_in('WhooshIndex', schema)
		writer = indexer.writer()
		with open('recipes/recipe_master_list.json','r') as db:
			doc_json = json.load(db)
			for entry in doc_json:

				recipe = entry['data']['recipe']

				dietLabels = recipe['dietLabels'] if 'dietLabels' in recipe else []
				healthLabels = recipe['healthLabels'] if 'healthLabels' in recipe else []
				dietInfo = dietLabels + healthLabels

				nutrients = []
				for nutrient in recipe['totalNutrients']:
					quantity = str(recipe['totalNutrients'][nutrient]['quantity'])
					quantity = quantity.partition('.')[0] + quantity.partition('.')[1] + quantity.partition('.')[2][:2]
					n = recipe['totalNutrients'][nutrient]['label'] + ": " + quantity + recipe['totalNutrients'][nutrient]['unit']
					nutrients.append(n)

				writer.add_document(id=str(entry['id']),
									url=str(recipe['url'] if 'url' in recipe else '0'),
									name=str(recipe['label'] if 'label' in recipe else '0'), 
									ingredients=str(recipe['ingredientLines'] if 'ingredientLines' in recipe else '0'),
									cautions=str(recipe['cautions'] if 'cautions' in recipe else '0'),
									dietInfo=str(dietInfo),
									nutrition=str(nutrients),
									image=str(recipe['image'] if 'image' in recipe else '0'))
			writer.commit()
		print("index built")