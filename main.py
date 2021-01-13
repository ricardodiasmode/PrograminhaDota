""" The objective of this program is return the current best heroes of the meta """
import requests
import numpy as np
import scraper
import math
from dataclasses import dataclass


NumberOfRelevantCounters = 10
NumberOfHeroes = 120
HCHeroes = ["Lycan", "Clinkz", "Razor", "Arc Warden", "Riki", "Monkey King", "Chaos Knight", "Juggernaut", "Wraith King", "Bloodseeker", "Troll Warlord", "Luna", "Ursa", "Slardar", "Weaver", "Spectre", "Drow Ranger", "Naga Siren", "Sven", "Slark", "Medusa", "Anti-Mage", "Phantom Lancer", "Ember Spirit", "Morphling", "Terrorblade", "Lifestealer", "Faceless Void", "Gyrocopter"]
MidlanerHeroes = ["Broodmother", "Lycan", "Clinkz", "Razor", "Monkey King", "Riki", "Arc Warden", "Visage", "Enigma", "Puck", "Lone Druid", "Tidehunter", "Alchemist", "Bloodseeker", "Invoker", "Troll Warlord", "Pugna", "Void Spirit", "Death Prophet", "Templar Assassin", "Dragon Knight", "Zeus", "Ursa", "Pangolier", "Windranger", "Huskar", "Earthshaker", "Necrophos", "Leshrac", "Silencer", "Drow Ranger", "Viper", "Timbersaw", "Naga Siren", "Storm Spirit", "Batrider", "Legion Commander", "Queen of Pain", "Anti-Mage", "Tinker", "Ember Spirit", "Shadow Fiend", "Brewmaster", "Medusa", "Mars", "Phantom Lancer", "Elder Titan", "Morphling", "Hoodwink", "Magnus", "Meepo", "Outworld Devourer", "Nature's Prophet", "Kunkka", "Sniper", "Snapfire", "Tiny", "Lina", ]
OfflanerHeroes = ["Nyx Assassin", "Underlord", "Visage", "Enigma", "Puck", "Night Stalker", "Lone Druid", "Tidehunter", "Beastmaster", "Dark Seer", "Omniknight", "Abaddon", "Phoenix", "Sand King", "Treant Protector", "Clockwerk", "Spirit Breaker", "Pangolier", "Slardar", "Earthshaker", "Necrophos", "Undying", "Tusk", "Leshrac", "Timbersaw", "Axe", "Legion Commander", "Earth Spirit", "Brewmaster", "Batrider", "Centaur Warrunner", "Mars", "Elder Titan", "Pudge", "Bristleback", "Nature's Prophet", "Tiny", "Doom", ]
SuppHeroes = ["Nyx Assassin", "Visage", "Enigma", "Night Stalker", "Monkey King", "Bounty Hunter", "Puck", "Ogre Magi", "Shadow Shaman", "Mirana", "Dark Willow", "Omniknight", "Abaddon", "Bane", "Phoenix", "Sand King", "Clockwerk", "Void Spirit", "Warlock", "Spirit Breaker", "Pangolier", "Windranger", "Earthshaker", "Undying", "Tusk", "Leshrac", "Silencer", "Skywrath Mage", "Jakiro", "Earth Spirit", "Io", "Lich", "Pudge", "Batrider", "Vengeful Spirit", "Techies", "Hoodwink", "Witch Doctor", "Keeper of the Light", "Enchantress", "Nature's Prophet", "Kunkka", "Snapfire", "Tiny", "Rubick", "Lina", "Grimstroke", ]
HardSuppHeroes = ["Ogre Magi", "Shadow Shaman", "Ancient Apparition", "Omniknight", "Abaddon", "Bane", "Winter Wyvern", "Treant Protector", "Oracle", "Warlock", "Crystal Maiden", "Chen", "Silencer", "Jakiro", "Lion", "Vengeful Spirit", "Dazzle", "Lich", "Disruptor", "Elder Titan", "Witch Doctor", "Keeper of the Light", "Enchantress", "Rubick", "Shadow Demon", "Grimstroke", ]

""" Get hero stats """
HeroStats_json = requests.get(
    "https://api.opendota.com/api/heroStats",
    headers={"Accept": "application/json"}
).json()


# Class that holds the hero counter
@dataclass
class HeroCounter:
    Name: str
    Disadvantage: float


def GetHeroCounter(HeroId):
    CurrentCounters = [HeroCounter for i in range(NumberOfRelevantCounters)]
    Name = (HeroStats_json[HeroId]['localized_name']).replace(' ', '-')
    Name = Name.lower()
    Page = (scraper.DotaScrape(f'https://pt.dotabuff.com/heroes/{Name}/counters')).scrape()
    for HeroCounterIndex in range(NumberOfRelevantCounters):
        # Getting hero name
        CounterHeroName = (Page.findAll("a", class_="link-type-hero"))[HeroCounterIndex].get_text()
        # Getting hero disadvantage
        HeroDisadvantage = ((Page.findAll("a", class_="link-type-hero"))[HeroCounterIndex].find_next()).get_text()
        # Saving CounterHeroName and HeroDisadvantage
        CurrentCounters[HeroCounterIndex].Name = CounterHeroName
        CurrentCounters[HeroCounterIndex].Disadvantage = HeroDisadvantage
    return CurrentCounters

# TODO: Get hero pick rate
def GetHeroPickRate(HeroId):
    return 0


# TODO: Get hero win rate by name
def GetHeroWinRateByName(HeroName):
    return 0


def GetHeroWinRate(HeroId):
    # Getting AncientWinRate
    if HeroStats_json[HeroId]['6_pick'] != 0:
        AncientWinRate = (HeroStats_json[HeroId]['6_win']) * 100 / HeroStats_json[HeroId]['6_pick']
    # Getting DivideWinRate
    if HeroStats_json[HeroId]['7_pick'] != 0:
        DivineWinRate = (HeroStats_json[HeroId]['7_win']) * 100 / HeroStats_json[HeroId]['7_pick']
    # Getting the mean of the Divine win rate and Ancient win rate which is my current bracket
    return round(((DivineWinRate + AncientWinRate) / 2), 4)

# Variable that saves the pick rate
HeroPickRateBackupArray = np.zeros(NumberOfHeroes)
HeroPickRateArray = np.zeros(NumberOfHeroes)
# Variable that saves the win rate
HeroWinRateBackupArray = np.zeros(NumberOfHeroes)
HeroWinRateArray = np.zeros(NumberOfHeroes)
# Variable that saves the heroes names
HeroNameArray = [str for i in range(NumberOfHeroes)]
HeroNameBackupArray = [str for i in range(NumberOfHeroes)]
# Saving win rate, pick rate and name of each hero
for x in range(NumberOfHeroes):
    # Getting Hero Name
    HeroNameArray[x] = HeroStats_json[x]['localized_name']
    # Getting Hero Win Rate
    HeroWinRateArray[x] = GetHeroWinRate(x)
    # Getting Hero Pick Rate
    HeroPickRateArray[x] = GetHeroPickRate(x)
    # Saving Win Rate with default index
    HeroWinRateBackupArray[x] = HeroWinRateArray[x]
    # Saving Name with default index
    HeroNameBackupArray[x] = HeroNameArray[x]
    # Saving Hero Pick Rate with default index
    HeroPickRateBackupArray[x] = HeroPickRateArray[x]

# Sorting win rate array
HeroWinRateArray = np.sort(HeroWinRateArray)

# Sorting name array according to win rate array
for x in range(NumberOfHeroes):
    for y in range(NumberOfHeroes):
        if HeroWinRateBackupArray[x] == HeroWinRateArray[y]:
            HeroNameArray[y] = HeroNameBackupArray[x]

# TODO: Sorting Pick Rate array from the bigger to lower

'''
# Printing win rate after sort 
for x in range(NumberOfHeroes):
    for y in range(len(MidlanerHeroes)):
        if MidlanerHeroes[y] == HeroNameArray[x]:
            print(f'{HeroNameArray[x]} Win Rate: {HeroWinRateArray[x]}%.')
'''

# Getting mean of top 10 picked heroes
PickRatesMean = math.mean(HeroPickRateArray[0:9])

# Getting CurrentHeroId's victory coefficient
CurrentHeroId = 0
HeroCounters = GetHeroCounter(CurrentHeroId)
LossCoefficient = [for i in range(NumberOfRelevantCounters)]
# Getting loss coefficient
for i in range(NumberOfRelevantCounters):
    LossCoefficient += (GetHeroWinRateByName(HeroCounters[i].Name)*HeroCounters[i].Disadvantage)/abs((GetHeroPickRate(CurrentHeroId) - PickRatesMean))
VictoryCoefficient = GetHeroWinRate(CurrentHeroId) - LossCoefficient
print(VictoryCoefficient)
