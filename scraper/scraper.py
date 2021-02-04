from bs4 import BeautifulSoup
import json
import requests


class Recipe:
    def __init__(self, recipe_json):
        self.name = recipe_json['name']
        self.description = recipe_json['description']
        self.ingredients = recipe_json['recipeIngredient']
        self.steps = list(step['text'] for step in recipe_json['recipeInstructions'])


def read(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    script = soup.find('script', attrs={'type': 'application/ld+json', 'class': 'yoast-schema-graph'})
    graph = json.loads(script.string)['@graph']
    try:
        recipe = Recipe(next(item for item in graph if item['@type'] == 'Recipe'))
    except StopIteration:
        return
    print(recipe.name)
    print(recipe.description)
    print(recipe.ingredients)
    print(recipe.steps)


def read_from_sitemap(sitemap_url):
    page = requests.get(sitemap_url)
    soup = BeautifulSoup(page.content, 'xml')
    pages = soup.find_all('url')
    for page in pages:
        loc = page.find('loc')
        read(loc.text)


if __name__ == '__main__':
    read_from_sitemap('https://www.loveandlemons.com/sitemap-pt-post-2021-01.xml')