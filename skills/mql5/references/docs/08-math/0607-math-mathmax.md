# MathMax

The function returns the maximal value of two values.

```
double  MathMax(
   double  value1,     // first value
   double  value2      // second value
   );

```

Parameters

value1

[in]  First numeric value.

value2

[in]  Second numeric value.

Return Value

The largest of the two values.

Note

Instead of MathMax() you can use fmax(). Functions fmax(), [fmin()](/en/docs/math/mathmin), MathMax(), [MathMin()](/en/docs/math/mathmin) can work with integer types without typecasting them to the type of double.

If parameters of different types are passed into a function, the parameter of the smaller type is automatically [cast](/en/docs/basis/types/casting) to the larger type. The type of the return value corresponds to the larger type.

If data of the same type are passed, no casting is performed.

Example:

```
//--- input parameters
input int                  InpPeriod = 10;            // Moving average calculation period
input ENUM_MA_METHOD       InpMethod = MODE_SMA;      // Moving average calculation method
input ENUM_APPLIED_PRICE   InpPrice  = PRICE_CLOSE;   // Moving average calculation price
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- if the moving average period is set to a value less than 1, then the default value (10) is used
   int period=(InpPeriod<1 ? 10 : InpPeriod);
//--- create the Moving Average indicator handle
   int handle=iMA(Symbol(),Period(),period,0,InpMethod,InpPrice);
   if(handle==INVALID_HANDLE)
     {
      Print("Failed to create the Moving Average indicator handle. Error ",GetLastError());
      return;
     }
//--- get the current Bid price
   double bid=0;
   ResetLastError();
   if(!SymbolInfoDouble(Symbol(),SYMBOL_BID,bid))
     {
      Print("Failed to get Bid price. Error ",GetLastError());
      return;
     }
//--- get the moving average value on the current bar
   double array[1];
   int    copied=CopyBuffer(handle,0,0,1,array);
   if(copied!=1)
     {
      Print("Failed to get Moving Average data. Error ",GetLastError());
      return;
     }
//--- get the highest price of the two (Bid price and Moving Average value) and display the resulting data in the journal
   double max_price=MathMax(bid,array[0]);
   PrintFormat("Bid: %.*f, Moving Average: %.*f, highest price of the two: %.*f",_Digits,bid,_Digits,array[0],_Digits,max_price);
   PrintFormat("Bid price %s moving average",(bid>array[0] ? "higher" : bid<array[0] ? "lower" : "equal to"));
  }

```
