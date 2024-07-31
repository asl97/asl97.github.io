I was curous about how the seed tracker works, turns out it was just a dumb bruteforce of all possible seed in the 32 bits range, all 4,294,967,295 seeds

At least that was the implementation on one of the listed seed tracker:

https://ampuri.github.io/bc-normal-seed-tracking/#/finder
https://github.com/ampuri/bc-normal-seed-tracking/blob/master/src/FinderPage.tsx#L54-L64

Looking at how the unit are chosen, I figure that it should be possible to speed up the seed lookup by filter and checking only vaild seeds.

For example, "Dark Catseye", it has a rate of 100 out of 10000, meaning we only need to check x9900-x9999, which could means a speed up of 100x.

A 5 minutes search could be reduce to just slightly above 3 seconds.

https://github.com/ampuri/bc-normal-seed-tracking/blob/master/src/utils/bannerData.tsx#L153-L154
```
      rate: 100,
      units: ["Dark Catseye"],
```

https://github.com/ampuri/bc-normal-seed-tracking/blob/master/src/seedFinderWorker.js#L10-L13
```
const getRarity = ({ seed, rateCumSum }) => {
  const seedMod = seed % 10000;
  return rateCumSum.findIndex((sum) => seedMod < sum);
};
```


However for that to work, we need to reverse how the seed advancement work.

Reversing a pseudo random generator is usually impossible since most data are usually discarded, however battle cats algorithm doesn't discard the data, making it reversible. 

https://github.com/ampuri/bc-normal-seed-tracking/blob/master/src/seedFinderWorker.js#L1-L8
```javascript
const advanceSeed = (seed) => {
  seed ^= seed << 13;
  seed = seed >>> 0; // Convert to 32bit unsigned integer
  seed ^= seed >>> 17;
  seed ^= seed << 15;
  seed = seed >>> 0; // Convert to 32bit unsigned integer
  return seed;
};
```

Like so:

```javascript
const reverseSeed = (seed) => {
    // reverse << 15
    seed15a = seed        & 0b111111111111111;
    seed15b = (seed >> 15 & 0b111111111111111) ^ seed15a;
    seed2c = (seed >> 30) ^ (seed15b & 0b11);
    seed = seed2c << 30 | seed15b << 15 | seed15a;
    seed = seed >>> 0; // Convert to 32bit unsigned integer
    // reverse >>> 17
    seed ^= seed >>> 17;
    // reverse << 13
    seed13a = seed        & 0b1111111111111;
    seed13b = (seed >> 13 & 0b1111111111111) ^ seed13a;
    seed6c = (seed >> 26) ^ (seed13b & 0b111111);
    seed = seed6c << 26 | seed13b << 13 | seed13a;
    seed = seed >>> 0; // Convert to 32bit unsigned integer
    return seed;
}
```

Using this information, one could just search the vaild rarity seed range instead of the whole 32 bits range by slightly modifying the seedFinderWorker.

And then calling reverseSeed on the vaild rarity seed before passing it to the check function.


https://github.com/ampuri/bc-normal-seed-tracking/blob/master/src/seedFinderWorker.js#L81
```
  for (let seed = startSeed; seed < endSeed; seed++) {
```

However this simple modification can only use the first roll rarity which in most cases will have very limit speed up impact.

To maximize the impact performance, one should use the rarest item in the rolls, but figuring out how to reverse the rolling algorithm is currently beyond my ability right now

Specifically how to tell when the seed state is a unit, a reroll or the rarity.

Technically one could just bruteforce reverse by testing `2**backrolls` number of seeds, basically doubling the time it takes to search per backroll, if `rate/10000*(2**backrolls) > 1` then searching this way wouldn't be worth it as it would be faster to search the whole 32 bits range.

Someone might be able to figure a better way with the information I have provided above.

Keywords: Battle Cats Seed Tracker

Source code keywords: advanceSeed ampuri bc-normal-seed-tracking