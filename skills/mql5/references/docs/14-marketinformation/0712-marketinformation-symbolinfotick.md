# SymbolInfoTick

The function returns current prices of a specified symbol in a variable of the MqlTick type.

```
bool  SymbolInfoTick(
   string    symbol,     // symbol name
   MqlTick&  tick        // reference to a structure
   );

```

Parameters

symbol

[in]  Symbol name.

tick

[out]  Link to the structure of the [MqlTick](/en/docs/constants/structures/mqltick) type, to which the current prices and time of the last price update will be placed.

Return Value

The function returns true if successful, otherwise returns false.

Example:

```
#define SYMBOL_NAME "EURUSD"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare an array with the MqlTick structure type of dimension 1
   MqlTick tick[1]={};
   
//--- get the latest prices for the SYMBOL_NAME symbol into the MqlTick structure
   if(!SymbolInfoTick(SYMBOL_NAME, tick[0]))
     {
      Print("SymbolInfoTick() failed. Error ", GetLastError());
      return;
     }
 
//--- send the obtained data to the journal
   PrintFormat("Latest price data for the '%s' symbol:", SYMBOL_NAME);
   ArrayPrint(tick);
   /*
   result:
   Latest price data for the 'EURUSD' symbol:
                    [time]   [bid]   [ask] [last] [volume]    [time_msc] [flags] [volume_real]
   [0] 2024.05.17 23:58:54 1.08685 1.08695 0.0000        0 1715990334319       6       0.00000
   */
  }

```
