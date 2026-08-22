Title: Modern games sucks on 16GB ram

It seems games nowadays assumes every computer has VRAM, at least 3GB worth.

Which is just not true, such as on handhelds and laptop where the igpu is deemed good enough.

Windows wants 6GB, game wants 6GB ram + 3GB VRAM, that leaves only 1GB for file cache, which just isn't enough, everything lags if there's any background tasks running. File cache miss everywhere.

Not to mention the memory leaks that plague every games nowadays, that 1GB would be gone in a few minutes of playing and everything would hang or get OOM killed.

Every game just straight up abuse memory by loading everything to ram, what happen to loading on demand and unloading to free up memory? It just gone from modern game.

They don't even save data properly anymore, dumping hundreds of MB of hundreds of json files and then calling external tool to zip it up and then deleting those json files, what happen to integrating zip library and creating the zip file using the library addfile in memory so as not to have needless IO? This kind of BS would hang an HDD for 5 minutes or more, not to mention for people playing on Android with it's slow ass permission checking virtual file system.

Modern gaming sucks
