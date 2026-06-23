# Random number generation

Many algorithms in trading require the generation of random numbers. MQL5 provides two functions that initialize and then poll the pseudo-random integer generator.

To get a better "randomness", you can use the Alglib library available in MetaTrader 5 (see MQL5/Include/Math/Alglib/alglib.mqh).

void MathSrand(int seed) ≡ void srand(int seed)

The function sets some initial state of the pseudo-random integer generator. It should be called once before starting the algorithm. The random values themselves should be obtained using the sequential call of the MathRand function.

By initializing a generator with the same seed value, you can get reproducible sequences of numbers. The seed value is not the first random number obtained from MathRand. The generator maintains some internal state, which at each moment of time (between calls to it for a new random number) is characterized by an integer value which is available from the program as the built-in uint variable [_RandomSeed](/en/book/common/environment/env_variables). It is this initial state value that establishes the MathSrand call.

Generator operation on every call to MathRand is described by two formulas:

```
Xn = Tf(Xp)
R = Gf(Xn)

```

The Tf function is called transition. It calculates the new internal state of the Xn generator based on the previous Xp state.

The Gf function generates another "random" value that the function MathRand will return, using a new internal state for this.

In MQL5, these formulas are implemented as follows (pseudocode):

```
Tf: _RandomSeed = _RandomSeed * 214013 + 2531011
Gf: MathRand = (_RandomSeed >> 16) & 0x7FFF

```

It is recommended to pass the [GetTickCount](/en/book/common/timing/timing_count) or [TimeLocal](/en/book/common/timing/timing_local_server) function as the seed value.

int MathRand() ≡ int rand()

The function returns a pseudo-random integer in the range from 0 to 32767. The sequence of generated numbers varies depending on the opening initialization done by calling MathSrand.

An example of working with the generator is given in the MathRand.mq5 file. It calculates statistics on the distribution of generated numbers over a given number of subranges (baskets). Ideally, we should get a uniform distribution.

```
#define LIMIT 1000 // number of attempts (generated numbers)
#define STATS 10   // number of baskets
   
int stats[STATS] = {}; // calculation of statistics of hits in baskets
   
void OnStart()
{
   const int bucket = 32767 / STATS;
   // generator reset
   MathSrand((int)TimeLocal());
   // repeat the experiment in a loop
   for(int i = 0; i < LIMIT; ++i)
   {
      // getting a new random number and updating statistics
      stats[MathRand() / bucket]++;
   }
   ArrayPrint(stats);
}

```

An example of results for three runs (each time we will get a new sequence):

```
 96  93 117  76  98  88 104 124 113  91
110  81 106  88 103  90 105 102 106 109
 89  98  98 107 114  90 101 106  93 104

```
