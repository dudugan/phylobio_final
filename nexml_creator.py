import pokebase as pb
import dendropy as dd
import requests as rq # just for the annoying locations querying ugh
import sys

def create_nexml(pokemon_list):
    nexml_tree = dd.DataSet()
    taxon_namespace = dd.TaxonNamespace(label="PokemonTaxa")

    # create a matrix for each relevant characteristic
    height_matrix = dd.ContinuousCharacterMatrix(taxon_namespace=taxon_namespace, label="Height")
    weight_matrix = dd.ContinuousCharacterMatrix(taxon_namespace=taxon_namespace, label="Weight")
    abilities_matrix = dd.StandardCharacterMatrix(taxon_namespace=taxon_namespace, label="Abilities")
    types_matrix = dd.StandardCharacterMatrix(taxon_namespace=taxon_namespace, label="Types")
    moves_matrix = dd.StandardCharacterMatrix(taxon_namespace=taxon_namespace, label="Moves")
    locations_matrix = dd.StandardCharacterMatrix(taxon_namespace=taxon_namespace, label="Locations")
    games_matrix = dd.StandardCharacterMatrix(taxon_namespace=taxon_namespace, label="Games")

    # add each matrix to the dataset
    nexml_tree.add_char_matrix(height_matrix)
    nexml_tree.add_char_matrix(weight_matrix)
    nexml_tree.add_char_matrix(abilities_matrix)
    nexml_tree.add_char_matrix(types_matrix)
    nexml_tree.add_char_matrix(moves_matrix)
    nexml_tree.add_char_matrix(locations_matrix)
    nexml_tree.add_char_matrix(games_matrix)

    pokemons = [pb.pokemon(name) for name in pokemon_list]

    stats_matrices = {}

    for stat in pokemons[0].stats:
        stat_name = stat.stat.name.capitalize()

        # create a matrix for this stat
        stats_matrices[f"{stat_name}_matrix"] = dd.ContinuousCharacterMatrix(taxon_namespace=taxon_namespace, label="Stats")
        
        # add this stat's matrix to the dataset
        nexml_tree.add_char_matrix(stats_matrices[f"{stat_name}_matrix"])

    # add all possible types, moves, abilities, game_indices and locations
    types_set = set()
    abilities_set = set()
    moves_set = set()
    locations_set = set()
    games_set = set()

    # populate categorical sets
    for pokemon in pokemons:
        for ability in pokemon.abilities:
            abilities_set.add(ability.ability.name)
        for move in pokemon.moves:
            moves_set.add(move.move.name)
        for type in pokemon.types:
            types_set.add(type.type.name)
        for game in pokemon.game_indices:
            games_set.add(game.version.name)
        encounters_url = pokemon.location_area_encounters
        locations = []
        for i in range(len(encounters_url)):
            location = encounters_url[i].location_area.name
            locations.append(location)
        for loc in locations:
            locations_set.add(loc)

    # make sets into lists to maintain order
    abilities_list = list(abilities_set)
    moves_list = list(moves_set)
    types_list = list(types_set)
    games_list = list(games_set)
    locs_list = list(locations_set)

    # create dictionary for each thing with name as key and index in list as value
    abilities_map = {ability: idx for idx, ability in enumerate(abilities_list)}
    moves_map = {move: idx for idx, move in enumerate(moves_list)}
    types_map = {type_: idx for idx, type_ in enumerate(types_list)}
    games_map = {move: idx for idx, move in enumerate(games_list)}
    locs_map = {type_: idx for idx, type_ in enumerate(locs_list)}

    # create dictionary for each thing with name as key and index in list as value
    abilities_matrix.state_map = abilities_map
    moves_matrix.state_map = moves_map
    types_matrix.state_map = types_map
    games_matrix.state_map = games_map
    locations_matrix.state_map = locs_map
        
    # add each pokemon's data
    for pokemon in pokemons:
        taxon = taxon_namespace.new_taxon(label=pokemon.name.capitalize())

        # read in continuous data and add to matrices
        height_matrix[taxon] = [float(pokemon.height)]
        weight_matrix[taxon] = [float(pokemon.weight)]

        for stat in pokemon.stats:
            stat_name = stat.stat.name.capitalize()
            stats_matrices[f"{stat_name}_matrix"][taxon] = [float(stat.base_stat)]

        # read in categorical data and add to matrices
        # abilities = {a.ability.name for a in pokemon.abilities[:10]}
        # types = {t.type.name for t in pokemon.types}
        # moves = {m.move.name for m in pokemon.moves[:10]}
        # games = {g.version.name for g in pokemon.game_indices[:10]}

        # Read in categorical data (abilities, types, moves, games, and locations) and add to matrices
            # -1 is returned if get doesn't find anything
        abilities_indices = [abilities_map.get(ability.ability.name, -1) for ability in pokemon.abilities[:10]]
        types_indices = [types_map.get(type.type.name, -1) for type_ in pokemon.types]
        moves_indices = [moves_map.get(move.move.name, -1) for move in pokemon.moves[:10]]  
        games_indices = [games_map.get(game.version.name, -1) for game in pokemon.game_indices[:10]] 

        encounters_url = pokemon.location_area_encounters
        locations = []
        for i in range(len(encounters_url)):
            location = encounters_url[i].location_area.name
            locations.append(location)
        locations_indices = [locs_map.get(loc, -1) for loc in locations[:10]]

        # Assign the indices to the appropriate matrices
        abilities_matrix[taxon] = abilities_indices
        types_matrix[taxon] = types_indices
        moves_matrix[taxon] = moves_indices
        games_matrix[taxon] = games_indices
        locations_matrix[taxon] = locations_indices
    
    # write NeXML file
    nexml_tree.write(path="pokedata.xml", schema="nexml")
    print("NeXML file created as 'pokedata.xml")

pokemon_list = sys.argv[1:] if len(sys.argv) > 1 else []

if not pokemon_list: 
    print("no command-line pokemon!")

create_nexml(pokemon_list)
        