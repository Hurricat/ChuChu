import requests

urlbase = 'http://owapi.net/api/v2/u/{0}/{1}'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"
}

def ow(username):
    username = username.replace('#', '-')
    allstats = requests.get(urlbase.replace('v1', 'v2').format(username, 'stats'), headers = headers).json()
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

def owheroes(username):
    username = username.replace('#', '-')
    heroes = requests.get(urlbase.format(username, 'heroes')).json()['heroes']

    mostused = "Top 5 Most Played Heroes and Amount of Games for {0}:\n".format(username)

    for hero in heroes:
        mostused = mostused + "{0}: {1}\n".format(hero['name'].title(), hero['games'])

    return "```\n" + mostused + "```"

def owhero(username, hero):
    username = username.replace('#', '-')
    heroname = hero.replace(' ', '').replace(':', '').replace('.', '')
    heroname = heroname.lower()

    herostats = requests.get(urlbase.format(username, 'heroes/') + heroname).json()['hero_stats']

    returnstats = "{0} stats for {1}:\n".format(username, hero)

    for herostat in herostats:
        returnstats = returnstats + "{0}: {1}\n".format(herostat.replace('_', ' ').title(), herostats[herostat])

    return "```\n" + returnstats + "```"
