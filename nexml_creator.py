import pokebase as pb
import dendropy as dd
import sys

def create_nexml(pokemon_list):
    nexml_tree = dd.DataSet()

    # create a matrix for each relevant characteristic
    height_matrix = dd.ContinuousCharacterMatrix(label="Height")
    weight_matrix = dd.ContinuousCharacterMatrix(label="Weight")
    abilities_matrix = dd.StandardCharacterMatrix(label="Abilities")
    types_matrix = dd.StandardCharacterMatrix(label="Types")
    moves_matrix = dd.StandardCharacterMatrix(label="Moves")
    locations_matrix = dd.StandardCharacterMatrix(label="Locations")
    games_matrix = dd.StandardCharacterMatrix(label="Games")

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
        stats_matrices[f"{stat_name}_matrix"] = dd.ContinuousCharacterMatrix(label="Stats")
        
        # add this stat's matrix to the dataset
        nexml_tree.add_char_matrix(stats_matrices[f"{stat_name}_matrix"])
        
    # add each pokemon's data
    for pokemon in pokemons:
        taxon = dd.Taxon(label=pokemon.name.capitalize())

        # need slightly different approach for continuous states
        height_row = height_matrix.new_characters_for_taxon(taxon)
        height_row["height"] = float(pokemon.height)
        
        weight_row = weight_matrix.new_characters_for_taxon(taxon)
        weight_row["weight"] = float(pokemon.weight)

        # add stats as individual continuous data
        # TODO: check if all pokemon have same number of stats
        for stat in pokemon.stats:
            stat_name = stat.stat.name
            stat_row = stats_matrices[f"{stat_name}_matrix"].new_characters_for_taxon(taxon)
            stat_row[stat_name] = float(stat.base_stat)
        
        # read in categorical data
        abilities = {a.ability.name for a in pokemon.abilities}
        types = {t.type.name for t in pokemon.types}
        moves = {m.move.name for m in pokemon.moves[:10]}
        games = {g.version.name for g in pokemon.game_indices[:10]}

        # add categorical data to their respective matrices
        abilities_matrix.add_taxon(taxon)
        abilities_matrix[taxon] = list(abilities)
        
        types_matrix.add_taxon(taxon)
        types_matrix[taxon] = list(types)
        
        moves_matrix.add_taxon(taxon)
        moves_matrix[taxon] = list(moves)

        games_matrix.add_taxon(taxon)
        games_matrix[taxon] = list(games)

        # location area encounters as a list, also limited to 10
        locations = pb.APIResource('pokemon', pokemon.name).location_area_encounters()
        location_areas = {loc["location_area"]["name"] for loc in locations[:10]} if locations else {"unknown"}
        
        locations_matrix.add_taxon(taxon)
        locations_matrix[taxon] = list(location_areas)
    
    # write NeXML file
    nexml_tree.write(path="pokedata.xml", schema="nexml")
    print("NeXML file created as 'pokedata.xml")

pokemon_list = sys.argv[1:] if len(sys.argv) > 1 else []

if not pokemon_list: 
    print("no command-line pokemon!")

create_nexml(pokemon_list)
        