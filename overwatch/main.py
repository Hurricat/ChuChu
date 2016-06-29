import requests

urlbase = 'https://owapi.net/api/v1/u/{0}/{1}'
herobase = {
    "roadhog": "1",
    "junkrat": "2",
    "lucio": "3",
    "soldier76": "4",
    "zarya": "5",
    "mccree": "6",
    "tracer": "7",
    "reaper": "8",
    "widowmaker": "9",
    "winston": "10",
    "pharah": "11",
    "reinhardt": "12",
    "symmetra": "13",
    "torbjorn": "14",
    "bastion": "15",
    "hanzo": "16",
    "mercy": "17",
    "zenyatta": "18",
    "mei": "20",
    "genji": "21",
    "dva": "22"
}

def ow(username):
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
    heroid = herobase[heroname]

    herostats = requests.get(urlbase.format(username, 'heroes/') + heroid).json()['stats']

    returnstats = "{0} stats for {1}:\n".format(username, hero)

    for herostat in herostats:
        if herostat['name'] == "hero-specific stats":
            for stat in herostat['stats']:
                returnstats = returnstats + "{0}: {1}\n".format(stat['name'].title(), stat['value'])
            break

                

    return "```\n" + returnstats + "```"
