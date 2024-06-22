Rimworld: Where the bulk drug recipe is located in the source code(core)

TLDL: the bulk recipe is added by `bulkRecipeCount` in `Data/Core/Defs/Drugs/DrugBases.xml`

I was searching everywhere in the "source code"(xml) in the official expansion folder(data) and couldn't find where the bulk version of the recipe was added anywhere easily.

I tried searching online and all I could find was that it was added in rimworld 1.1 and nothing about where specifically it was in the source.
https://steamcommunity.com/sharedfiles/filedetails/?id=2016906815 
https://www.reddit.com/r/RimWorld/comments/qjtpck/what_mod_is_adding_the_4x_bulk_cookingdrug_making/

I even used grepWin to try searching for it
https://github.com/stefankueng/grepWin

Only after a few days of thinking, I thought maybe it was in the base and it was indeed in `MakeableDrugBase`

This blog post is created incase anyone else searches for where is the bulk recipe added in vanilla.

Keywords: rimworld bulk psychite tea drug vanilla source code x4 Yayo Flake
Source code keywords: PsychoidLeaves PsychoidBrewing "Making psychite tea x4"