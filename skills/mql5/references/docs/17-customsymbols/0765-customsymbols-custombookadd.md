# CustomBookAdd

Passes the status of the Depth of Market for a custom symbol. The function allows broadcasting the Depth of Market as if the prices arrive from a broker's server.

```
bool  CustomBookAdd(
   const string        symbol,            // symbol name
   const MqlBookInfo&  books[]            // array with descriptions of the Depth of Market elements
   uint                count=WHOLE_ARRAY  // number of elements to be used
   );

```

Parameters

symbol

[in]  Custom symbol name.

books[]

[in]   The array of [MqlBookInfo](/en/docs/constants/structures/mqlbookinfo) type data fully describing the Depth of Market status — all buy and sell requests. The passed Depth of Market status completely replaces the previous one.

count=WHOLE_ARRAY

[in]   The number of 'books' array elements to be passed to the function. The entire array is used by default.

Return Value

true – success, otherwise – false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The CustomBookAdd function works only for custom symbols the Depth of Market is opened for — via the platform interface or the [MarketBookAdd](/en/docs/marketinformation/marketbookadd) function.

When throwing the Depth of Market in, the symbol's Bid and Ask prices are not updated. You should control the change of the best prices and throw in the ticks using [CustomTicksAdd](/en/docs/customsymbols/customticksadd).

The function verifies the accuracy of transmitted data: the type, price and volume must be indicated for each element. Furthermore, MqlBookInfo.volume and MqlBookInfo.volume_real must not be zero or negative; if both volumes are negative, this will be considered an error.  You can specify any of the volumes or both of them: the one that is indicated or is positive will be used:

```
volume=-1 && volume_real=2 — volume_real=2 will be used,
a volume=3 && volume_real=0 — volume=3 will be used.

```

The MqlBookInfo.volume_real extended accuracy volume has a higher priority over the regular MqlBookInfo.volume. If both values are specified for the Depth of Market element, the volume_real one is used.

The order of the MqlBookInfo elements in the 'books' array does not matter. When saving the data, the terminal sorts them by price on its own.

When saving data, the "Book depth" ([SYMBOL_TICKS_BOOKDEPTH](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_integer)) parameter of the recipient custom symbol is checked. If the number of sell requests exceeds this value in the passed Depth of Market, the excess levels are discarded. The same is true for buy requests.

Sample filling of the 'books' array:

| Depth of Market status | Filling books[] |
| --- | --- |
|  | books[0].type= BOOK_TYPE_SELL ; 
 books[0].price=1.14337; 
 books[0].volume=100;    
 books[1].type= BOOK_TYPE_SELL ; 
 books[1].price=1.14330; 
 books[1].volume=50;    
 books[2].type= BOOK_TYPE_SELL ; 
 books[2].price=1.14335; 
 books[2].volume=40;    
 books[3].type= BOOK_TYPE_SELL ; 
 books[3].price=1.14333; 
 books[3].volume=10;    
 books[4].type= BOOK_TYPE_BUY ; 
 books[4].price=1.14322; 
 books[4].volume=10;    
 books[5].type= BOOK_TYPE_BUY ; 
 books[5].price=1.14320; 
 books[5].volume=90;   
 books[6].type= BOOK_TYPE_BUY ; 
 books[6].price=1.14319; 
 books[6].volume=100;    
 books[7].type= BOOK_TYPE_BUY ; 
 books[7].price=1.14318; 
 books[7].volume=10; |

Example:

```
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- enable the Depth of Market for a symbol we are to retrieve data from
   MarketBookAdd(Symbol());
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
  }
//+------------------------------------------------------------------+
//| Tick function                                                    |
//+------------------------------------------------------------------+
void OnTick(void)
  {
   MqlTick ticks[];
   ArrayResize(ticks,1);
//--- copy the current prices from the common symbol to the custom one
   if(SymbolInfoTick(Symbol(),ticks[0]))
     {
      string symbol_name=Symbol()+".SYN";
      CustomTicksAdd(symbol_name,ticks);
     }
  }
//+------------------------------------------------------------------+
//| Book function                                                    |
//+------------------------------------------------------------------+
void OnBookEvent(const string &book_symbol)
  {
//--- copy the current Depth of Market status from the common symbol to the custom one
   if(book_symbol==Symbol())
     {
      MqlBookInfo book_array[];
      if(MarketBookGet(Symbol(),book_array))
        {
         string symbol_name=Symbol()+".SYN";
         CustomBookAdd(symbol_name,book_array);
        }
     }
  }
//+------------------------------------------------------------------+

```

See also

[MarketBookAdd](/en/docs/marketinformation/marketbookadd), [CustomTicksAdd](/en/docs/customsymbols/customticksadd), [OnBookEvent](/en/docs/event_handlers/onbookevent)
