# CS454 Project - Recipe Search Engine
## About
This project is a search engine that allows users to query a database of online recipes. We use Whoosh for the indexing of our database, and Jinja/Flask for our web framework. The engine shows ten results for the user’s query on each page, each consisting of an image and a link to an external website containing the recipe. Users also have the option to perform an advanced search and select a different ranking algorithm. 

The advanced search and filtering feature looks at the ingredients list and diet labels of recipes and removes any recipes from the list of results that do not meet the filterint requirements. The ranking algorithm selection feature provides the user two options for ranking results.

We scraped our dataset using Edamam, a recipe search API. This provides us with links, images, ingredients lists, recipe titles, and nutrition and diet data for each recipe. The free plan provided us with the opportunity to scrape over 13000 recipes.

## Using the Search Engine
### Setup
To make this webapp run, there must be a directory at the root level of the project named "WhooshIndex". This is where the index files are kept once it is built.
Once this directory is created, run main.py and direct your browser to "localhost:5000".

### The Basic Search Interface
To perform a basic search, input your query in the box and click 'Search'.

### The Advanced Search Interface
The advanced search interface contains several fields that allow the user to be more specific in what they are looking for.

#### Search
This field is the same as the basic search field.

#### Ranking Algorithm
This select allows the user to select which ranking algorithm to use.

#### Ingredients
These two fields allow the user to supply comma separated lists of ingredients. The include list will make the search only return results that contain all of the specified ingredients. The exclude list will make the search filter out any results that contain any of the specified ingredients.

#### Diets
These checkboxes allow the user to select one or more diets that they want to filter results by. Returned results will contain all of the specified diet labels.

#### Cautions
These checkboxes allow the user to filter out any results that contain the caution labels that they select.

