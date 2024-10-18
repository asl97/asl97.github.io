The seeding function may look like any old pseudo-random number generator but it isn't just so, instead it is a specific subclass of pseudo-random generator known as a `random permutation` number generator, in simple terms, it's a perfectly uniform distribution random number generator.

That means once a seed shows up, it will never show up again until all the other possible seed shows up again.

Basically, you have to advance the seed through all possible seed in the 32 bits range, ie: advance the seed 4,294,967,295 times before you get the same seed again.

So rather than being a completely random set of number, it's more like a circular track.

Even without taking the shortcut mentioned in my earlier post, https://github.com/asl97/asl97.github.io/blob/master/blog/2024-08-01_Battle_Cats_Seed_Reverse_Back_Advance.md , I believe it is possible to get more than a 2x speed improvement even while checking every seed when compare to the method used by https://github.com/ampuri/bc-normal-seed-tracking .

Code Proof:
```javascript
// A regular 4,294,967,295 length array is too big to fit in most computer
// so we use an ArrayBuffer instead, using 1 bit per index
// or about ~537MB of memory to store the array
class BitArray extends DataView{
  constructor(n){
    super(new ArrayBuffer(n));
  }

  at(n){
    return this.getUint8(n >>> 3) & (1 << (n & 7)) ? 1 : 0;
  }

  set(n){
    this.setUint8(n >>> 3, this.getUint8(n >>> 3) | (1 << (n & 7)));
  }
}

// advanceSeed function from https://github.com/ampuri/bc-normal-seed-tracking
const advanceSeed = (seed) => {
  seed ^= seed << 13;
  seed = seed >>> 0; // Convert to 32bit unsigned integer
  seed ^= seed >>> 17;
  seed ^= seed << 15;
  seed = seed >>> 0; // Convert to 32bit unsigned integer
  return seed;
};

// The array we are using to mark which seed has been seen
seed_amount_in_bytes = 2**32/8;
if (!Number.isInteger(seed_amount_in_bytes)){throw "seed count should be divisible by 8"};
seeds = new BitArray(seed_amount_in_bytes);

// There is no such seed as 0 so we pre-set it in our array
seeds.set(0);

// Instead of doing a for loop through all ~4b seed at once and
// using if Modulo to check and print progress which is slow,
// We split it up into two for loops, to avoid having to do Modulo
//
// Prime factorization of 4294967295:
// 3 × 5 × 17 × 257 × 65537
// 5 * 257 = 1285
fgroups = 1285;
fgroupsize = (2**32-1)/fgroups;
// Make sure we have a suitable group size to cover all seeds
if (!Number.isInteger(fgroupsize)){throw "Invalid group size"};

// Starting seed
sseed = 1;
gseed = sseed;

// Now we call advanceSeed 4,294,967,295 times and mark each seed as we see them
for (let l=0; l<fgroups; l++){
  console.log(`Checked ${l*fgroupsize} seeds (${l}/${fgroups})`);
  for (let i=0; i<fgroupsize; i++){
    gseed=advanceSeed(gseed);

    // If we seen the seed before, print the times advanceSeed is called
    if (seeds.at(gseed) == 1){
      throw `Dupe Seed Found: ${gseed}, called advanceSeed ${l*fgroupsize+i} times`;
    }

    // Mark the new seed that we get in the array
    seeds.set(gseed);
  }
}

// After we called advanceSeed 4,294,967,295 times, we check if we looped back to our starting seed
if (gseed != sseed){
  throw "Seed doesn't match after calling advanceSeed 4,294,967,295 times";
}

// Check that we seen all the seeds
let missing = false;
for (l=0; l<seed_amount_in_bytes;l++){
  if (seeds.getUint8(l)!=(2**8-1)){
    if (!missing){
      console.log('Missing Seed Detected:');
      missing=true;
    }
    for (i=0;i<8;i++){
      let seed = l*8+i;
      if (seeds.at(seed) != 1){
        console.log(` > ${seed}`);
      }
    }
  }
}

if (!missing){
  console.log('No Missing Seed Detected');
}
```