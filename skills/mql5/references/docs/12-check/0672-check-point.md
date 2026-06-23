# Point

Returns the point size of the current symbol in the quote currency.

```
double  Point();

```

Return Value

The value of the [_Point](/en/docs/predefined/_point) variable which stores the point size of the current symbol in the quote currency.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the current symbol point size in the quote currency
   double point = Point();
   
//--- send the obtained data to the journal
   Print("Point size of the current symbol in the quote currency: ", DoubleToString(point, _Digits));
   /*
   result:
   Point size of the current symbol in the quote currency: 0.00001
   */
  }

```
