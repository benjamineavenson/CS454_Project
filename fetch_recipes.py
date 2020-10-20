import urllib.request   #library for making requests to the api
import json             #library for decoding/encoding json
import time             #needed for sleep method for waiting between requests when ratelimited, and for timing the program
from bs4 import BeautifulSoup   #used for cleaning html before inserting it into db

# our base url, formatted to request the api for page description and images from pages that contain the word 'rainforest'
url = "https://api.edamam.com/search?app_id=51f2afbd&app_key=6e44f521c39a2b8c69e64fd1d9d8b1bf&q=chicken"
response = urllib.request.urlopen(url)  #make a request
obj = json.load(response)               #convert it to a dict we can use

print(obj)