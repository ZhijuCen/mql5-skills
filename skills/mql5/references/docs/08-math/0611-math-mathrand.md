# MathRand

Returns a pseudorandom integer within the range of 0 to 32767.

```
int  MathRand();

```

Return Value

Integer value within the range of 0 to 32767.

Note

Before the first call of the function, it's necessary to call [MathSrand](/en/docs/math/mathsrand) to set the generator of pseudorandom numbers to the initial state.

Note

Instead of MathRand() you can use rand().

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set a new initial state to generate a series of pseudo-random integers at each launch
   MathSrand(GetTickCount());
//--- in a loop, display 10 generated pseudo-random integers in the journal
   for(int i=0; i<10; i++)
     {
      int rand_value=MathRand();
      PrintFormat("Pseudorandom integer №%d: %u",i+1,rand_value);
     }
  }

```
