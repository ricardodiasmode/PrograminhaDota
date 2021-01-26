""" The objective of this program is return the current best heroes of the meta """
import numpy as np
import json
import scraper
import math
from time import sleep
from copy import deepcopy

NumberOfRelevantCounters = 10
NumberOfHeroes = 120
HCHeroes = ["Lycan", "Clinkz", "Razor", "Arc Warden", "Riki", "Monkey King", "Chaos Knight", "Juggernaut",
            "Wraith King", "Bloodseeker", "Troll Warlord", "Luna", "Ursa", "Slardar", "Weaver", "Spectre",
            "Drow Ranger", "Naga Siren", "Sven", "Slark", "Medusa", "Anti-Mage", "Phantom Lancer", "Ember Spirit",
            "Morphling", "Terrorblade", "Lifestealer", "Faceless Void", "Gyrocopter"]
MidlanerHeroes = ["Broodmother", "Lycan", "Clinkz", "Razor", "Monkey King", "Riki", "Arc Warden", "Visage", "Enigma",
                  "Puck", "Lone Druid", "Tidehunter", "Alchemist", "Bloodseeker", "Invoker", "Troll Warlord", "Pugna",
                  "Void Spirit", "Death Prophet", "Templar Assassin", "Dragon Knight", "Zeus", "Ursa", "Pangolier",
                  "Windranger", "Huskar", "Earthshaker", "Necrophos", "Leshrac", "Silencer", "Drow Ranger", "Viper",
                  "Timbersaw", "Naga Siren", "Storm Spirit", "Batrider", "Legion Commander", "Queen of Pain",
                  "Anti-Mage", "Tinker", "Ember Spirit", "Shadow Fiend", "Brewmaster", "Medusa", "Mars",
                  "Phantom Lancer", "Elder Titan", "Morphling", "Hoodwink", "Magnus", "Meepo",
                  "Outworld Destroyer",
                  "Nature's Prophet", "Kunkka", "Sniper", "Snapfire", "Tiny", "Lina"]
OfflanerHeroes = ["Nyx Assassin", "Underlord", "Visage", "Enigma", "Puck", "Night Stalker", "Lone Druid", "Tidehunter",
                  "Beastmaster", "Dark Seer", "Omniknight", "Abaddon", "Phoenix", "Sand King", "Treant Protector",
                  "Clockwerk", "Spirit Breaker", "Pangolier", "Slardar", "Earthshaker", "Necrophos", "Undying", "Tusk",
                  "Leshrac", "Timbersaw", "Axe", "Legion Commander", "Earth Spirit", "Brewmaster", "Batrider",
                  "Centaur Warrunner", "Mars", "Elder Titan", "Pudge", "Bristleback", "Nature's Prophet", "Tiny",
                  "Doom"]
SuppHeroes = ["Nyx Assassin", "Visage", "Enigma", "Night Stalker", "Monkey King", "Bounty Hunter", "Puck", "Ogre Magi",
              "Shadow Shaman", "Mirana", "Dark Willow", "Omniknight", "Abaddon", "Bane", "Phoenix", "Sand King",
              "Clockwerk", "Void Spirit", "Warlock", "Spirit Breaker", "Pangolier", "Windranger", "Earthshaker",
              "Undying", "Tusk", "Leshrac", "Silencer", "Skywrath Mage", "Jakiro", "Earth Spirit", "Io", "Lich",
              "Pudge", "Batrider", "Vengeful Spirit", "Techies", "Hoodwink", "Witch Doctor", "Keeper of the Light",
              "Enchantress", "Nature's Prophet", "Kunkka", "Snapfire", "Tiny", "Rubick", "Lina", "Grimstroke"]
HardSuppHeroes = ["Ogre Magi", "Shadow Shaman", "Ancient Apparition", "Omniknight", "Abaddon", "Bane", "Winter Wyvern",
                  "Treant Protector", "Oracle", "Warlock", "Crystal Maiden", "Chen", "Silencer", "Jakiro", "Lion",
                  "Vengeful Spirit", "Dazzle", "Lich", "Disruptor", "Elder Titan", "Witch Doctor",
                  "Keeper of the Light", "Enchantress", "Rubick", "Shadow Demon", "Grimstroke"]

# Update hero stat file
scraper.RequestHeroStats()
# Getting hero stats in the file
HeroStatsFile = open("HeroStats.txt", "r")
HeroStatsAsStr = HeroStatsFile.read()
HeroStats_json = json.loads(HeroStatsAsStr)
HeroStatsFile.close()

# Getting number of matches for all heroes
NumberOfMatchesPlayed = 0
for x in range(NumberOfHeroes):
    NumberOfMatchesPlayed += HeroStats_json[x]['6_pick'] + HeroStats_json[x]['7_pick']


def GetHeroVictoryCoefficient(HeroId):
    HeroCountersNames, HeroCountersDisadvantage = GetHeroCounter(HeroId)
    LossCoefficient = np.zeros(NumberOfRelevantCounters)
    VictoryCoefficient = NumberOfRelevantCounters*(GetHeroWinRate(HeroId)**1.5)
    # Getting loss coefficient (probability of losing based on counters)
    for i in range(NumberOfRelevantCounters):
        PickRate = GetHeroPickRate(i)*1000
        Disadvantage = HeroCountersDisadvantage[i]
        if PickRate < 1:
            PickRate = 0
        else:
            PickRate = math.sqrt(PickRate)
        if Disadvantage < 1:
            Disadvantage = 1
        else:
            Disadvantage = math.sqrt(Disadvantage)
        LossCoefficient[i] = math.sqrt(round((GetHeroWinRateByName(HeroCountersNames[i])**2) * Disadvantage * PickRate, 5))
        VictoryCoefficient = VictoryCoefficient - LossCoefficient[i]
    return round(VictoryCoefficient/10, 3)


def GetVictoryCoefficientByPosition(PosHeroes, HeroesCount, PosHeroesDefault):
    PosHeroesSorted = deepcopy(PosHeroesDefault)
    PosVC = np.zeros(HeroesCount)
    for i in range(len(PosHeroes)):
        PosVC[i] = GetHeroVictoryCoefficient(GetHeroIdByName(PosHeroes[i]))
    # Sorting Hero victory coefficient from the bigger to lower
    IndexPos = np.argsort(PosVC)[::-1]
    PosVC = np.sort(PosVC)[::-1]
    # Sorting name array according to PosVC array
    for CurrentIndex in range(len(PosHeroes)):
        PosHeroesSorted[CurrentIndex] = PosHeroesDefault[IndexPos[CurrentIndex]]
    return PosVC, PosHeroesSorted


def GetHeroIdByName(HeroName):
    for i in range(NumberOfHeroes):
        if HeroStats_json[i]['localized_name'] == "Outworld Devourer":
            if HeroName == "Outworld Destroyer":
                return i
        if HeroStats_json[i]['localized_name'] == HeroName:
            return i


def GetHeroCounter(HeroId):
    CurrentCountersName = [str for i in range(NumberOfRelevantCounters)]
    CurrentCountersDisadvantage = [float for i in range(NumberOfRelevantCounters)]
    Name = (HeroStats_json[HeroId]['localized_name']).replace(' ', '-').replace("'", '')
    Name = Name.lower()
    if Name == "outworld-devourer":
        Name = "outworld-destroyer"
    Page = (scraper.DotaScrape(f'https://pt.dotabuff.com/heroes/{Name}/counters')).scrape()
    print(f"Getting {Name}'s counters...")
    for HeroCounterIndex in range(NumberOfRelevantCounters):
        # Getting hero disadvantage
        HeroDisadvantage = ((Page.findAll("a", class_="link-type-hero"))[HeroCounterIndex].find_next()).get_text()
        # Saving CounterHeroName and HeroDisadvantage
        CurrentCountersName[HeroCounterIndex] = (Page.findAll("a", class_="link-type-hero"))[
            HeroCounterIndex].get_text()
        HeroDisadvantage = HeroDisadvantage[:-1]
        CurrentCountersDisadvantage[HeroCounterIndex] = float(HeroDisadvantage)
    return CurrentCountersName, CurrentCountersDisadvantage


def GetHeroPickRate(HeroId):
    return (HeroStats_json[HeroId]['6_pick'] + HeroStats_json[HeroId]['7_pick']) / NumberOfMatchesPlayed


def GetHeroWinRateByName(HeroName):
    return GetHeroWinRate(GetHeroIdByName(HeroName))


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

# Sorting Pick Rate array from the bigger to lower
HeroPickRateArray = np.sort(HeroPickRateArray)[::-1]

# Getting mean of top 10 picked heroes
PickRatesMean = np.mean(HeroPickRateArray[0:9])

# Getting Hc's victory coefficient
print(f"Getting HC's Victory Coefficient...")
HCVC, HCHeroesSorted = GetVictoryCoefficientByPosition(HCHeroes, len(HCHeroes), HCHeroes)
sleep(10)

print("--------")
# Getting Mid's victory coefficient
print(f"Getting MID's Victory Coefficient...")
MIDVC, MIDHeroesSorted = GetVictoryCoefficientByPosition(MidlanerHeroes, len(MidlanerHeroes), MidlanerHeroes)
sleep(10)

print("--------")
# Getting Off's victory coefficient
print(f"Getting OFF's Victory Coefficient...")
OFFVC, OFFHeroesSorted = GetVictoryCoefficientByPosition(OfflanerHeroes, len(OfflanerHeroes), OfflanerHeroes)
sleep(10)

print("--------")
# Getting Supp's victory coefficient
print(f"Getting Supp's Victory Coefficient...")
SUPPVC, SUPPHeroesSorted = GetVictoryCoefficientByPosition(SuppHeroes, len(SuppHeroes), SuppHeroes)
sleep(10)

print("--------")
# Getting HardSupp's victory coefficient
print(f"Getting HardSupp's Victory Coefficient...")
HARDSUPPVC, HARDSUPPHeroesSorted = GetVictoryCoefficientByPosition(HardSuppHeroes, len(HardSuppHeroes), HardSuppHeroes)
print("--------")

# Write in the file all Heroes victory coefficient
Positions = [HCHeroes, MidlanerHeroes, OfflanerHeroes, SuppHeroes, HardSuppHeroes]
HeroesSortedArray = [HCHeroesSorted, MIDHeroesSorted, OFFHeroesSorted, SUPPHeroesSorted, HARDSUPPHeroesSorted]
AllVC = [HCVC, MIDVC, OFFVC, SUPPVC, HARDSUPPVC]
for CurrentHeroIndex in range(len(Positions)):
    if CurrentHeroIndex == 0:
        CurrentPosName = "HCHeroes"
    if CurrentHeroIndex == 1:
        CurrentPosName = "MidlanerHeroes"
    if CurrentHeroIndex == 2:
        CurrentPosName = "OfflanerHeroes"
    if CurrentHeroIndex == 3:
        CurrentPosName = "SuppHeroes"
    if CurrentHeroIndex == 4:
        CurrentPosName = "HardSuppHeroes"
    with open(f"{CurrentPosName} Victory Coefficient.txt", "w") as PosFile:
        PosFile.write(f"{CurrentPosName} Victory coefficient:\n")
        for x in range(len(Positions[CurrentHeroIndex])):
            PosFile.write(
                f"{HeroesSortedArray[CurrentHeroIndex][x]}: {AllVC[CurrentHeroIndex][x]}\n")
    PosFile.close()
    print(f"{CurrentPosName} Victory Coefficient Updated!")
    print("--------")
