# Managing subscriptions to Depth of Market events

The terminal receives the Depth of Market information on a subscription basis: an MQL program must express its intent to receive Depth of Market (order book) events or, conversely, terminate its subscription by calling the appropriate functions, MarketBookAdd and MarketBookRelease.

The MarketBookAdd function subscribes to receive notifications about changes in the order book for the specified instrument. Thus, you can subscribe to order books for many instruments, and not just the working instrument of the current chart.

bool MarketBookAdd(const string symbol)

Usually, this function is called from OnInit or in the class constructor of a long-lived object. Notifications about the order book change are sent to the program in the form of [OnBookEvent](/en/book/automation/marketbook/marketbook_events) events, therefore, to process them, the program must have a handler function of the same name.

If the specified symbol was not selected in the Market Watch before calling the function, it will be added to the window automatically.

The MarketBookRelease function unsubscribes from notifications about changes in the specified order book.

bool MarketBookRelease(const string symbol)

As a rule, this function should be called from OnDeinit or from the class destructor of a long-lived object.

Both functions return a value true if successful and false otherwise.

For all applications running on the same chart, separate subscription counters are maintained by symbols. In other words, there can be several subscriptions to different symbols on the chart, and each of them has its own counter.

Subscription or unsubscription by a single call of any of the functions changes the subscription counter only for a specific symbol, on a specific chart where the program is running. This means that two charts can have subscriptions to OnBookEvent events of the same symbol, but with different values of subscription counters.

The initial value of the subscription counter is zero. On every call of MarketBookAdd, the subscription counter for the specified symbol on the given chart is incremented by 1 (the chart symbol and the symbol in MarketBookAdd do not have to match). When calling MarketBookRelease, the counter of subscriptions to the specified symbol within the chart decreases by 1.

OnBookEvent events for any symbol within the chart are generated as long as the subscription counter for this symbol is greater than zero. Therefore, it is important that every MQL program that contains MarketBookAdd calls, upon completion of its work, correctly unsubscribes from receiving events for each symbol using MarketBookRelease. For this, you should make sure that the number of MarketBookAdd calls and MarketBookRelease calls match. MQL5 does not allow you to find out the value of the counter.

The first example is a simple bufferless indicator MarketBookAddRelease.mq5, which enables a subscription to the order book at the time of launch and disables it when it is unloaded. In the WorkSymbol input parameter, you can specify a symbol to subscribe. If it is left empty (default value), the subscription will be initiated for the working symbol of the current chart.

```
input string WorkSymbol = ""; // WorkSymbol (empty means current chart symbol)
   
const string _WorkSymbol = StringLen(WorkSymbol) == 0 ? _Symbol : WorkSymbol;
string symbols[];
   
void OnInit()
{
   const int n = StringSplit(_WorkSymbol, ',', symbols);
   for(int i = 0; i < n; ++i)
   {
      if(!PRTF(MarketBookAdd(symbols[i])))
         PrintFormat("MarketBookAdd(%s) failed", symbols[i]);
   }
}
   
int OnCalculate(const int rates_total, const int prev_calculated, const int, const double &price[])
{
   return rates_total;
}
   
void OnDeinit(const int)
{
   for(int i = 0; i < ArraySize(symbols); ++i)
   {
      if(!PRTF(MarketBookRelease(symbols[i])))
         PrintFormat("MarketBookRelease(%s) failed", symbols[i]);
   }
}

```

As an additional feature, it is allowed to specify several instruments separated by commas. In this case, a subscription to all will be requested.

When the indicator is launched, a sign of subscription success or an error code is displayed in the log. The indicator then tries to unsubscribe from the events in the OnDeinit handler.

With the default settings, on the chart with the symbol for which the order book is available, we will get the following entries in the log.

```
MarketBookAdd(symbols[i])=true / ok
MarketBookRelease(symbols[i])=true / ok

```

If you put the indicator on a chart with a symbol without the order book, we will see error codes.

```
MarketBookAdd(symbols[i])=false / BOOKS_CANNOT_ADD(4901)
MarketBookAdd(XPDUSD) failed
MarketBookRelease(symbols[i])=false / BOOKS_CANNOT_DELETE(4902)
MarketBookRelease(XPDUSD) failed

```

You can experiment by specifying in the input parameter WorkSymbol existing or missing characters. We will consider the case of subscribing to order books of several symbols in the next section.
