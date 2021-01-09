import requests
import numpy as np
import scrapy

NumberOfHeroes = 120
HCHeroes = ["Lycan", "Clinkz", "Razor", "Arc Warden", "Riki", "Monkey King", "Chaos Knight", "Juggernaut", "Wraith King", "Bloodseeker", "Troll Warlord", "Luna", "Ursa", "Slardar", "Weaver", "Spectre", "Drow Ranger", "Naga Siren", "Sven", "Slark", "Medusa", "Anti-Mage", "Phantom Lancer", "Ember Spirit", "Morphling", "Terrorblade", "Lifestealer", "Faceless Void", "Gyrocopter"]
MidlanerHeroes = ["Broodmother", "Lycan", "Clinkz", "Razor", "Monkey King", "Riki", "Arc Warden", "Visage", "Enigma", "Puck", "Lone Druid", "Tidehunter", "Alchemist", "Bloodseeker", "Invoker", "Troll Warlord", "Pugna", "Void Spirit", "Death Prophet", "Templar Assassin", "Dragon Knight", "Zeus", "Ursa", "Pangolier", "Windranger", "Huskar", "Earthshaker", "Necrophos", "Leshrac", "Silencer", "Drow Ranger", "Viper", "Timbersaw", "Naga Siren", "Storm Spirit", "Batrider", "Legion Commander", "Queen of Pain", "Anti-Mage", "Tinker", "Ember Spirit", "Shadow Fiend", "Brewmaster", "Medusa", "Mars", "Phantom Lancer", "Elder Titan", "Morphling", "Hoodwink", "Magnus", "Meepo", "Outworld Devourer", "Nature's Prophet", "Kunkka", "Sniper", "Snapfire", "Tiny", "Lina", ]
OfflanerHeroes = ["Nyx Assassin", "Underlord", "Visage", "Enigma", "Puck", "Night Stalker", "Lone Druid", "Tidehunter", "Beastmaster", "Dark Seer", "Omniknight", "Abaddon", "Phoenix", "Sand King", "Treant Protector", "Clockwerk", "Spirit Breaker", "Pangolier", "Slardar", "Earthshaker", "Necrophos", "Undying", "Tusk", "Leshrac", "Timbersaw", "Axe", "Legion Commander", "Earth Spirit", "Brewmaster", "Batrider", "Centaur Warrunner", "Mars", "Elder Titan", "Pudge", "Bristleback", "Nature's Prophet", "Tiny", "Doom", ]
SuppHeroes = ["Nyx Assassin", "Visage", "Enigma", "Night Stalker", "Monkey King", "Bounty Hunter", "Puck", "Ogre Magi", "Shadow Shaman", "Mirana", "Dark Willow", "Omniknight", "Abaddon", "Bane", "Phoenix", "Sand King", "Clockwerk", "Void Spirit", "Warlock", "Spirit Breaker", "Pangolier", "Windranger", "Earthshaker", "Undying", "Tusk", "Leshrac", "Silencer", "Skywrath Mage", "Jakiro", "Earth Spirit", "Io", "Lich", "Pudge", "Batrider", "Vengeful Spirit", "Techies", "Hoodwink", "Witch Doctor", "Keeper of the Light", "Enchantress", "Nature's Prophet", "Kunkka", "Snapfire", "Tiny", "Rubick", "Lina", "Grimstroke", ]
HardSuppHeroes = ["Ogre Magi", "Shadow Shaman", "Ancient Apparition", "Omniknight", "Abaddon", "Bane", "Winter Wyvern", "Treant Protector", "Oracle", "Warlock", "Crystal Maiden", "Chen", "Silencer", "Jakiro", "Lion", "Vengeful Spirit", "Dazzle", "Lich", "Disruptor", "Elder Titan", "Witch Doctor", "Keeper of the Light", "Enchantress", "Rubick", "Shadow Demon", "Grimstroke", ]

'''
# Getting all matches
AllMatches_json = requests.get(
    "https://api.opendota.com/api/publicMatches",
    headers={"Accept": "application/json"}
).json()

MatchIndex = 0
# Get all needed info about matches
while MatchIndex < len(AllMatches_json):
    # Verify if the match has the requirements
    if AllMatches_json[MatchIndex]['avg_mmr'] and AllMatches_json[MatchIndex]['game_mode'] == 22 and 5200 > AllMatches_json[MatchIndex]['avg_mmr'] > 3800:
        # print(AllMatches_json[x])

        # Getting the match
        match_ID = AllMatches_json[MatchIndex]['match_id']
        MatchRequestURL = "https://api.opendota.com/api/matches/" + str(match_ID)
        Match_json = requests.get(
            MatchRequestURL,
            headers={"Accept": "application/json"}
        ).json()

        # Getting the heroes of the current match
        PlayerIndex = 0
        while PlayerIndex < 10:
            # Setting hero id to a variable
            HeroID = Match_json['picks_bans'][PlayerIndex]['hero_id']
            if Match_json['picks_bans'][PlayerIndex]['is_pick']:
                # Incrementing the number of times that the hero was picked
                HeroPickRate[HeroID] += 1
                # Incrementing win rate
                if Match_json['radiant_win'] and Match_json['picks_bans'][PlayerIndex]['team']:
                    HeroWinRate[HeroID] += 1
            PlayerIndex += 1

    MatchIndex += 1
'''
""" Get hero stats """
HeroStats_json = requests.get(
    "https://api.opendota.com/api/heroStats",
    headers={"Accept": "application/json"}
).json()


# Variable that saves the win rate
HeroWinRateBackupArray = np.zeros(NumberOfHeroes)
HeroWinRateArray = np.zeros(NumberOfHeroes)
# Variable that saves the heroes names
HeroNameArray = [str for i in range(NumberOfHeroes)]
HeroNameBackupArray = [str for i in range(NumberOfHeroes)]
# Printing win rate of each hero
for x in range(NumberOfHeroes):
    HeroName = HeroStats_json[x]['localized_name']
    if HeroStats_json[x]['6_pick'] != 0:
        AncientWinRate = (HeroStats_json[x]['6_win']) * 100 / HeroStats_json[x]['6_pick']
    if HeroStats_json[x]['7_pick'] != 0:
        DivineWinRate = (HeroStats_json[x]['7_win']) * 100 / HeroStats_json[x]['7_pick']
    # print(f'{HeroName}: Divine Win Rate: {DivineWinRate}%. Ancient Win Rate: {AncientWinRate}%.')
    # Getting the mean of the Divine win rate and Ancient win rate which is my current bracket
    HeroWinRateArray[x] = round(((DivineWinRate + AncientWinRate) / 2), 4)
    HeroWinRateBackupArray[x] = HeroWinRateArray[x]
    HeroNameArray[x] = HeroName
    HeroNameBackupArray[x] = HeroNameArray[x]

# Printing win rate before sort
# for x in range(NumberOfHeroes):
#    print(f'{HeroNameArray[x]} Win Rate: {HeroWinRateArray[x]}%.')

# Sorting win rate array
HeroWinRateArray = np.sort(HeroWinRateArray)

# Sorting name array according to win rate array
for x in range(NumberOfHeroes):
    for y in range(NumberOfHeroes):
        if HeroWinRateBackupArray[x] == HeroWinRateArray[y]:
            HeroNameArray[y] = HeroNameBackupArray[x]

# Printing win rate after sort
for x in range(NumberOfHeroes):
    for y in range(len(MidlanerHeroes)):
        if MidlanerHeroes[y] == HeroNameArray[x]:
            print(f'{HeroNameArray[x]} Win Rate: {HeroWinRateArray[x]}%.')
