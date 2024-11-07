import pokebase as pb
import dendropy as dd

def create_nexml(pokemon_list):
    char_matrix = dd.CharacterMatrix()

    for name in pokemon_list:
        pokemon = pb.pokemon(name)

        taxon = dd.Taxon(label=name.capitalize())
        char_row = char_matrix.new_characters_for_taxon(taxon)

        # height, weight as continuous data
        char_row["height"] = float(pokemon.height)
        char_row["weight"] = float(pokemon.weight)

        # abilities, types, moves as categorical sets
        char_row["abilities"] = {a.ability.name for a in pokemon.abilities}
        char_row["types"] = {t.type.name for t in pokemon.types}
        # only first 10 moves
        char_row["moves"] = {m.move.name for m in pokemon.moves[:10]}

        # location area encounters as a list, also limited to 10
        locations = pb.APIResource('pokemon', name).location_area_encounters()
        location_areas = {loc["location_area"]["name"] for loc in locations[:10]} if locations else {"unknown"}
        char_row["locations"] = location_areas

        # game indices as categorical
        char_row["games"] = {g.version.name for g in pokemon.game_indices}

        # add stats as individual continuous data
        # TODO: check if all pokemon have same number of stats
        for stat in pokemon.stats:
            char_row[f"stat_{stat.stat.name}"] = float(stat.base_stat)

        # add taxon to NeXML dataset
        char_matrix.append(char_row)
    
    # write to NeXML file
    nexml_tree = dd.DataSet()
    nexml_tree.add_char_matrix(char_matrix)
    nexml_tree.write(path="pokedata.xml", schema="nexml")
    print("NeXML file created as 'pokedata.xml")





        