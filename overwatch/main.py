import requests

urlbase = 'https://owapi.net/api/v2/u/{0}/{1}'
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
    allstats = requests.get(urlbase.format(username, 'stats')).json()
    print(urlbase.format(username, 'stats'))
    overallstats = allstats['overall_stats']
    gamestats = allstats['game_stats']

    fullstats = (
        "```\n" +
        "Total stats for {0}(Level: {1}, Games: {2}, W/L: {3}/{4} ({5}%)):\n".format(
                                                                         username,
                                                                         overallstats['level'],
                                                                         overallstats['games'],
                                                                         overallstats['wins'],
                                                                         overallstats['losses'],
                                                                         overallstats['win_rate']
                                                                       ) +
        "  Kills:         {0}\n".format(gamestats['final_blows']) +
        "  Kill Assists:  {0}\n".format(gamestats['eliminations']) +
        "  K/D:           {0}\n".format(gamestats['kpd']) +
        "  Deaths:        {0}\n".format(gamestats['deaths']) +
        "  Damage:        {0}\n".format(gamestats['damage_done']) +
        "  Healing:       {0}\n".format(gamestats['healing_done']) +
        "  Medals:        {0}\n".format(gamestats['medals']) +
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
