# _RandomSeed

Variable for storing the current state when generating pseudo-random integers. _RandomSeed changes its value when calling [MathRand()](/en/docs/math/mathrand). Use [MathSrand()](/en/docs/math/mathsrand) to set the required initial condition.

x random number received by MathRand() function is calculated in the following way at each call:

```
x=_RandomSeed*214013+2531011;
_RandomSeed=x;
x=(x>>16)&0x7FFF;

```

See also

[MathRand()](/en/docs/math/mathrand), [MathSrand()](/en/docs/math/mathsrand), [Integer types](/en/docs/basis/types/integer)
