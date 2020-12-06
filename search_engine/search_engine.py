import whoosh
from whoosh import scoring
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh import qparser
import json


def list_to_keywords(ls):
	keywords = ""
	for k in ls:
		keywords += k+','
	return keywords[:-1]



class RecipeWhooshSearch(object):
	"""RecipeWhooshSearch creates an object that can 
	take in a given json data set and create a schema, 
	index it and process searches"""

	def __init__(self):
		super(RecipeWhooshSearch, self).__init__()


	def search(self, given_query='', 
				in_query=[''], ex_query=[''], 
				diets=[], allergies=[], page=1, ranking="BM25"):
		# These are only for parsing not for filling the results
		keys = ['name', 'ingredients', 'cautions', 'dietLabels', 'healthLabels']

		try:
			index = open_dir('WhooshIndex')
		except Exception:
			self.index()
			index = open_dir('WhooshIndex')

		if ranking == "TF-IDF":
			ranking = scoring.TF_IDF()
		else:
			ranking = scoring.BM25F()

		with index.searcher(weighting=ranking) as searcher:
			# Universal all docs in case of None
			# because in the intersection the smaller 
			# result will be returned
			parser = QueryParser('url', schema = index.schema)
			q = parser.parse('http OR https')
			all_docs = searcher.search(q, limit=None)
			# Creates an empty result for a filter and mask
			p = QueryParser('id', schema=index.schema)
			q = p.parse('')
			myMask = searcher.search(q, limit=None)
			myFilter = searcher.search(q, limit=None)
			
			# include query parsing
			if in_query != ['']:	
				in_parser = QueryParser('ingredients', schema=index.schema)
				inFilter = searcher.search(q, limit=None)
				in_q = in_parser.parse(in_query[0])
				in_r = searcher.search(in_q, limit=None)
				inFilter.extend(in_r)
				for q in in_query:
					in_q = in_parser.parse(q)
					in_r = searcher.search(in_q, limit=None)
					inFilter.filter(in_r)
				myFilter.extend(inFilter)

			# exclude query parsing
			if ex_query != ['']:
				ex_parser = QueryParser('ingredients', schema=index.schema)
				for q in ex_query:
					ex_q = ex_parser.parse(q)
					ex_r = searcher.search(ex_q, limit=None)
					myMask.extend(ex_r)

			# allergies query parsing
			if allergies != []:
				allergy_parser = QueryParser('cautions', schema=index.schema)
				for q in allergies:
					allergy_q = allergy_parser.parse(q)
					allergy_r = searcher.search(allergy_q, limit=None)
					myMask.extend(allergy_r)

			# diets query parsing
			if diets != []:
				p = QueryParser('id', schema=index.schema)
				q = p.parse('')
				dietFilter = searcher.search(q, limit=None)
				diet_parser = QueryParser('dietInfo', schema=index.schema)
				diet_q = diet_parser.parse(diets[0])
				diet_r = searcher.search(diet_q, limit=None)
				dietFilter.extend(diet_r)
				for d in diets:
					diet_q = diet_parser.parse(d)
					diet_r = searcher.search(diet_q, limit=None)
					dietFilter.filter(diet_r)

				if(in_query == ['']):
					myFilter.extend(dietFilter)
				else:
					myFilter.filter(dietFilter)
			# filtering results to get intersection
			# print(type(results))

			# Check if the filter is empty so we don't intersect nothing
			if(diets == [] and in_query == ['']):
				myFilter = all_docs
			elif myFilter.scored_length() == 0:	#if we filtered and got nothing, we should return nothing
				payload = {}
				payload_entries = list()
				payload['entries']  = payload_entries
				payload['total'] = 0
				return payload
			
			if given_query != '' and given_query != None:
				if given_query[0] == '"' and given_query[-1] == '"':
					given_query = given_query[1:-1]
					parser = MultifieldParser(keys, schema=index.schema)
				else:
					parser = MultifieldParser(keys, schema=index.schema, group=OrGroup)
				query = parser.parse(given_query)
				results = searcher.search_page(query, page, filter=myFilter, mask=myMask)
			else:
				parser = QueryParser('url', schema = index.schema)
				q = parser.parse('http OR https')
				results = searcher.search_page(q, page, filter=myFilter, mask=myMask)
				

			# Format results for returning
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
						cautions=TEXT(stored=True),
						dietInfo=TEXT(stored=True),
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