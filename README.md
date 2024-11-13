# Phylogenetic analysis of primate nocturnality, sociality and communication
My final project for Phylogenetic Biology.

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
statistical methods ([1](https://www.reddit.com/r/pokemon/comments/ect3kx/pokemon_phylogenetic_tree_of_life_updated_for), [2](https://www.youtube.com/watch?v=NLuyiw3_I0c, https://jgeekstudies.org/2024/08/24/euarthropod-diversity-in-pokemon-searching-for-the-ancestral-type/), [3](https://www.researchgate.net/publication/323639991_Arthropod_diversity_in_Pokemon), [4](https://www.youtube.com/@Pokecology)), and one group actually did apparently use a Bayesian MCMC analysis ([5](https://www.youtube.com/watch?v=mTItPwZThNM))! However, their research wasn't
well-documented at all (and therefore completely impossible to replicate - this isn't
to down on them because they probably did not consider it as serious as an analysis
of Earth-species) *and* they did this analysis at least 11 years ago, with a different
set of tools and without most of the pokémon we know and love today (including 
all fairy-type pokémon)? Also, they used a very limited set of characteristics and
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

