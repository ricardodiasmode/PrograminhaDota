import requests
from bs4 import BeautifulSoup, SoupStrainer


# https://pt.dotabuff.com/heroes/ {hero name} /counters


class DotaScrape:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def scrape(self):
        ''''Returns all counters to a hero with all data unparsed'''
        # TODO Save all data to a local file to manipulate (sorted by hero)
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        response = self.session.get(self.url, headers=headers)
        source = response.text
        parse_tag = SoupStrainer('table', class_='sortable')
        return BeautifulSoup(source, 'html.parser', parse_only=parse_tag)


heroname = "anti-mage" # TODO feed {heroname} using HeroNameArray from main

newScrape = DotaScrape(f'https://pt.dotabuff.com/heroes/{heroname}/counters')
print(newScrape.scrape())
