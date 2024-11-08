import pokebase as pb
import dendropy as dd
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
        stats_matrices[f"{stat_name}_matrix"] = dd.ContinuousCharacterMatrix(taxon_namespace=taxon_namespace, label=stat_name)
        
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
        for ability in pokemon.abilities[:10]:
            abilities_set.add(ability.ability.name)
        for move in pokemon.moves[:10]:
            moves_set.add(move.move.name)
        for type_ in pokemon.types:
            types_set.add(type_.type.name)
        for game in pokemon.game_indices[:1]:
            games_set.add(game.version.name)
        encounters_url = pokemon.location_area_encounters
        locations = []
        for i in range(min(len(encounters_url), 9)):
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

    print("Abilities Map:", abilities_map)
    print("Abilities List:", abilities_list)
    print("Moves Map:", moves_map)
    print("Moves List:", moves_list)
    print("Types Map:", types_map)
    print("Types List:", types_list)
    print("Games Map:", games_map)
    print("Games List:", games_list)
    print("Locations Map:", locs_map)
    print("Locations List:", locs_list)

    # create dictionary for each thing with name as key and index in list as value
    abilities_matrix.state_map = abilities_map
    moves_matrix.state_map = moves_map
    types_matrix.state_map = types_map
    games_matrix.state_map = games_map
    locations_matrix.state_map = locs_map
        
    # add each pokemon's data
    for pokemon in pokemons:
        print("Pokémon:", pokemon.name.capitalize())
        taxon = taxon_namespace.new_taxon(label=pokemon.name.capitalize())

        # read in continuous data and add to matrices
        height_matrix[taxon] = [float(pokemon.height)]
        weight_matrix[taxon] = [float(pokemon.weight)]
        print("Height:", float(pokemon.height))
        print("Weight:", float(pokemon.height))

        for stat in pokemon.stats:
            stat_name = stat.stat.name.capitalize()
            stats_matrices[f"{stat_name}_matrix"][taxon] = [float(stat.base_stat)]
            print(f"{stat_name}:", float(stat.base_stat))

        # read in categorical data and add to matrices
        abilities = {a.ability.name for a in pokemon.abilities[:10]}
        types = {t.type.name for t in pokemon.types}
        moves = {m.move.name for m in pokemon.moves[:10]}
        games = {g.version.name for g in pokemon.game_indices[:1]}
        print("Abilities:", abilities)
        print("Types:", types)
        print("Moves:", moves)
        print("Last Game:", games)

        # Read in categorical data (abilities, types, moves, games, and locations) and add to matrices
            # -1 is returned if get doesn't find anything
        abilities_indices = [abilities_map.get(ability, -1) for ability in abilities]
        types_indices = [types_map.get(type_, -1) for type_ in types]
        moves_indices = [moves_map.get(move, -1) for move in moves]  
        games_indices = [games_map.get(game, -1) for game in games] 
        print("Ability Indices:", abilities_indices)
        print("Type Indices:", types_indices)
        print("Move Indices:", moves_indices)
        print("Last Game Index:", games_indices)

        encounters_url = pokemon.location_area_encounters
        locations = []
        for i in range(len(encounters_url)):
            location = encounters_url[i].location_area.name
            locations.append(location)
        print("Locations:", locations)
        locations_indices = [locs_map.get(loc, -1) for loc in locations[:10]]
        print("Location Indices:", locations_indices)

        # Assign the indices to the appropriate matrices
        abilities_matrix[taxon] = abilities_indices if abilities_indices else [-1]
        types_matrix[taxon] = types_indices if types_indices else [-1]
        moves_matrix[taxon] = moves_indices if moves_indices else [-1]
        games_matrix[taxon] = games_indices if games_indices else [-1]
        locations_matrix[taxon] = locations_indices if locations_indices else [-1]

        print("Ability Matrix:", abilities_matrix)
        print("Location Matrix:", locations_matrix)
    
    # write NeXML file
    nexml_tree.write(path="pokedata.xml", schema="nexml")
    print("NeXML file created as 'pokedata.xml")

pokemon_list = sys.argv[1:] if len(sys.argv) > 1 else []

if not pokemon_list: 
    print("no command-line pokemon!")

create_nexml(pokemon_list)
        