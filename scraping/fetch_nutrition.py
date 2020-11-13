import urllib.request   #library for making requests to the api
import json             #library for decoding/encoding json

# our url, formatted to request the edamam api for recipes containing chicken
url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=fcBqfh9kykD02GLu8Yc64nPA032PRKabfkitIQQe&query=russet%20potato&dataType=Foundation&pageSize=1"
response = urllib.request.urlopen(url)  #make a request
obj = json.load(response)               #convert it to a dict we can use

print(obj)