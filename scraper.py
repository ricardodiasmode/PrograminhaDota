import requests
import json
import os.path
import os
from bs4 import BeautifulSoup, SoupStrainer


class DotaScrape:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def scrape(self):
        """Returns all counters to a hero with all data unparsed"""
        # TODO Save all data to a local file to manipulate (sorted by hero)
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        response = self.session.get(self.url, headers=headers)
        source = response.text
        parse_tag = SoupStrainer('table', class_='sortable')
        return BeautifulSoup(source, 'html.parser', parse_only=parse_tag)


def RequestHeroStats():
    if os.path.isfile('HeroStats.txt'):
        os.remove("HeroStats.txt")
    HeroStats_json = requests.get(
        "https://api.opendota.com/api/heroStats",
        headers={"Accept": "application/json"}
    ).json()
    with open("HeroStats.txt", "w") as HeroStatsFile:
        HeroStatsFile.write(json.dumps(HeroStats_json))
    print("HeroStats file Updated!")
    print("--------")
    HeroStatsFile.close()
