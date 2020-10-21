# CS454 Project - Recipe Search Engine
## About
For our project we plan to create a search engine that will allow users to query a database of online recipes. We plan to use Whoosh for the indexing of our database, and Jinja/Flask for our web framework. The engine will show ten results for the user’s query on each page, each consisting of an image (if available) and a link to an external website containing the recipe. Users will also have the option to perform an advanced search, and/or modify the order of the returned results. 

The advanced search and filtering feature would look at the ingredients list of recipes and would remove any recipes from the list of results that do not fit a pre-defined dietary restriction selected by the user, or contain ingredients that aren’t listed as ‘on-hand’ by the user. The result modification feature would provide the user a way to reorder the results based on nutritional data, such as calorie count.

We plan to scrape our dataset using Edamam, a recipe search API. This will provide us with links, images, ingredients lists, recipe titles, and nutrition data for each recipe. The free plan provides us with the opportunity to scrape 500,000 recipes in the span of a month, which should be plenty for the scope of the project.
