import requests

urlbase = 'https://owapi.net/api/v1/u/{0}/{1}'

def ow(username, region = 'us'):
    username = username.replace('#', '-')
    allstats = requests.get(urlbase.format(username, 'stats')).json()
    overallstats = allstats['overall_stats']
    gamestats = allstats['game_stats']

    fullstats = (
        "```\n" +
        "Total stats for {0}(Level: {1}, Games: {2}, W/L: {3}/{4} ({5}%)):\n"
            .format(
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
    heroes = requests.get(urlbase.format(username, 'heroes')).json()['heroes']

    mostused = "Top 5 Most Played Heroes and Amount of Games for {0}:\n".format(username)

    for hero in heroes:
        mostused = mostused + "{0}: {1}\n".format(hero['name'].title(), hero['games'])

    return "```\n" + mostused + "```"

def owhero(username, hero, region = 'us'):
    finalurl = urlbase + region + '/' + username + '/hero/' + hero + '/'
    response = requests.get(finalurl)
    return response.json()
