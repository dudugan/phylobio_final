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

This problem is very interesting to me because it also came up in the paper I presented: the authors decided to encode placement of sound-producing organs as various booleans rather than as a single multi-state trait. It also seems like this problem is somewhat of a parallel to problems with sequenced DNA people presented about, specifically, when one species just has many more sequences than another. 

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

2. I excluded all legendary, man-made, or alien Pokémon, which canonically did not evolve within the Pokémon universe. This was also both because it makes sense and because these species were causing problems. 

## Results

### Baby Analyses
I first conducted an analysis of all Generation 1 fire-type Pokémon (12 pokémon total). This produces some interesting results - notably, the data for different forms (basic, stage 1, stage 2) of the same species were often identical, so I was forced to combine them with an "_" as you can see here. 

Also, the sole legendary Pokémon *Moltres* failed the chi2 test, indicating that it was too far away from the other species to be reliably placed in the tree. This was a really cool result, because it kind of affirms what is in the Pokémon canon (and therefore signals that the creators were pretty consistent in how they made the stats for legendary Pokémon). 

![alt text](<extra/baby_analysis.png>)

### Final Analyses

Many analyses came in between my baby analyses and my final analyses, but as they're all basically just dysfunctional versions of my final analyses, I didn't include them. My final analyses were all conducted on the same group of 262 Pokémon: all of the non-legendary/man-made/alien basic Pokémon from generations 1-5. I probably could've incorporated more generations into my analysis, but 5 already took a full day on iqtree, and I wanted to spend the rest of my time analyzing rather than generating. I do plan to repeat this analysis with all the generations over break, though. 

I will now provide visualizations of each trait plotted on the topology of my final Gen 1-5 Basic Pokémon tree - the reconstructed ancestral states and the tip states. Note that all of these plots are very high resolution, so to actually view them and scroll around to read everything, you can open them in new tabs or find them in this repository in /basic/ASR/.... 

Also note that all of these trees are rooted at Mew, and you can find the trees rooted at the midpoint instead in /basic no_mew/ASR/.... 

(But first, the topology on its own!:)

![alt text](basic/topology.png)

#### Type:

![alt text](basic/ASR/type/rect.png)

#### Shape:

![alt text](basic/ASR/shape/rect.png)

#### Color:

![alt text](basic/ASR/color/rect.png)

#### Habitat:

![alt text](basic/ASR/habitat/rect.png)

#### Egg Group:

![alt text](basic/ASR/egg_group/rect.png)

#### Highest Statistic:

![alt text](basic/ASR/stat/rect.png)

#### Ability Bucket:

![alt text](basic/ASR/ability/rect.png)

#### Region (not inputted into analysis):

![alt text](basic/ASR/region/rect.png)


## Discussion
In a sense what we are really measuring is how consistent the creators of Pokémon are, so keep that in mind as a lens under which to view this entire discussion. 

### Conclusions from Baby Analyses
Pokémon of the same species have very similar trait values! Also, Pokémon that canonically did not evolve from the big Pokémon evolutionary tree (legendaries, man-made or alien Pokémon, etc.) have sufficiently different trait values to either fail the chi2 test or be grouped all on their own. 

Evidence for this last point is that my final large trees, I hadn't taken out *Jirachi*, *Victini*, and *Celebi*, which are all "mythical" Pokémon - extremely rare and only obtainable via special events - and iqtree often grouped them together (the 'basic' analysis grouped *Victini* and *Celebi*, the analysis without type grouped *Jirachi* and *Victini*, and the analysis using the 'multiply' method of ability encoding grouped all three). 

![alt text](<extra/celebi victini jirachi.png>)

### The Topology Itself
As presented in class, the basic topology can be broadly summarized in terms of Earth organisms (from top to bottom of the tree) - this is the basic tree rooted at Mew:

![alt text](extra/top4.png)
![alt text](extra/top3.png)
![alt text](extra/top2.png)
![alt text](extra/top1.png)

What's really funny to think about here is that water types evolved last. I was wondering whether this had to do with the tree being rooted at Mew, a non-water type, but in fact, when I root the tree at its midpoint, water types also appear near-last:

![alt text](extra/no_mew.png)

I think all this signals though is that water types are pretty distinct from everything else. 


### Ancestral States

The most parsimonious trait were type and egg group - meaning, type and egg group were the traits plotted most parsimoniously across the tree with my ancestral state reconstructions. Many of the other traits were pretty parsimonious as well, just less so. Furthermore, type and egg group seemed to evolve in tandem a lot of the time. 

This makes a sense when you look at what the options for type and egg group actually are:

![alt text](extra/types.png)

![alt text](<extra/egg_groups.png>)

At least six of these options overlap, and yet more are very very similar!

One thing to consider is whether the fact that we have two traits that evolved closely together is the reason *why* these traits are the most parsimoniously distributed across the tree. I didn't get to the ancestral state reconstructions for the analysis without 'type' yet, but if type and egg group are significantly less parsimoniously distributed across the tree, then this might be why. 

The ramifications of this is also interesting to consider for analyses on sequenced DNA. Is it fine that certain areas of the genome will always be really similar to each other, and therefore weighted more heavily, than other parts? Is this good? Is this bad? For what purposes? If so, how do we fix it?

### Type Guessing
One really cool and unexpected result, which I discussed in class, was that the analysis was really good at guessing the second type of certain Pokémon. I only gave iqtree the *first* type of each Pokémon, but a large portion of the Pokémon grouped outside their first type on the tree are actually grouped with their *second* type. 

For example, *Surskit* here is a water and grass type; however, my NEXUS file only contains the information that it's a grass type (thus why it's plotted as green on this type-colored tree). But it was placed with the water types!

![alt text](<extra/surskit.png>)

Similarly, *Skorupi* is a poison and bug type, but iqtree only knew it was a poison type - yet it was grouped with the bug types. 

![alt text](<extra/skorupi.png>)

So why is the model able to guess these things? It probably has to do with one or two of the other traits. Indeed, if we look at egg group, the trait we found to be most similar to type in distribution, we find that *Surskit* and *Skorupi* are grouped with their second type!:

![alt text](<extra/surskit_egg.png>)

![alt text](<extra/skorupi_egg.png>)


### Region Not Good

Plotting region onto our topology did not look good. It seemed to have a pretty random distribution. This could mean two things: First, it could mean that this analysis is pretty flawed, and the only reason region didn't plot nicely is because we didn't put it into our analysis (hence, the only reason the other things plotted well was because we *did*). Second, it could mean there's some other reason why region should be distributed randomly. 

I can't say with complete confidence this is why, but I do think I have a pretty good reason for this result other than our analysis being bad: it makes sense that region should be distributed randomly, because 'region' is the same thing as 'generation' here, and it makes sense that in each generation of Pokémon released by Nintendo, they'd want a full spread of Pokémon of all types, shapes, colors, etc. In each generation, we see a similar spread of varied Pokémon. 

And we can actually get evidence about this hypothesis just by looking again at the region tree. We are trying to figure out whether the distribution is truly random, or whether the distribution is *even* - not clumps of Pokémon from region 1 and clumps of Pokémon from region 2, but region 1 spanning the full tree, and region 2 spanning the full tree, and so on. Whereas if it was completely random we'd actually be *more* likely to see clumps, out of pure chance. 

![alt text](<extra/region_zoom.png>)

Sure enough, that's what we see! Even just looking at a small part of the larger tree, in each tiny sub-branch, we can almost always see at least one representative from all five regions - they are very evenly split. 

### When Not Rooting at Mew

Changing where we root the tree doesn't actually change much! The one interesting thing to note here is that water types still evolve somewhat late, and that the midpoint of the tree is determined to be a normal type. 

Here's the topology:

![alt text](<basic no_mew/topology.png>)

### When Without Type

Without type, things get kind of crazy...

![alt text](<no_type/topology.png>)

I can still tell why certain things happen - so I know my NEXUS file didn't get super corrupted because I subtracted a trait or something - but all in all, the phylogeny just makes less intuitive sense. 

Either this is because type was just really that important to the analysis, or this is because *anything* would be that important, and subtracting *anything* from it would result in a similarly weird topology. I really want to take out other traits to figure this out!


### Using the 'Multiply' Method

In contrast to this, the 'multiply' method topology actually *seems* really nice and in accordance with my expectations. I want to devote more time to thinking about why this is - I'm really not sure why this would work so well. Maybe ability bucket was just not helping to begin with, but then why would doubling its weight make anything better?

![alt text](<multiply/topology.png>)

## The Future of This Project
I think I will continue to do work on this over winter break, mostly just because I think it's cool and I want to see what the results are/make a more finished analysis. (Also, I'm taking a gap semester in the spring so I'll have time!). With that in mind, here are some of the things I plan to do in the near future!

- Take out all of the rest of the traits one by one, not just type, and see how that impacts the analysis (and not just the topology but the reconstructed states as well). 
- Get my ancestral state reconstruction to work on the no_type and multiply analyses. 
- Utilize 'fossil' pokémon for internal nodes. 
- Get iqtree to take less time in generating the trees, and verify that it's not stopping too early all the time. 

<!-- ## Introduction and Goals
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

My analysis will be scientific in all ways it can be, and unscientific in all other ways.  -->
