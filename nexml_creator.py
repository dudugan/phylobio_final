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
        abilities = {a.ability.name for a in pokemon.abilities}
        types = {t.type.name for t in pokemon.types}
        moves = {m.move.name for m in pokemon.moves[:10]}
        games = {g.version.name for g in pokemon.game_indices[:10]}

        abilities_matrix[taxon] = list(abilities)
        types_matrix[taxon] = list(types)
        moves_matrix[taxon] = list(moves)
        games_matrix[taxon] = list(games)

        # location area encounters as a list, also limited to 10
        encounters_url = pokemon.location_area_encounters
        # splitting by slash gives us the last two things in the url
        locations = pb.APIResource(encounters_url.split('/')[-2], encounters_url('/')[-1])

        # locations = pokemon.location_area_encounters
        location_areas = {loc["location_area"]["name"] for loc in locations[:10]} if locations else {"unknown"}
        
        
        # if encounters_url:
        #     response = rq.get(encounters_url)
        #     if response.status_code == 200:
        #         locations = response.json()
        #         location_areas = {loc["location_area"]["name"] for loc in locations[:10]} if locations else {"unknown"}
        #     else:
        #         location_areas = {"unknown"}
        # else:
        #     location_areas = {"unknown"}

        locations_matrix[taxon] = list(location_areas)
    
    # write NeXML file
    nexml_tree.write(path="pokedata.xml", schema="nexml")
    print("NeXML file created as 'pokedata.xml")

pokemon_list = sys.argv[1:] if len(sys.argv) > 1 else []

if not pokemon_list: 
    print("no command-line pokemon!")

create_nexml(pokemon_list)
        