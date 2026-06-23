# Reading the current Depth of Market data

After successful execution of the [MarketBookAdd](/en/book/automation/marketbook/marketbook_add_release) function, an MQL program can query the order book states using the MarketBookGet function upon the arrival of OnBookEvent events. The MarketBookGet function populates the MqlBookInfo array of structures passed by reference with the Depth of Market values of the specified symbol.

bool MarketBookGet(string symbol, MqlBookInfo &book[])

For the receiving array, you can pre-allocate memory for a sufficient number of records. If the dynamic array has zero or insufficient size, the terminal itself will allocate memory for it.

The function returns an indication of success (true) or error (false).

MarketBookGet is usually utilized directly in the [OnBookEvent](/en/book/automation/marketbook/marketbook_events) handler code or in functions called from it.

A separate record about the Depth of Market price level is stored in the MqlBookInfo structure.

```
struct MqlBookInfo 
{ 
   ENUM_BOOK_TYPE type;            // request type 
   double         price;           // price 
   long           volume;          // volume 
   double         volume_real;     // volume with increased accuracy 
};

```

The enumeration ENUM_BOOK_TYPE contains the following members.

| Identifier | Description |
| --- | --- |
| BOOK_TYPE_SELL | Request to sell |
| BOOK_TYPE_BUY | Request to buy |
| BOOK_TYPE_SELL_MARKET | Request to sell at market price |
| BOOK_TYPE_BUY_MARKET | Request to buy at market price |

In the order book, sell orders are located in its upper half and buy orders are placed in the lower half. As a rule, this leads to a sequence of elements from high prices to low prices. In other words, below the 0th index, there is the highest price, and the last entry is the lowest one, while between them prices decrease gradually. In this case, the minimum price step between the levels is [SYMBOL_TRADE_TICK_SIZE](/en/book/automation/symbols/symbols_point_tick), however, levels with zero volumes are not translated, that is, adjacent elements can be separated by a large amount.

In the terminal user interface, the order book window provides an option to enable/disable Advanced Mode, in which levels with zero volumes are also displayed. But by default, in the standard mode, such levels are hidden (skipped in the table).

In practice, the order book content can sometimes contradict the announced rules. In particular, some buy or sell requests may fall into the opposite half of the order book (probably, someone placed a buy at an unfavorably high price or a sell at an unfavorably low price, but the provider can also have data aggregation errors). As a result, due to the observance of the priority "all sell orders from above, all buy orders from below", the sequence of prices in the order book will be violated (see example below). In addition, repeated values of prices (levels) can be found both in one half of the order book and in the opposite ones.

In theory, the coincidence of buy and sell prices in the middle of the order book is correct. It means zero spread. However, unfortunately, duplicate levels also happen at a greater depth of the order book.

When we say "half" of the order book, it should not be taken literally. Depending on liquidity, the number of supply and demand levels may not match. In general, the book is not symmetrical.

The MQL program must check the correctness of the order book (in particular, the price sorting order) and be ready to handle potential deviations.

Less serious abnormal situations (which, nevertheless, should be taken into account in the algorithm) include:

- Consecutive identical order books, without changes
- Empty order book
- Order book with one level

Below is a fragment of a real Depth of Market received from a broker. The letters 'S' and 'B' mark, respectively, the prices of sell and buy requests.

Note that the buy and sell levels actually overlap: visually, this is not very noticeable, because all the 'S' records in the order book are specially placed up (the beginning of the receiving array), and the 'B' records are down (the end of the array). However, take a closer look: the buy prices in elements 20 and 21 are 143.23 and 138.86, respectively, and this is more than all sell offers. And, at the same time, the selling prices in elements 18 and 19 are 134.62 and 133.55, which is lower than all buy offers.

```
...
10 S 138.48 652
11 S 138.47 754
12 S 138.45 2256
13 S 138.43 300
14 S 138.42 14
15 S 138.40 1761
16 S 138.39 670    // Duplicate
17 S 138.11 200
18 S 134.62 420    // Low
19 S 133.55 10627  // Low
 
20 B 143.23 9564   // High
21 B 138.86 533    // High
22 B 138.39 739    // Duplicate
23 B 138.38 106
24 B 138.31 100
25 B 138.25 29
26 B 138.24 6072
27 B 138.23 571
28 B 138.21 17
29 B 138.20 201
30 B 138.19 1
...

```

In addition, the price of 138.39 is found both in the upper half at number 16 and in the lower half at number 22.

Errors in the order book are most likely to be present in extreme conditions: with strong volatility or lack of liquidity.

Let's check the receipt of the order book using the indicator MarketBookDisplay.mq5. It will subscribe to Depth of Market events for the specified symbol in the parameter WorkSymbol (if you leave an empty line there, the working symbol of the current chart is assumed).

```
input string WorkSymbol = ""; // WorkSymbol (if empty, use current chart symbol)
   
const string _WorkSymbol = StringLen(WorkSymbol) == 0 ? _Symbol : WorkSymbol;
int digits;
   
void OnInit()
{
   PRTF(MarketBookAdd(_WorkSymbol));
   digits = (int)SymbolInfoInteger(_WorkSymbol, SYMBOL_DIGITS);
   ...
}
   
void OnDeinit(const int)
{
   Comment("");
   PRTF(MarketBookRelease(_WorkSymbol));
}

```

The OnBookEvent handler is defined in the code for handling events, in which MarketBookGet is called, and all elements of the resulting MqlBookInfo array output as a multiline comment.

```
void OnBookEvent(const string &symbol)
{
   if(symbol == _WorkSymbol) // take only order books of the requested symbol
   {
      MqlBookInfo mbi[];
      if(MarketBookGet(symbol, mbi)) // getting the current order book
      {
         ...
         int half = ArraySize(mbi) / 2; // estimate of the middle of the order book
         bool correct = true;
         // collect information about levels and volumes in one line (with hyphens)
         string s = "";
         for(int i = 0; i < ArraySize(mbi); ++i)
         {
            s += StringFormat("%02d %s %s %d %g\n", i,
               (mbi[i].type == BOOK_TYPE_BUY ? "B" : 
               (mbi[i].type == BOOK_TYPE_SELL ? "S" : "?")),
               DoubleToString(mbi[i].price, digits),
               mbi[i].volume, mbi[i].volume_real);
               
            if(i > 0) // look for the middle of the order book as a change in request type
            {
               if(mbi[i - 1].type == BOOK_TYPE_SELL
                  && mbi[i].type == BOOK_TYPE_BUY)
               {
                  half = i; // this is the middle, because there has been a type change
               }
               
               if(mbi[i - 1].price <= mbi[i].price)
               {
                  correct = false; // reverse order = data problem
               }
            }
         }
         Comment(s + (!correct ? "\nINCORRECT BOOK" : ""));
         ...
      }
   }
}

```

Since the order book changes rather quickly, it is not very convenient to follow the comment. Therefore, we will add a couple of buffers to the indicator, in which we will display the contents of two halves of the order book as histograms: sell and buy separately. The zero bar will correspond to the central levels that form the spread. With an increase in bar numbers, there is an increase in the "depth of the market", that is, more and more distant price levels are displayed there: in the upper histogram, this means lower prices with buy orders, and in the lower one there are higher prices with sell orders.

```
#property indicator_separate_window
#property indicator_plots 2
#property indicator_buffers 2
   
#property indicator_type1   DRAW_HISTOGRAM
#property indicator_color1  clrDodgerBlue
#property indicator_width1  2
#property indicator_label1  "Buys"
   
#property indicator_type2   DRAW_HISTOGRAM
#property indicator_color2  clrOrangeRed
#property indicator_width2  2
#property indicator_label2  "Sells"
   
double buys[], sells[];

```

Let's provide an opportunity to visualize the order book in standard and extended modes (that is, skip or show levels with zero volumes), as well as display the volumes themselves in fractions of lots or units. Both options have analogs in the built-in Depth of Market window.

```
input bool AdvancedMode = false;
input bool ShowVolumeInLots = false;

```

Let's set buffers and obtaining of some symbol properties (which we will need later) in OnInit.

```
int depth, digits;
double tick, contract;
   
void OnInit()
{
   ...
   // setting indicator buffers
   SetIndexBuffer(0, buys);
   SetIndexBuffer(1, sells);
   ArraySetAsSeries(buys, true);
   ArraySetAsSeries(sells, true);
   // getting the necessary symbol properties
   depth = (int)PRTF(SymbolInfoInteger(_WorkSymbol, SYMBOL_TICKS_BOOKDEPTH));
   tick = SymbolInfoDouble(_WorkSymbol, SYMBOL_TRADE_TICK_SIZE);
   contract = SymbolInfoDouble(_WorkSymbol, SYMBOL_TRADE_CONTRACT_SIZE);
}

```

Let's add buffer filling to the handler OnBookEvent .

```
#define VOL(V) (ShowVolumeInLots ? V / contract : V)
   
void OnBookEvent(const string &symbol)
{
   if(symbol == _WorkSymbol) // take only order books of the requested symbol
   {
      MqlBookInfo mbi[];
      if(MarketBookGet(symbol, mbi)) // getting the current order book
      {
         // clear the buffers to the depth with 10 times the margin of the maximum depth,
         // because extended mode can have a lot of empty elements
         for(int i = 0; i <= depth * 10; ++i)
         {
            buys[i] = EMPTY_VALUE;
            sells[i] = EMPTY_VALUE;
         }
         ...// further along we form and display the comment as before
         if(!correct) return;
         
         // filling buffers with data
         if(AdvancedMode) // show skips enabled
         {
            for(int i = 0; i < ArraySize(mbi); ++i)
            {
               if(i < half)
               {
                  int x = (int)MathRound((mbi[i].price - mbi[half - 1].price) / tick);
                  sells[x] = -VOL(mbi[i].volume_real);
               }
               else
               {
                  int x = (int)MathRound((mbi[half].price - mbi[i].price) / tick);
                  buys[x] = VOL(mbi[i].volume_real);
               }
            }
         }
         else // standard mode: show only significant elements
         {
            for(int i = 0; i < ArraySize(mbi); ++i)
            {
               if(i < half)
               {
                  sells[half - i - 1] = -VOL(mbi[i].volume_real);
               }
               else
               {
                  buys[i - half] = VOL(mbi[i].volume_real);
               }
            }
         }
      }
   }
}

```

The following image demonstrates how the indicator works with settings AdvancedMode=true, ShowVolumeInLots=true.

![Buys are displayed as positive values (blue bar at the top), and sells are negative (red at the bottom). For clarity, there is a standard Depth of Market window on the right with the same settings (in advanced mode, volumes in lots), so you can make sure that the values match.](pics/market_book_display.png)

Buys are displayed as positive values (blue bar at the top), and sells are negative (red at the bottom). For clarity, there is a standard Depth of Market window on the right with the same settings (in advanced mode, volumes in lots), so you can make sure that the values match.

It should be noted that the indicator may not have time to redraw quickly enough to keep synchronization with the built-in order book. This does not mean that the MQL program did not receive the event in time, but only a side effect of asynchronous chart rendering. Working algorithms usually have analytical processing and order placing with the order book, rather than visualization.

In this case, updating the chart is implicitly requested at the time of calling the Comment function.
