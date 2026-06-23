# MarketBookRelease

Provides closing of Depth of Market for a selected symbol, and cancels the subscription for receiving notifications of the DOM changes.

```
bool  MarketBookRelease(
   string  symbol      // symbol
   );

```

Parameters

symbol

[in] Symbol name.

Return Value

The true value if closed successfully, otherwise false.

Note

Normally, this function must be called from the [OnDeinit()](/en/docs/event_handlers/ondeinit) function, if the corresponding [MarketBookAdd()](/en/docs/marketinformation/marketbookadd) function has been called in the [OnInit()](/en/docs/event_handlers/oninit) function. Or it must be called from the class destructor, if the corresponding MarketBookAdd() function has been called from the class constructor.

Example:

```
#define SYMBOL_NAME "GBPUSD"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- open the market depth for SYMBOL_NAME symbol
   if(!MarketBookAdd(SYMBOL_NAME))
     {
      PrintFormat("MarketBookAdd(%s) failed. Error ", SYMBOL_NAME, GetLastError());
      return;
     }
 
//--- send the message about successfully opening the market depth to the journal
   PrintFormat("The MarketBook for the '%s' symbol was successfully opened and a subscription to change it was received", SYMBOL_NAME);
   
//--- wait 2 seconds
   Sleep(2000);
   
//--- upon completion, unsubscribe from the open market depth
//--- send the message about successfully unsubscribing from the market depth or about the error to the journal
   ResetLastError();
   if(MarketBookRelease(SYMBOL_NAME))
      PrintFormat("MarketBook for the '%s' symbol was successfully closed", SYMBOL_NAME);
   else
      PrintFormat("Error %d occurred when closing MarketBook using the '%s' symbol", GetLastError(), SYMBOL_NAME);
      
   /*
   result:
   The MarketBook for the 'GBPUSD' symbol was successfully opened and a subscription to change it was received
   MarketBook for the 'GBPUSD' symbol was successfully closed
   */
  }

```

See also

[Structure of Depth of Market](/en/docs/constants/structures/mqlbookinfo),  [Structures and Classes](/en/docs/basis/types/classes)
