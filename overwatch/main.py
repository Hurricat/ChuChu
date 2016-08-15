import json
import urllib3
import certifi

urlbase = 'http://owapi.net/api/v2/u/{0}/{1}'
http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())

def ow(username):
    username = username.replace('#', '-')
    r = http.request('GET', urlbase.format(username, 'stats/general'))
    allstats = json.loads(r.data.decode('utf-8'))
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
    r = http.request('GET', urlbase.format(username, 'heroes/general'))
    heroes = json.loads(r.data.decode('utf-8'))['heroes']

    mostused = "Heroes Played and Playtime for {0}:\n".format(username)

    for hero in heroes:
        mostused = mostused + "{0}: {1} hours\n".format(hero.title(), heroes[hero])

    return "```\n" + mostused + "```"

def owhero(username, hero):
    username = username.replace('#', '-')
    heroname = hero.replace(' ', '').replace(':', '').replace('.', '')
    heroname = heroname.lower()

    r = http.request('GET', urlbase.format(username, 'heroes/') + heroname)
    herostats = json.loads(r.data.decode('utf-8'))['hero_stats']

    returnstats = "{0} stats for {1}:\n".format(username, hero)

    for herostat in herostats:
        returnstats = returnstats + "{0}: {1}\n".format(herostat.replace('_', ' ').title(), herostats[herostat])

    return "```\n" + returnstats + "```"
