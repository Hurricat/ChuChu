import aiohttp

urlbase = "http://pokeapi.co/api/v2/{0}/{1}"

async def getJson(url):
    async with aiohttp.get(url) as r:
        js = await r.json()
        return js

async def getBerry(b):
    berry = await getJson(urlbase.format("berry", b.lower().replace(" ", "").replace("berry", "")))
    
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

async def getItem(i):
    item = await getJson(urlbase.format("item", i.replace(" ", "-").lower()))

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

async def getPokemon(p):
    pokemon = await getJson(urlbase.format("pokemon-species", p.lower()))
    name = p.title()
    dex = ""
    types = ""

    #name
    for pokename in pokemon['names']:
        if pokename['language']['name'] == 'en':
            name = pokename['name']
            break
    
    #types for pokemon with one form
    if len(pokemon['varieties']) == 1:
        temppoke = await getJson(pokemon['varieties'][0]['pokemon']['url'])
        t1 = ""
        t2 = ""
        typetempl = "{0} / {1}"
        fintype = ""
        for poketype in temppoke['types']:
            if poketype['slot'] == 1:
                t1 = poketype['type']['name'].title()
            else:
                t2 = poketype['type']['name'].title()
        if len(temppoke['types']) == 1:
            fintype = t1
        else:
            fintype = typetempl.format(t1, t2)
        types = "Type: {0}\n".format(fintype)

    #types for pokemon with multiple forms
    else:
        types = "\nForms:\n"
        for pokeform in pokemon['varieties']:
            temppoke = await getJson(pokeform['pokemon']['url'])
            t1 = ""
            t2 = ""
            typetempl = "{0} / {1}"
            fintype = ""
            formname = ""
            for poketype in temppoke['types']:
                if poketype['slot'] == 1:
                    t1 = poketype['type']['name'].title()
                else:
                    t2 = poketype['type']['name'].title()
            if len(temppoke['types']) == 1:
                fintype = t1
            else:
                fintype = typetempl.format(t1, t2)
            tempform = await getJson(temppoke['forms'][0]['url'])
            if len(tempform['form_names']) > 0:
                for fname in tempform['form_names']:
                    if fname['language']['name'] == 'en':
                        formname = fname['name']
                        break
            else:
                formname = name
            types += "{0}: {1}\n".format(formname, fintype)

    #pokedex entry
    for pokedex in pokemon['flavor_text_entries']:
        if pokedex['language']['name'] == 'en':
            dex += "{0}\n".format(pokedex['flavor_text'])
            break

    returnPoke = (
        "```\n" +
        "Species: {0}\n".format(name) +
        "{0}\n".format(types) +
        "Pokedex:\n{0}\n".format(dex) +
        "```"
    )

    return returnPoke
