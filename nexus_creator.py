import pokebase as pb
import sys

# TODO: add EggGroup, PokemonShape, PokemonColor, 
# PokemonHabitat, highest stat, abilities, and moves
# TODO: take out legendaries
# TODO: only include basics OR only include final evos

# so only types, height, weight, and stats
    # 18 types

def get_data(pokemon_list):

    # get pokemon objects
    pokemons = [pb.pokemon(name) for name in pokemon_list]

    # initialize data dictionary
    data = {}

    # find all stats (from first pokemon)
    stats_list = []
    for stat in pokemons[0].stats:
        stat_name = stat.stat.name
        stats_list.append(stat_name)
        print(f"found stat {stat_name}")

    # make stats dictionary
    stats_dict = {stat_name: [] for stat_name in stats_list}

    # alphabetize stats dictionary
    stats_dict = {k: stats_dict[k] for k in sorted(stats_dict)}

    # find height and weight and stats range
    height_list = []
    weight_list = []
    for pokemon in pokemons:
        if (not pokemon.id_):
            print(f"pokemon {pokemon.name} not found")
            sys.exit(1)
        print(f"\npokemon {pokemon.name}")
        print(f"{pokemon.name} height is {pokemon.height}")
        height_list.append(float(pokemon.height))
        print(f"{pokemon.name} weight is {pokemon.weight}")
        weight_list.append(float(pokemon.weight))

        for stat in pokemon.stats:
            if (stats_dict[stat.stat.name] == []):
                stats_dict[stat.stat.name] = [float(stat.base_stat)]
            else:
                stats_dict[stat.stat.name].append(float(stat.base_stat))

    # TODO: actually in the end test stats by distribution, 
    # ie get the sum of all stats and then get the % of that that is HP, attack, etc.
            
    # find max and min for each stat
    for stat in stats_list:
        max_stat = max(stats_dict[stat])
        print(f"max {stat} is {max_stat}")
        min_stat = min(stats_dict[stat])
        print(f"min {stat} is {min_stat}")
        stats_dict[stat] = [min_stat, max_stat]
    
    # find max and min height and weight value
    max_height = max(height_list)
    print(f"max height is {max_height}")
    min_height = min(height_list)
    print(f"min height is {min_height}")
    max_weight = max(weight_list)
    print(f"max weight is {max_weight}")
    min_weight = min(weight_list)
    print(f"min weight is {min_weight}")

    for pokemon in pokemons:
        # force load everything
        pokemon._load()
        print(f"\npokemon {pokemon.name}\n")
        # this assumes every pokemon only has one type
        type_str = pokemon.types[0].type.name
        print(f"Pokemon {pokemon.name} has pre-type: {type_str}")
        type_ = type_to_char(type_str)
        print(f"Pokemon {pokemon.name} has type: {type_}")

        height_fl = float(pokemon.height)
        print(f"Pokemon {pokemon.name} has pre-height: {height_fl}")
        height = int((height_fl - min_height)*9/(max_height-min_height))
        print(f"Pokemon {pokemon.name} has height: {height}")

        weight_fl = float(pokemon.weight)
        print(f"Pokemon {pokemon.name} has pre-weight: {weight_fl}")
        weight = int((weight_fl - min_weight)*9/(max_weight-min_weight))
        print(f"Pokemon {pokemon.name} has weight: {weight}")
        
        this_data = ""
        this_data += type_
        this_data += str(height)
        this_data += str(weight)
        for stat in sorted(pokemon.stats, key=lambda stat: stat.stat.name):
            stat_fl = float(stat.base_stat)
            stat_val = int((stat_fl - stats_dict[stat.stat.name][0])*9/(stats_dict[stat.stat.name][1] - stats_dict[stat.stat.name][0]))
            this_data += str(stat_val)
            print(f"Pokemon {pokemon.name} has pre-{stat.stat.name}: {stat_fl}")
            print(f"Pokemon {pokemon.name} has {stat.stat.name}: {stat_val}")

        data[pokemon.name] = this_data
        print(f"Pokemon {pokemon.name} has data: {data[pokemon.name]}")
    return data

def create_nexus(data):    
    nexus_content = "#NEXUS\nBEGIN DATA;\n"
    nexus_content += f"\tDIMENSIONS NCHAR={len(next(iter(data.values())))} NTAX={len(data)};\n"
    nexus_content += "\tFORMAT DATATYPE=STANDARD GAP=- MISSING=? SYMBOLS=\"0123456789ABCDEFGH\";\n\tMATRIX\n"

    for taxon, states in data.items():
        nexus_content += f"\t{taxon}\t{states}\n"

    nexus_content += ";\nEND;\n"

    with open("output.nex", "w") as file:
        file.write(nexus_content)
    print("Nexus file generated: output.nex")


## MAIN
# create pokemon list
pokemon_list = sys.argv[1:] if len(sys.argv) > 1 else []
if not pokemon_list: 
    print("no command-line pokemon!")
    sys.exit(1)
for pokemon in pokemon_list:
    if (not pb.pokemon(pokemon)):
        print(f"pokemon {pokemon} doesn't exist in the pokebase!")
        sys.exit(1)

# get data from pokemon list
data = get_data(pokemon_list)

# create nexus file from data
create_nexus(data)

def type_to_char(type_):
    match type_.lower():
        case "fire":
            return "0"
        case "water":
            return "1"
        case "grass":
            return "2"
        case "electric":
            return "3"
        case "ice":
            return "4"
        case "ghost":
            return "5"
        case "poison":
            return "6"
        case "dragon":
            return "7"
        case "dark":
            return "8"
        case "flying":
            return "9"
        case "normal":
            return "A"
        case "fairy":
            return "B"
        case "steel":
            return "C"
        case "rock":
            return "D"
        case "bug":
            return "E"
        case "psychic":
            return "F"
        case "fighting":
            return "G"
        case "ground":
            return "H"
        case _:
            return "?"