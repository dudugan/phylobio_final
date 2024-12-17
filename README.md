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

Importantly, I also wanted to figure out what would happen if I took out each trait from my NEXUS input - how would the topology change? So I ran one analysis where my NEXUS file did not take into account Pokémon type. I couldn't get to the others because each iqtree run took about a day, but I would like to in the future!

### Running the Analyses
After creating a NEXUS file, I moved it onto the Yale McCleary Computing Cluster and ran iqtree on it (for smaller analyses, with a 2-hour limit, but for my final analyses, with a 24-hour limit). My analyses often took quite a long time, with some exceeding the time limit completely or stopping themselves before reaching a solution - I solved the latter issue by allowing them more iterations before stoppage, but the former remains unsolved. 

### Visualizing the Results, and Reconstructing Ancestral States

I created an R file called [central.rmd](central.rmd) to turn a .treefile and .csv file into various visualizations of the tree's topology and ancestral states. I also tried to create an ARD model for each trait, but as of right now this doesn't work on larger trees. 

I also visualized everything both rooted at Mew (the canonical ancestor of all Pokémon) and at the midpoint of the tree. 

### Excluding Certain Pokémon

One last thing to note is that I excluded certain Pokémon from my analyses. There are two main ways this happened:

1. I excluded all non-Basic Pokémon. "Basic" Pokémon can be thought of as the first stage in each Pokémon's species' life cycle, with "Stage 1" and "Stage 2" Pokémon being the next stages. Many Pokémon species have only basic forms; many have only basics and stage 1s, and many have all three forms. The 'species' is the grouping of all 1-3 Pokémon - I included one Pokémon per species. I did this partly because it just makes sense to me to perform the analysis on the species level, but also because Pokémon of the same species were actually causing problems by being too similar to each other in my initial analyses. 

2. I excluded all legendary, man-made, mythical, or alien Pokémon, which canonically did not evolve within the Pokémon universe. This was also both because it makes sense and because these species were causing problems. 

## Results

### Baby Analyses
I first conducted an analysis of all Generation 1 fire-type Pokémon (12 pokémon total). This produces some interesting results - notably, the data for different forms (basic, stage 1, stage 2) of the same species were often identical, so I was forced to combine them with an "_" as you can see here. 

Also, sole legendary Pokémon *Moltres* failed the chi-2 test, indicating that it was too far away from the other species to be reliably placed in the tree. This was a really cool result, because it kind of affirms what is in the Pokémon canon (and therefore signals that the creators were pretty consistent in how they made the stats for legendary Pokémon). 

![alt text](<Screenshot 2024-12-17 at 13.23.33.png>)

### Final Analyses

Many analyses came in between my baby analyses and my final analyses, but as they're all basically just dysfunctional versions of my final analyses, I didn't include them. My final analyses were all conducted on the same group of 262 Pokémon: all of the non-legendary/man-made/alien/mythical basic Pokémon from generations 1-5. I probably could've incorporated more generations into my analysis, but 5 already took a full day on iqtree, and I wanted to spend the rest of my time analyzing rather than generating. I do plan to repeat this analysis with all the generations over break, though. 

The topology of my final Gen1-5 basic Pokémon tree looks like this:





## Discussion

These results indicate...

The biggest difficulty in implementing these analyses was...

If I did these analyses again, I would...

## References



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