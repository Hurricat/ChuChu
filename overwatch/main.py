import aiohttp

urlbase = 'http://owapi.net/api/v2/u/{0}/{1}'

async def getJson(url):
    async with aiohttp.get(url) as r:
        js = await r.json()
        return js

async def ow(username):
    username = username.replace('#', '-')
    allstats = await getJson(urlbase.format(username, 'stats/general'))
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

async def owheroes(username):
    username = username.replace('#', '-')
    heroes = await getJson(urlbase.format(username, 'heroes/general'))
    heroes = heroes['heroes']

    mostused = "Heroes Played and Playtime for {0}:\n".format(username)

    for hero in heroes:
        mostused += "{0}: {1} hours\n".format(hero.title(), heroes[hero])

    return "```\n" + mostused + "```"

async def owhero(username, hero):
    username = username.replace('#', '-')
    heroname = hero.replace(' ', '').replace(':', '').replace('.', '')
    heroname = heroname.lower()

    herostats = await getJson(urlbase.format(username, 'heroes/') + heroname)
    herostats = herostats['hero_stats']

    returnstats = "{0} stats for {1}:\n".format(username, hero)

    for herostat in herostats:
        returnstats = returnstats + "{0}: {1}\n".format(herostat.replace('_', ' ').title(), herostats[herostat])

    return "```\n" + returnstats + "```"
