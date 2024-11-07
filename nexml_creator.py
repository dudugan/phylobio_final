import pokebase as pb
import dendropy as dd
import sys

def create_nexml(pokemon_list):
    char_matrix = dd.StandardCharacterMatrix()

    for name in pokemon_list:
        pokemon = pb.pokemon(name)

        taxon = dd.Taxon(label=name.capitalize())
        char_matrix[taxon] = []

        # height, weight as continuous data
        char_matrix[taxon].append(float(pokemon.height))
        char_matrix[taxon].append(float(pokemon.weight))

        abilities = {a.ability.name for a in pokemon.abilities}
        types = {t.type.name for t in pokemon.types}
        moves = {m.move.name for m in pokemon.moves[:10]}
        games = {g.version.name for g in pokemon.game_indices[:10]}


        # right now this weights height the same as each individual ability; maybe change
        char_matrix[taxon].extend(abilities)
        char_matrix[taxon].extend(types)
        char_matrix[taxon].extend(moves)
        char_matrix[taxon].extend(games)

        # location area encounters as a list, also limited to 10
        locations = pb.APIResource('pokemon', name).location_area_encounters()
        location_areas = {loc["location_area"]["name"] for loc in locations[:10]} if locations else {"unknown"}
        char_matrix[taxon].extend(location_areas)

        # add stats as individual continuous data
        # TODO: check if all pokemon have same number of stats
        for stat in pokemon.stats:
            char_matrix[taxon].append(float(stat.base_stat))
    
    # write to NeXML file
    nexml_tree = dd.DataSet()
    nexml_tree.add_char_matrix(char_matrix)
    nexml_tree.write(path="pokedata.xml", schema="nexml")
    print("NeXML file created as 'pokedata.xml")

pokemon_list = sys.argv[1:] if len(sys.argv) > 1 else []

if not pokemon_list: 
    print("no command-line pokemon!")

create_nexml(pokemon_list)
        