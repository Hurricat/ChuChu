import requests

urlbase = 'https://api.lootbox.eu/pc/'

def ow(username, region = 'us'):
    username = username.replace('#', '-')
    finalurl = urlbase + region + '/' + username + '/allHeroes/'
    response = requests.get(finalurl)
    stats = response.json()
    finalurl = urlbase + region + '/' + username + '/profile'
    response = requests.get(finalurl)
    profile = response.json()

    level = str(profile['data']['level'])
    games = str(profile['data']['games']['played'])
    wins = str(profile['data']['games']['wins'])
    losses = str(profile['data']['games']['lost'])

    kills = stats['FinalBlows'].replace(',', '')
    killassists = int(stats['Eliminations'].replace(',', ''))
    deaths = int(stats['Deaths'].replace(',', ''))
    kd = str('%.2f' % (killassists/deaths))
    killassists = str(killassists)
    deaths = str(deaths)
    damage = stats['DamageDone'].replace(',', '')
    healing = stats['HealingDone'].replace(',', '')
    medals = stats['Medals'].replace(',', '')

    stats1 = "Total stats for " + username + "(Level: " + level + ", Games: " + games + ", W/L: " + wins + "/" + losses + "):\n"
    stats2 = "Kills:         " + kills + "\n"
    stats3 = "Kill Assists:  " + killassists + "\n"
    stats4 = "K/D:           " + kd + "\n"
    stats5 = "Deaths:        " + deaths + "\n"
    stats6 = "Damage:        " + damage + "\n"
    stats7 = "Healing:       " + healing + "\n"
    stats8 = "Medals:        " + medals + "\n"

    fullstats = "```\n" + stats1 + stats2 + stats3 + stats4 + stats5 + stats6 + stats7 + stats8 + "```"

    return fullstats

def owheroes(username, region = 'us'):
    username = username.replace('#', '-')
    finalurl = urlbase + region + '/' + username + '/heroes'
    response = requests.get(finalurl)
    heroes = response.json()
    favheroes = []

    for i in range(8):
        finalurl = urlbase + region + '/' + username + '/hero/' + heroes[i]['name'].replace(': ', '').replace('.', '') + '/'
        response = requests.get(finalurl)
        curhero = response.json()
        if 'GamesPlayed' in curhero:
            favheroes.append({'name':heroes[i]['name'], 'games':int(curhero['GamesPlayed'])})

    favheroes = sorted(favheroes, key=lambda k: k['games'], reverse = True)


    user = "Top 5 Heroes and games played for " + username + ":\n"
    hero1 = (favheroes[0]['name'] + ": ").ljust(15) + str(favheroes[0]['games']) + "\n"
    hero2 = (favheroes[1]['name'] + ": ").ljust(15) + str(favheroes[1]['games']) + "\n"
    hero3 = (favheroes[2]['name'] + ": ").ljust(15) + str(favheroes[2]['games']) + "\n"
    hero4 = (favheroes[3]['name'] + ": ").ljust(15) + str(favheroes[3]['games']) + "\n"
    hero5 = (favheroes[4]['name'] + ": ").ljust(15) + str(favheroes[4]['games']) + "\n"

    topheroes = "```\n" + user + hero1 + hero2 + hero3 + hero4 + hero5 + "```"

    return topheroes 

def owhero(username, hero, region = 'us'):
    finalurl = urlbase + region + '/' + username + '/hero/' + hero + '/'
    response = requests.get(finalurl)
    return response.json()
