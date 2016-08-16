import json
import urllib3
import certifi

urlbase = "http://pokeapi.co/api/v2/{0}/{1}"
http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())

def getJson(url):
    r = http.request('GET', url)
    return json.loads(r.data.decode('utf-8'))

def getBerry(b):
    berry = getJson(urlbase.format("berry", b.lower().replace(" ", "").replace("berry", "")))
    
    name = berry['name'].title()
    time = berry['growth_time']
    harvest = berry['max_harvest']
    npower = berry['natural_gift_power']
    ntype = berry['natural_gift_type']['name'].title()
    size = berry['size']
    smooth = berry['smoothness']
    soil = berry['soil_dryness']
    firm = berry['firmness']['name'].title()
    flavors = berry['flavors']

    returnBerry = (
        "```\n" +
        "Berry:              {0}\n".format(name) +
        "Growth Time:        {0}\n".format(time) +
        "Max Harvest:        {0}\n".format(harvest) +
        "Natural Gift Type:  {0}\n".format(ntype) +
        "Natural Gift Power: {0}\n".format(npower) +
        "Size:               {0}\n".format(size) +
        "Soil Dryness:       {0}\n".format(soil) +
        "Firmness:           {0}\n\n".format(firm) +
        "Flavors:\n"
    )

    for flavor in flavors:
        if flavor['potency'] > 0:
            returnBerry += "{0}: {1}\n".format(flavor['flavor']['name'].title(), flavor['potency'])

    returnBerry += "```"

    return returnBerry

def getItem(i):
    item = getJson(urlbase.format("item", i.replace(" ", "-").lower()))

    name = item['names'][0]['name']
    cost = item['cost']
    if item['fling_effect'] is not None:
        fpower = item['fling_power']
        feffect = item['fling_effect']['name'].title()
    else:
        fpower = "N/A"
        feffect = "N/A"
    effect = item['effect_entries'][0]['short_effect']
    
    returnItem = (
        "```\n" +
        "Item Name:    {0}\n".format(name) +
        "Shop Cost:    {0}\n".format(cost) +
        "Fling Power:  {0}\n".format(fpower) +
        "Fling Effect: {0}\n".format(feffect) +
        "Effect:       {0}\n".format(effect) +
        "```"
    )

    return returnItem

def getPokemon(p):
    pokemon = getJson(urlbase.format("pokemon-species", p.lower()))
    name = p.title()
    dex = ""

    for pokename in pokemon['names']:
        if pokename['language']['name'] == 'en':
            name = pokename['name']
            break

    for pokedex in pokemon['flavor_text_entries']:
        if pokedex['language']['name'] == 'en':
            dex += "{0}\n".format(pokedex['flavor_text'])
            break

    returnPoke = (
        "```\n" +
        "Species: {0}\n\n".format(name) +
        "Pokedex:\n{0}\n".format(dex) +
        "```"
    )

    return returnPoke
