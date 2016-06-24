import requests

urlbase = 'https://api.lootbox.eu/pc/{0}/{1}/{2}'
heroes = [
    'Genji',
    'Pharah',
    'McCree',
    'Reaper',
    'Soldier: 76',
    'Tracer',
    'Bastion',
    'Hanzo',
    'Junkrat',
    'Mei',
    'Torbjorn',
    'Widowmaker',
    'D.Va',
    'Reinhardt',
    'Roadhog',
    'Winston',
    'Zarya',
    'Lucio',
    'Mercy',
    'Symmetra',
    'Zenyatta'
]

def ow(username, region = 'us'):
    username = username.replace('#', '-')
    stats = requests.get(urlbase.format(region, username, 'allHeroes/')).json()
    profile = requests.get(urlbase.format(region, username, 'profile')).json()['data']

    fullstats = (
        "```\n" +
        "Total stats for {0}(Level: {1}, Games: {2}, W/L: {3}/{4}):\n".format(
                                                                         username,
                                                                         profile['level'],
                                                                         profile['games']['played'],
                                                                         profile['games']['wins'],
                                                                         profile['games']['lost']
                                                                       ) +
        "  Kills:         {0}\n".format(stats['FinalBlows']) +
        "  Kill Assists:  {0}\n".format(stats['Eliminations']) +
        "  K/D:           {0}\n".format(str('%.2f' % (int(stats['Eliminations'].replace(',', ''))/int(stats['Deaths'].replace(',', ''))))) +
        "  Deaths:        {0}\n".format(stats['Deaths']) +
        "  Damage:        {0}\n".format(stats['DamageDone']) +
        "  Healing:       {0}\n".format(stats['HealingDone']) +
        "  Medals:        {0}\n".format(stats['Medals']) +
        "```"
    )

    return fullstats

def owheroes(username, region = 'us'):
    username = username.replace('#', '-')
    topheroes = []
    for hero in heroes:
        curhero = requests.get(urlbase.format(region, username, 'hero/') + hero.replace(': ', '').replace('.', '') + '/').json()
        if 'GamesPlayed' in curhero:
            topheroes.append({'name':hero, 'games':int(curhero['GamesPlayed'])})

    topheroes = sorted(topheroes, key=lambda k: k['games'], reverse = True)

    mostused = ("Top 5 Heroes and games played for {0}:\n".format(username))
    for i in range(5):
        mostused = mostused + "  {0}{1}\n".format((topheroes[i]['name'] + ": ").ljust(15), topheroes[i]['games'])

    return "```\n" + mostused + "```"

def owhero(username, hero, region = 'us'):
    finalurl = urlbase + region + '/' + username + '/hero/' + hero + '/'
    response = requests.get(finalurl)
    return response.json()
