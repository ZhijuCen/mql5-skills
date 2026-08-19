# Digits

Returns the number of decimal digits determining the accuracy of price of the current chart symbol.

```
int  Digits();

```

Return Value

The value of the [_Digits](/en/docs/predefined/_digits) variable which stores the number of decimal digits determining the accuracy of price of the current chart symbol.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the number of decimal places for the current chart symbol
   int digits = Digits();
   
//--- send the obtained data to the journal
   Print("Number of decimal digits for the current chart symbol: ", digits);
   /*
   result:
   Number of decimal digits for the current chart symbol: 5
   */
  }

```
