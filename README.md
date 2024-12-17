# Phylogenetic analysis of extant Pokémon species
My final project for Phylogenetic Biology.

I reconstructed the evolutionary history of all Generation 1-5 Pokémon, and their ancestral states with regard to various traits available on a public Pokémon API database. I also tested for various confounders and spent some time analyzing the results. 

I chose this project not only because it was fun, but also because the discreteness of the traits I would be modeling (and their small sample size) would make it easier to see inside iqtree and discern different choices it makes. It makes it easier to figure out *why* certain topologies or ancestral states were found. It also makes it easier to change various things in your input and see how they change the output. These types of decisions are much more difficult and complex when working with sequenced DNA, but I think many of them are probably relevant to both morphological and genetic analyses, and so I think it's helpful for both to look deeper into these questions. 

## Methods

### Creating NEXUS and CSV files
I wrote a python program called [file_creator.py](https://colab.research.google.com/drive/1m-btLlmKF7QiCdySDWcPs1hZzrsCqaNH?usp=sharing) (on Google Colab for runtime reasons) which would take as input a list of Pokémon, and output a NEXUS and CSV file depending on various parameters the user can modify in the code. 

These parameters include which traits to include in both analyses. For example, in my final analyses, I included these traits in the NEXUS file: <span style="color:salmon">[type, ability, shape, color, habitat, egg group, highest statistic]</span>, and those plus <span style="color:salmon">[region]</span> in the CSV file. This can be achieved by simply commenting out the part of the code which gets each trait from the API I queried, PokéAPI (using an interface called [Pokebase](https://github.com/PokeAPI/pokebase)). I chose these traits simply because they were the easiest to query from the PokéAPI while still having potential relevance to the Pokémon's evolutionary history (as opposed to something like the original artist's name or the items they can possess). 

I spent a *lot* of my time figuring out how to get these traits from the database into my various files. 

### Choices in NEXUS input
An important choice made in the process was to only take the *first*-listed type and ability of each Pokémon (where Pokémon can have 1-2 types and many abilities). The first-listed type and ability in the database were those earliest assigned to the Pokémon, and I chose them for this reason. I would have liked to take as much information as possible, but as not all Pokémon have the same number of types or abilities, this would produce either unaligned morphological datasets (if I just added all a Pokémon's types and abilities to its NEXUS string) or datasets that were way too large (if I encoded each type and ability as a boolean for whether the Pokémon has it), and in both cases the analyses would be way too influenced by type and ability - probably drowning out the other traits. 

This problem is very interesting to me because it also came up in the paper I presented: the authors decided to encode placement of sound-producing organ as various booleans rather than as a single multi-state trait. It also seems like this problem is somewhat of a parallel to problems with sequenced DNA people presented about, specifically, when one species just has many more sequences than another. 

The other parameter (not counting the list of Pokémon to be analyzed) was <span style="color:lightgreen">[ability encoding method]</span>. The problem was that for discrete morphological traits, iqtree can only handle 31 distinct states, but there are 297 possible first-listed abilities for each Pokémon. 

I came up with two strategies, both with different types of information loss. 

Strategy 1, which I used for most of my analyses, I called <span style="color:violet">map</span>. In this strategy I would take the remainder of each ability index divided by a number *n* from 1-31, and that would be the Pokémon's score. In a sense I split up the abilities into *n* different buckets and encode a Pokémon's ability's bucket in its NEXUS and CSV file. 

Strategy 2 I called <span style="color:violet">multiply</span>, and in this strategy, I use two states to encode ability, and multiplied their values to get the ability index of the Pokémon. The two big problems with this approach are that iqtree doesn't know the states are related, and will probably interpret them as evolving separately, and also that ability is now weighted twice as much as any other trait. This is why I only tested this strategy at the end and didn't use it for most of my analyses. 

I also initially wanted to try mapping this space of 1-297 onto a continuous trait which could range from 0 to 1, but I spent a long time trying to get iqtree to run continuous and discrete traits in tandem and it just wasn't working. However, even this approach has its problems, because I assume iqtree would predict it easier to move from, for example, the 214th ability to the 215th ability, than to the 197th ability, even though the listing of abilities is likely random or uninformative. 

### Running the Analyses
After creating a NEXUS file, I moved it onto the Yale McCleary Computing Cluster and ran iqtree on it (for smaller analyses, with a 2-hour limit, but for my final analyses, with a 24-hour limit). My analyses often took quite a long time, with some exceeding the time limit completely (and thus I had to figure out a way to get them to run faster). 

What I did:

- created an R file ([central.rmd](central.rmd)) to turn a treefile and csv file into various visualizations of the tree's topology and ancestral states

- created treefiles for said groups using iqtree on the Yale McCleary Computing Cluster.
- reconstructed the ancestral states of these Pokémon on the previously mentioned traits, with the addition of <span style="color:salmon">[region]</span>. 
- created visualizations of ancestral states and topology.
- ran one of my analyses but without <span style="color:salmon">[type]</span> as a trait in the NEXUS file.
- ran one of my analyses but encoded <span style="color:salmon">[ability]</span> differently.
- rooted each of my visualizations at Mew, and also at the midpoint of the tree.






## Introduction and Goals
*to be edited later...*

It is a great mystery, and an understudied one at that, 
how Pokémon are related to each other. Many brave souls have tried to
understand the phylogenetic relationships between Pokémon species, but
thus far the currently-known data on all Pokémon has not been
put through a rigorous and replicatable phylogenetic analysis. This
project aims to use morphological data from the PokéAPI in order
to attempt to create a phylogeny of all known Pokémon and 
reconstruct ancestral character states. 

Many have tried reconstructing the phylogenetic tree without using
statistical methods ([1](https://www.reddit.com/r/pokemon/comments/ect3kx/pokemon_phylogenetic_tree_of_life_updated_for), [2](https://www.youtube.com/watch?v=NLuyiw3_I0c), [3](https://jgeekstudies.org/2024/08/24/euarthropod-diversity-in-pokemon-searching-for-the-ancestral-type/), [4](https://www.researchgate.net/publication/323639991_Arthropod_diversity_in_Pokemon), [5](https://www.youtube.com/@Pokecology)), and one group actually did apparently use a Bayesian MCMC analysis ([6](https://www.youtube.com/watch?v=mTItPwZThNM))! However, their research wasn't
well-documented at all (and therefore completely impossible to replicate - this isn't
to down on them because they probably did not consider it as serious as an analysis
of Earth-species, *and* they did this analysis at least 11 years ago, with a different
set of tools and without most of the pokémon we know and love today (including 
all fairy-type pokémon)). Also, they used a very limited set of characteristics and
weighted pokémon type very highly in a way I don't think I will, and they didn't
clamp anything at all, whereas I will probably not include most legendary pokémon in 
my analysis, as they're more like mythical creatures - only one organism alive at any one time, not a species. (However, I do think those people are still really cool for doing this 11 years ago :). 

My analysis will be scientific in all ways it can be, and unscientific in all other ways. 

## Minimum Viable Analysis
For my Minimum Viable Analysis, I have created a few different files, all available in this github repository:
1. ```nexus_creator.py``` is a python program which takes in a list of pokemon as command-line arguments (right now all lowercase, although I'll fix this later), and creates a nexus file named ```output.nex``` which turns their height, weight, statistics (HP, attack, speed, etc.), and first-listed type into a categorical state matrix. Importantly, I was still having bugs with continuous data so for now this program finds the minumum and maximum of each continuous characteristic, and maps this onto the range 0-9, and places each pokémon's value into one of these 10 integer buckets. I also plan to use a lot of other data available via the PokéAPI (which is where I query this data from), but was getting some bugs with characteristics that had more than 32 options (ie moves, abilities, etc.). You can see some of what I planned to do in ```nexml_creator.py```, which is otherwise defunct. *Importantly, this took an EXTREMELY LONG time to run on my computer, so I created a Google CoLab file, accessible here, which has slightly different code just because it's a Google CoLab file: https://colab.research.google.com/drive/1m-btLlmKF7QiCdySDWcPs1hZzrsCqaNH?usp=sharing. 
2. ```output.nex``` is an example of what ```nexus_creator.py``` might output. 
3. ```output.nex.parstree``` is an example of what iqtree2 outputs after running through ```output.nex``` on the cluster. The job script is as follows: 

```
#!/bin/bash
#SBATCH --job-name=iqtree
#SBATCH --time=2:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=1G
#SBATCH -p education

module load IQ-TREE

iqtree2 -s output.nex -bb 1000 -nt AUTO
```

This job script also can take a long time to run, depending on the number of pokémon - as of the time of writing, I've been running a script trying to find the phylogeny of 75 different taxa (nearly all the basic Gen 1 Pokémon) for 31 minutes and 42 seconds. 

4. ```pokeapi_pokemon.txt``` is a temporary file I created which contains the names of every pokémon that is possible to be queried through the PokéAPI. 
5. ```analysis.rmd``` is a copy of our Chapter 08 exercise rmd, which I modified (barely) to view the basic results of my analyses.
6. ```analysis.pdf``` is the pdf output of the previous rmd file. 

## Parameters
Properties to use:
- abilities[0].ability.name
- moves[0].move.name
- stats
- highest stat index
- types[0].type.name
- egg group
-- if pokemon.name in all j of each i EggGroup[i].pokemon_species[j].name
- color
-- if pokemon.name in all j of each i PokemonColor[i].pokemon_species[j].name
- habitat
-- if pokemon.name in all j of each i PokemonHabitat[i].pokemon_species[j].name
- shape
-- if pokemon.name in all j of each i PokemonShape[i].pokemon_species[j].name

can get some stuff with PokemonSpecies
id:
name:
egg_groups:
color:
shape:
habitat: can be null


## Clamping


## Guidelines - you can delete this section before submission

If you would like the writeup to be an executable document (with [knitr](http://yihui.name/knitr/), [jupytr](http://jupyter.org/), or other tools), you can create it as a separate file and put a link to it here in the readme.

The project must be entirely reproducible. In addition to the results, the repository must include all the data (or links to data) and code needed to reproduce the results.

Paste references (including urls) into the reference section, and cite them with the general format (Smith at al. 2003).

OK, here we go.

## Methods

The tools I used were... See analysis files at (links to analysis files).

## Results

The tree in Figure 1...

## Discussion

These results indicate...

The biggest difficulty in implementing these analyses was...

If I did these analyses again, I would...

## References

