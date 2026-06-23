# Comment

This function outputs a comment defined by a user in the top left corner of a chart.

```
void  Comment(
   argument,     // first value
   ...           // next values
   );

```

Parameters

...

[in]   Any values, separated by commas. To delimit output information into several lines, a line break symbol "\n" or "\r\n" is used. Number of parameters cannot exceed 64. Total length of the input comment (including invisible symbols) cannot exceed 2045 characters (excess symbols will be cut out during output).

Return Value

No return value

Note

Arrays can't be passed to the Comment() function. Arrays must be entered element-by-element.

Data of double type are output with the accuracy of up to 16 digits after a decimal point, and can be output either in traditional or in scientific format, depending on what notation will be more compact. Data of float type are output with 5 digits after a decimal point. To output real numbers with another accuracy or in a predefined format, use the [DoubleToString()](/en/docs/convert/doubletostring) function.

Data of bool type are output as "true" or "false" strings. Dates are shown as YYYY.MM.DD HH:MI:SS. To show dates in another format, use the [TimeToString()](/en/docs/convert/timetostring) function. Data of color type are output either as R,G,B string or as a color name, if this color is present in the color set.

Comment() function does not work during optimization in the [Strategy Tester](/en/docs/runtime/testing#print).

Example:

```
void OnTick()
  {
//---
   double Ask,Bid;
   int Spread;
   Ask=SymbolInfoDouble(Symbol(),SYMBOL_ASK);
   Bid=SymbolInfoDouble(Symbol(),SYMBOL_BID);
   Spread=SymbolInfoInteger(Symbol(),SYMBOL_SPREAD);
//--- Output values in three lines
   Comment(StringFormat("Show prices\nAsk = %G\nBid = %G\nSpread = %d",Ask,Bid,Spread));
  }

```

See also

[ChartSetString](/en/docs/chart_operations/chartsetstring), [ChartGetString](/en/docs/chart_operations/chartgetstring)
