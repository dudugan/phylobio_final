import pokebase as pb
import sys

# testing WITHOUT moves, abilities, games, or locations
# and putting height and weight and stats into buckets

# so only types, height, weight, and stats
    # 18 types

def type_to_char(type_):
    match type_:
        case "fire":
            return "F"
        case "water":
            return "W"
        case "grass":
            return "G"
        case "electric":
            return "E"
        case "ice":
            return "I"
        case "ghost":
            return "H"
        case "poison":
            return "P"
        case "dragon":
            return "D"
        case "dark":
            return "K"
        case "flying":
            return "L"
        case "normal":
            return "N"
        case "fairy":
            return "A"
        case "steel":
            return "S"
        case "rock":
            return "R"
        case "bug":
            return "B"
        case "psychic":
            return "Y"
        case "fighting":
            return "T"
        case "ground":
            return "O"

def get_data(pokemon_list):

    # get pokemon objects
    pokemons = [pb.pokemon(name) for name in pokemon_list]

    # initialize data dictionary
    data = {}

    # find all stats
    stats_list = []
    for stat in pokemons[0].stats:
        stat_name = stat.stat.name
        stats_list.append(stat_name)

    # make stats dictionary
    stats_dict = {stat_name: [] for stat_name in stats_list}

    # alphabetize stats dictionary
    stats_dict = {k: stats_dict[k] for k in sorted(stats_dict)}

    # find height and weight and stats range
    height_list = []
    weight_list = []
    for pokemon in pokemons:
        height_list.append(float(pokemon.height))
        weight_list.append(float(pokemon.weight))
        for stat in pokemon.stats:
            if (stats_dict[stat.stat.name] == []):
                stats_dict[stat.stat.name] = [float(stat.base_stat)]
            else:
                stats_dict[stat.stat.name].append(float(stat.base_stat))
            
    # find max and min for each stat
    for stat in stats_list:
        max_stat = max(stats_dict[stat])
        min_stat = min(stats_dict[stat])
        stats_dict[stat] = [min_stat, max_stat]
    
    # find max and min height and weight value
    max_height = max(height_list)
    min_height = min(height_list)
    max_weight = max(weight_list)
    min_weight = min(weight_list)

    for pokemon in pokemons:
        # this assumes every pokemon only has one type
        type_str = pokemon.type[0]
        type_ = type_to_char(type_str)

        height_fl = float(pokemon.height)
        height = int((height_fl - min_height)*9/(max_height-min_height))
        
        weight_fl = float(pokemon.weight)
        weight = int((weight_fl - min_weight)*9/(max_weight-min_weight))
        
        this_data = ""
        this_data += type_
        this_data += str(height)
        this_data += str(weight)
        for stat in sorted(pokemon.stats, key=lambda stat: stat.stat.name):
            stat_fl = float(stat.base_stat)
            stat_val = int((stat_fl - stats_dict[stat.stat.name][0])*9/(stats_dict[stat.stat.name][1] - stats_dict[stat.stat.name][0]))
            this_data += str(stat_val)

        data[pokemon.name] = this_data
    return data

def create_nexus(data):    
    nexus_content = "#NEXUS\nBEGIN DATA;\n"
    nexus_content += f"\tDIMENSIONS NCHAR={len(next(iter(data.values())))} NTAX={len(data)};\n"
    nexus_content += "\tFORMAT DATATYPE=STANDARD GAP=- MISSING=? SYMBOLS=\"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ\";\n\tMATRIX\n"

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

# get data from pokemon list
data = get_data(pokemon_list)

# create nexus file from data
create_nexus(data)