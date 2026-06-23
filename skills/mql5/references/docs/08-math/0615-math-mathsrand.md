# MathSrand

Sets the starting point for generating a series of pseudorandom integers.

```
void  MathSrand(
   int  seed      // initializing number
   );

```

Parameters

seed

[in]  Starting number for the sequence of random numbers.

Return Value

No return value.

Note

The [MathRand()](/en/docs/math/mathrand) function is used for generating a sequence of pseudorandom numbers. Call of MathSrand() with a certain initializing number allows to always produces the same sequence of pseudorandom numbers.

To ensure receipt of non-recurring sequence, use the call of MathSrand(GetTickCount()), since the value of [GetTickCount()](/en/docs/common/gettickcount) increases from the moment of the start of the operating system and is not repeated within 49 days, until the built-in counter of milliseconds overflows. Use of MathSrand(TimeCurrent()) is not suitable, because the [TimeCurrent()](/en/docs/dateandtime/timecurrent) function returns the time of the last tick, which can be unchanged for a long time, for example at the weekend.

Initialization of the random number generator using MathSrand() for indicators and Expert Advisors is better performed in the OnInit() handler; it saves you from the following multiple restarts of the generator in OnTick() and OnCalculate().

Instead of the MathSrand() function you can use the srand() function.

Example:

```
#property description "The indicator shows the central limit theorem, which states:"
#property description "The sum of a sufficiently large number of weakly dependent random variables, "
#property description "having approximately equal magnitude (none of the summands dominates,"
#property description "or makes a determining contribution to the sum), has a distribution close to normal."
 
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//--- Properties of the graphical construction
#property indicator_label1  "Label"
#property indicator_type1   DRAW_HISTOGRAM
#property indicator_color1  clrRoyalBlue
#property indicator_style1  STYLE_SOLID
#property indicator_width1  5
//--- An input variable
input int      sample_number=10;
//--- An indicator buffer to for drawing the distribution
double         LabelBuffer[];
//--- A counter of ticks
double         ticks_counter;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
void OnInit()
  {
//--- Binding an array and an indicator buffer
   SetIndexBuffer(0,LabelBuffer,INDICATOR_DATA);
//--- turn the indicator buffer around from the present to the past
   ArraySetAsSeries(LabelBuffer,true);
//--- Initialize the generator of random numbers
   MathSrand(GetTickCount());
//--- Initialize the counter of ticks
   ticks_counter=0;
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
  {
//--- For a zero counter reset the indicator buffer
   if(ticks_counter==0) ArrayInitialize(LabelBuffer,0);
//--- Increase the counter
   ticks_counter++;
//--- We should periodically reset the counter ticks, to revive the distribution
   if(ticks_counter>100)
     {
      Print("We've reset the indicator values, let's start filling the cells once again");
      ticks_counter=0;
     }
//--- Get a sample of random values as the sum of three numbers from 0 to 7
   for(int i=0;i<sample_number;i++)
     {
      //--- Calculation of the index of the cell, where the random number falls as the sum of three other numbers
      int rand_index=0;
      //--- Get three random numbers from 0 to 7
      for(int k=0;k<3;k++)
        {
         //--- A remainder in the division by 7 will return a value from 0 to 6
         rand_index+=MathRand()%7;
        }
      //--- Increase the value in the cell number rand_index by 1
      LabelBuffer[rand_index]++;
     }
//--- Exit the OnCalculate() handler
   return(rates_total);
  }

```
