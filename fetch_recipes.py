import urllib.request   #library for making requests to the api
import json             #library for decoding/encoding json

# our url, formatted to request the edamam api for recipes containing chicken
url = "https://api.edamam.com/search?app_id=51f2afbd&app_key=6e44f521c39a2b8c69e64fd1d9d8b1bf&q=chicken"
response = urllib.request.urlopen(url)  #make a request
obj = json.load(response)               #convert it to a dict we can use

print(obj)