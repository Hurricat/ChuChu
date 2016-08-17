import sqlite3
conn = sqlite3.connect('pokemon/pokedex.sqlite')
c = conn.cursor()

def cleanInput(i):
    i = i.replace(" ", "-")
    i = i.replace(".", "")
    i = i.lower()
    return i

def getPokemonType(pokemon_id):
    pokemon_types = ""
    for x in range(1, 3):
        c.execute('''
            SELECT
                type_names.name
            FROM
                pokemon_types INNER JOIN type_names ON
                    pokemon_types.type_id = type_names.type_id AND
                    pokemon_types.slot = ? AND
                    type_names.local_language_id = 9
            WHERE
                pokemon_types.pokemon_id = ?
        ''', (x, pokemon_id,))
        cur_type_name = c.fetchone()
        if cur_type_name is not None:
            if x == 2:
                pokemon_types += " / "
            pokemon_types += cur_type_name[0]
    return pokemon_types

def getPokemon(identifier):
    #get species
    i = cleanInput(identifier)
    c.execute('''
        SELECT 
            pokemon_species.id,
            pokemon_dex_numbers.pokedex_number,
            pokemon_species_names.name
        FROM 
            pokemon_species INNER JOIN pokemon_species_names ON
                pokemon_species.id = pokemon_species_names.pokemon_species_id AND
                pokemon_species_names.local_language_id = 9
            INNER JOIN pokemon_dex_numbers ON
                pokemon_species.id = pokemon_dex_numbers.species_id AND
                pokemon_dex_numbers.pokedex_id = 1
        WHERE
            pokemon_species.identifier = ?
    ''', (i,))
    species = c.fetchone()
    species_id = species[0]
    species_dex = species[1]
    species_name = species[2]

    #get forms
    c.execute('''
        SELECT
            pokemon.id,
            pokemon_forms.id,
            pokemon_form_names.form_name
        FROM
            pokemon INNER JOIN pokemon_forms ON
                pokemon.id = pokemon_forms.pokemon_id
            LEFT OUTER JOIN pokemon_form_names ON
                pokemon_forms.id = pokemon_form_names.pokemon_form_id AND
                pokemon_form_names.local_language_id = 9
        WHERE
            pokemon.species_id = ?
    ''', (species_id,))

    pokemon = c.fetchall()
    
    #get types
    types = ""
    type_diff = 0
    if len(pokemon) > 1:
        types = "\nTypes by Form:\n"
        prev_type = ""
        for poke in pokemon:
            pokemon_id = poke[0]
            form_name = poke[2]
            if form_name is None:
                form_name = species_name
            pokemon_types = getPokemonType(pokemon_id)
            if pokemon_types != prev_type and prev_type != "":
                type_diff += 1
            types += "{0}: {1}\n".format(form_name, pokemon_types)
            prev_type = pokemon_types
    if type_diff == 0:
        pokemon_id = pokemon[0][0]
        pokemon_type = getPokemonType(pokemon_id)
        types = "Type: {0}\n".format(pokemon_type)

    #get pokedex
    c.execute('''
        SELECT
            flavor_text
        FROM
            pokemon_species_flavor_text
        WHERE
            species_id = ? AND
            language_id = 9
    ''',(species_id,))
    pokedex = c.fetchall()
    species_dex_entry = pokedex[len(pokedex) - 1][0]

    return_poke = (
        "```\n" +
        "No. {0}\n".format(species_dex) +
        "{0}\n".format(species_name) +
        "{0}".format(types) +
        "\n{0}\n".format(species_dex_entry) +
        "```"
    )

    return return_poke

def getBerry(identifier):
    i = cleanInput(identifier).replace("-berry", "") + "-berry"
    c.execute('''
        SELECT
            berries.id,
            berry_firmness_names.name,
            berries.natural_gift_power,
            type_names.name,
            berries.size,
            berries.max_harvest,
            berries.growth_time,
            berries.soil_dryness,
            berries.smoothness,
            item_names.name
        FROM
            items JOIN berries ON
                items.id = berries.item_id
            JOIN item_names ON
                items.id = item_names.item_id AND
                item_names.local_language_id = 9
            JOIN berry_firmness_names ON
                berries.firmness_id = berry_firmness_names.berry_firmness_id AND
                berry_firmness_names.local_language_id = 9
            JOIN type_names ON
                berries.natural_gift_type_id = type_names.type_id AND
                type_names.local_language_id = 9
        WHERE
            items.identifier = ?
    ''', (i,))

    item = c.fetchone()
    berry_id = item[0]
    firmness = item[1]
    natural_gift_power = item[2]
    natural_gift_type = item[3]
    size = item[4]
    max_harvest = item[5]
    growth_time = item[6]
    soil_dryness = item[7]
    smoothness = item[8]
    name = item[9]

    c.execute('''
        SELECT
            berry_flavors.flavor,
            contest_type_names.name,
            contest_type_names.flavor
        FROM
            berry_flavors JOIN contest_type_names ON
                berry_flavors.contest_type_id = contest_type_names.contest_type_id AND
                contest_type_names.local_language_id = 9 AND
                berry_flavors.flavor > 0
        WHERE
            berry_flavors.berry_id = ?
    ''', (berry_id,))
    flavors = c.fetchall()
    printed_flavors = "Flavors:\n"
    for flavor in flavors:
        amount = flavor[0]
        name1 = flavor[2]
        name2 = flavor[1]
        printed_flavors += "{0} / {1}: {2}\n".format(name1, name2, amount)

    return_berry = (
        "```\n" +
        "{0}\n\n".format(name) +
        "Firmness: {0}\n".format(firmness) +
        "Size: {0}\n".format(size) +
        "Max Harvest: {0}\n".format(max_harvest) +
        "Growth Time: {0}\n".format(growth_time) +
        "Soil Dryness: {0}\n".format(soil_dryness) +
        "Smoothness: {0}\n\n".format(smoothness) +
        "Natural Gift Power: {0}\n".format(natural_gift_power) +
        "Natural Gift Type: {0}\n\n".format(natural_gift_type) +
        printed_flavors +
        "```"
    )

    return return_berry

def getItem(identifier):
    i = cleanInput(identifier)
    c.execute('''
        SELECT
            item_names.name,
            item_flavor_text.flavor_text,
            items.cost,
            items.fling_power,
            item_fling_effect_prose.effect
        FROM
            items LEFT OUTER JOIN item_fling_effect_prose ON
                items.fling_effect_id = item_fling_effect_prose.item_fling_effect_id AND
                item_fling_effect_prose.local_language_id = 9
            JOIN item_names ON
                items.id = item_names.item_id AND
                item_names.local_language_id = 9
            JOIN item_flavor_text ON
                items.id = item_flavor_text.item_id AND
                item_flavor_text.language_id = 9
        WHERE
            items.identifier = ?
        ORDER BY
            item_flavor_text.version_group_id
    ''', (i,))

    itemlist = c.fetchall()
    item = itemlist[len(itemlist) - 1]

    item_name = item[0]
    item_effect = item[1]
    item_cost = item[2]
    item_fp = item[3]
    item_fe = item[4]

    return_item = (
        "```\n" +
        "{0}\n".format(item_name) +
        "Cost: {0}\n\n".format(item_cost) +
        "Fling Power:  {0}\n".format(item_fp) +
        "Fling Effect: {0}\n\n".format(item_fe) +
        "{0}\n".format(item_effect) +
        "```"
    )

    return return_item
