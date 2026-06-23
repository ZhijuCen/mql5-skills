# Generating ticks in tester

The presence of the OnTick handler in the Expert Advisor is not mandatory for it to be tested in the tester. The Expert Advisor can use one or more of the other familiar functions:

- OnTick — event handler for the arrival of a new tick
- OnTrade — trade event handler
- OnTradeTransaction — trade transaction handler
- OnTimer — timer signal handler
- OnChartEvent — event handler on the chart, including custom charts

At the same time, inside the tester, the main equivalent of the time course is a thread of ticks, which contain not only price changes but also time accurate to milliseconds. Therefore, to test Expert Advisors, it is necessary to generate tick sequences. The MetaTrader 5 tester has 4 tick generation modes:

- Real ticks (if their history is provided by the broker)
- Every tick (emulation based on available M1 timeframe quotes)
- OHLC prices from minute bars (1 Minute OHLC)
- Open prices only (1 tick per bar)

Another mode of operation — mathematical calculations — we will analyze later since it is not related to quotes and ticks.

Whichever of the 4 modes the user chooses, the terminal loads the available historical data for testing. If the mode of real ticks was selected, and the broker does not have them for this instrument, then the "All ticks" mode is used. The tester indicates the nature of tick generation in its report graphically and as a percentage (where 100% means all ticks are real).

The history of the instrument selected in the tester settings is synchronized and downloaded by the terminal from the trading server before starting the testing process. At the same time, for the first time, the terminal downloads the history from the trading server to the required depth (with a certain margin, depending on the timeframe, at least 1 year before the start of the test), so as not to apply for it later. In the future, only the download of new data will occur. All this is accompanied by corresponding messages in the tester's log.

The testing agent receives the history of the tested instrument from the client terminal immediately after testing is started. If the testing process uses data on other instruments (for example, this is a multicurrency Expert Advisor), then in this case the testing agent requests the required history from the client terminal at the first call. If historical data is available on the terminal, they are immediately transferred to testing agents. If the data is missing, the terminal will request and download it from the server, and then transfer it to the testing agents.

Additional instruments are also used when the cross-rate price is calculated during trading operations. For example, when testing a strategy on EURCHF with a deposit currency in US dollars, before processing the first trading operation, the testing agent will request the history of EURUSD and USDCHF from the client terminal, although the strategy does not directly refer to these instruments.

In this regard, before testing a multicurrency strategy, it is recommended that you first download all the necessary historical data into the client terminal. This will assist in avoiding testing/optimization delays associated with resuming data. You can download the history, for example, by opening the corresponding charts and scrolling them to the beginning of the history.

Now let's look at tick generation modes in more detail.

Real ticks from history

Testing and optimization on real ticks are as close to real conditions as possible. These are ticks from exchanges and liquidity providers.

If there is a minute bar in the symbol's history, but no tick data for that minute, the tester will generate ticks in the "Every tick" mode (see further). This allows you to build the correct chart in the tester in case of incomplete tick data from the broker. Moreover, tick data may not match minute bars for various reasons. For example, due to disconnections or other failures in the transmission of data from the source to the client terminal. When testing, minute data is considered more reliable.

Ticks are stored in the symbol cache in the strategy tester. The cache size is no more than 128,000 ticks. When new ticks arrive, the oldest data is pushed out of it. However, using the CopyTicks function, you can get ticks outside the cache (only when testing using real ticks). In this case, the data will be requested from the tester's tick database, which fully corresponds to the similar database of the client terminal. No adjustments by minute bars are made to this base. Therefore, the ticks in it may differ from the ticks in the cache.

Every tick (emulation)

If the real tick history is not available or if you need to minimize network traffic (because the archive of real ticks can consume significant resources), you can choose to artificially generate ticks based on the available quotes of the M1 timeframe.

The history of quotes for financial instruments is transmitted from the trading server to the MetaTrader 5 client terminal in the form of tightly packed blocks of minute bars. The history query procedure and the constructions of the required timeframes were considered in detail in the section [Technical features of organization and storage of timeseries](/en/book/applications/timeseries/timeseries_storage_tech).

The minimum element of the price history is a minute bar, from which you can get information about four OHLC price values: Open, High, Low, and Close.

A new minute bar opens not at the moment when a new minute begins (the number of seconds becomes 0) but when a tick — a price change of at least one point — occurs. Similarly, we cannot determine from the bar with accuracy of a second when the tick corresponding to the closing price of this minute bar arrived: we only know the last price of the one-minute bar, which was recorded as the Close price.

Thus, for each minute bar, we know 4 control points, which we can say for sure that the price has been there. If the bar has only 4 ticks, then this information is enough for testing, but usually, the tick volume is more than 4. This means that it is necessary to generate additional checkpoints for ticks that came between prices Open, High, Low, and Close. The basics of generating ticks in the "Every tick" mode are described in the [documentation](https://www.metatrader5.com/en/terminal/help/algotrading/tick_generation).

When testing in the "Every tick" mode, the OnTick function of the Expert Advisor will be called on every generated tick. The Expert Advisor will receive time and Ask/Bid/Last prices the same way as when working online.

The "Every tick" testing mode is the most accurate (after the real ticks mode), but also the most time-consuming. For the primary evaluation of most trading strategies, it is usually sufficient to use one of two simplified testing modes: at OHLC M1 prices or at the opening of bars of the selected timeframe.

1 minute OHLC

In the "1 minute OHLC" mode, the tick sequence is built only by OHLC prices of minute bars, the number of the OnTick function calls is significantly reduced; hence, the testing time is also reduced. This is a very efficient, useful mode that offers a compromise between testing accuracy and speed. However, you need to be careful with it when it comes to someone else's Expert Advisor.

Refusal to generate additional intermediate ticks between prices Open, High, Low, and Close leads to the appearance of rigid determinism in the development of prices from the moment the Open price is defined. This makes it possible to create a "Testing Grail" that shows a nice upward trending balance chart when testing.

For a minute bar, 4 prices are known, of which the first one is Open, and the last one is Close. Prices registered between them are High and Low, and information about the order of their occurrence is lost, but we know that the High price is greater than or equal to Open, and Low is less than or equal to Open.   

   

After receiving the Open price, we need to analyze only the next tick to determine whether it is High or Low. If the price is below Open, this is Low — buy on this tick, as the next tick will correspond to the High price, on which we close the buy trade and open a sell one. The next tick is the last on the bar, Close, on which we close sell.   

   

If a tick with a price higher than the opening price comes after our price, then the sequence of transactions is reversed. Seemingly, one could trade on every bar in this mode. When testing such an Expert Advisor on history, everything goes perfectly, but online it will fail.

A similar effect can happen unintentionally, due to a combination of features of the calculation algorithm (for example, statistics calculation) and tick generation.

Thus, it is always important to test it in the "Every tick" mode or, better, based on real ticks after finding the optimal Expert Advisor settings on rough testing modes ("1 minute OHLC" and "Only Open Prices").

Open prices only

In this mode, ticks are generated using the OHLC prices of the timeframe selected for testing. In this case, the OnTick function runs only once, at the beginning of each bar. Because of this feature, stop levels and pending orders may be triggered at a price different from the requested one (especially when testing on higher timeframes). In exchange for this, we get the opportunity to quickly conduct evaluation testing of the Expert Advisor.

For example, the Expert Advisor is tested on EURUSD H1 in the "Open price only" mode. In this case, the total number of ticks (control points) will be 4 times more than the number of hourly bars that fall within the tested interval. But in this case, the OnTick handler will only be called at the opening of hourly bars. For the rest ticks ("hidden" from the Expert Advisor), the following checks required for correct testing are performed:

- calculation of margin requirements
- triggering of Stop Loss and Take Profit
- triggering pending orders
- deleting pending orders upon expiration

If there are no open positions or pending orders, then there is no need for these checks on hidden ticks, and the speed increase can be significant.

An exception when generating ticks in the "Open prices only" mode are the W1 and MN1 periods: for these timeframes, ticks are generated for the OHLC prices of each day, not weekly or monthly, respectively.

This "Open prices only" mode is well suited for testing strategies that perform trades only at the opening of the bar and do not use pending orders, and do not use Stop Loss and Take Profit levels. For the class of such strategies, all the necessary testing accuracy is preserved.

The MQL5 API does not allow the program to find out in which mode it is running in the tester. At the same time, this may be important for Expert Advisors or the indicators they use, which are not designed, for example, to work correctly at opening prices or OHLC. In this regard, we implement a simple mode detection mechanism. The source code is attached in the file TickModel.mqh.

Let's declare our enumeration with the existing modes.

```
enum TICK_MODEL
{
   TICK_MODEL_UNKNOWN = -1,    /*Unknown (any)*/    // unknown/not yet defined
   TICK_MODEL_REAL = 0,        /*Real ticks*/       // best quality
   TICK_MODEL_GENERATED = 1,   /*Generated ticks*/  // good quality
   TICK_MODEL_OHLC_M1 = 2,     /*OHLC M1*/          // acceptable quality and fast
   TICK_MODEL_OPEN_PRICES = 3, /*Open prices*/      // worse quality, but very fast
   TICK_MODEL_MATH_CALC = 4,   /*Math calculations*/// no ticks (not defined)
};

```

Except the first element, which is reserved for the case when the mode has not yet been determined or cannot be determined for some reason, all other elements are arranged in descending order of simulation quality, starting from real and ending with opening prices (for them, the developer must check the compatibility strategy with the fact that its trading is carried out only at the opening of a new bar). The last mode TICK_MODEL_MATH_CALC operates without ticks altogether; we will consider it [separately](/en/book/automation/tester/tester_math_calc).

The mode detection principle is based on the check of the availability of ticks and their times on the first two ticks when starting the test. The check itself is wrapped in the getTickModel function, which the Expert Advisor should call from the OnTick handler. Since the check is done once, the static variable model is described inside the function initially set to TICK_MODEL_UNKNOWN. It will store and switch the current state of the check, which will be required to distinguish between OHLC modes and opening prices.

```
TICK_MODEL getTickModel()
{
   static TICK_MODEL model = TICK_MODEL_UNKNOWN;
   ...

```

On the first analyzed tick, the model is equal to TICK_MODEL_UNKNOWN, and an attempt is made to get real ticks by calling CopyTicks.

```
   if(model == TICK_MODEL_UNKNOWN)
   {
      MqlTick ticks[];
      const int n = CopyTicks(_Symbol, ticks, COPY_TICKS_ALL, 0, 10);
      if(n == -1)
      {
         switch(_LastError)
         {
         case ERR_NOT_ENOUGH_MEMORY:    // emulate ticks
            model = TICK_MODEL_GENERATED;
            break;
            
         case ERR_FUNCTION_NOT_ALLOWED: // prices of opening and OHLC
            if(TimeCurrent() != iTime(_Symbol, _Period, 0))
            {
               model = TICK_MODEL_OHLC_M1;
            }
            else if(model == TICK_MODEL_UNKNOWN)
            {
               model = TICK_MODEL_OPEN_PRICES;
            }
            break;
         }
         
         Print(E2S(_LastError));
      }
      else
      {
         model = TICK_MODEL_REAL;
      }
   }
   ...

```

If it succeeds, the detection immediately ends with setting the model to TICK_MODEL_REAL. If real ticks are not available, the system will return a certain error code, according to which we can draw the following conclusions. The error code ERR_NOT_ENOUGH_MEMORY corresponds to the tick emulation mode. Why the code is this way is not entirely clear, but this is a characteristic feature, and we use it here. In the other two tick generation modes, we will get the ERR_FUNCTION_NOT_ALLOWED error.

You can distinguish one mode from the other by the tick time. If it turns out to be a non-multiple of the timeframe for a tick, then we are talking about the OHLC mode. However, the problem here is that the first tick in both modes can be aligned with the bar opening time. Thus, we will get the value TICK_MODEL_OPEN_PRICES, but it needs to be specified. Therefore, for the final conclusion, one more tick should be analyzed (call the function on it again if TICK_MODEL_OPEN_PRICES was received earlier). For this case, the following if branch is provided inside the function.

```
   else if(model == TICK_MODEL_OPEN_PRICES)
   {
      if(TimeCurrent() != iTime(_Symbol, _Period, 0))
      {
         model = TICK_MODEL_OHLC_M1;
      }
   }
   return model;
}

```

Let's check the operation of the detector in a simple Expert Advisor TickModel.mq5. In the TickCount input parameter, we specify the maximum number of analyzed ticks, that is, how many times the getTickModel function will be called. We know that two is enough, but in order to make sure that the model does not change afterward, 5 ticks are suggested by default. We also provide the RequireTickModel parameter which instructs the Expert Advisor to terminate operation if the simulation level is lower than the requested one. By default, its value is TICK_MODEL_UNKNOWN, which means no mode restriction.

```
input int TickCount = 5;
input TICK_MODEL RequireTickModel = TICK_MODEL_UNKNOWN;

```

In the OnTick handler, we run our code only if it works in the tester.

```
void OnTick()
{
   if(MQLInfoInteger(MQL_TESTER))
   {
      static int count = 0;
      if(count++ < TickCount)
      {
         // output tick information for reference
         static MqlTick tick[1];
         SymbolInfoTick(_Symbol, tick[0]);
         ArrayPrint(tick);
         // define and display the model (preliminarily)
         const TICK_MODEL model = getTickModel();
         PrintFormat("%d %s", count, EnumToString(model));
         // if the tick counter is 2+, the conclusion is final and we act based on it
         if(count >= 2)
         {
            if(RequireTickModel != TICK_MODEL_UNKNOWN
            && RequireTickModel < model) // quality less than requested
            {
               PrintFormat("Tick model is incorrect (%s %sis required), terminating",
                  EnumToString(RequireTickModel),
                  (RequireTickModel != TICK_MODEL_REAL ? "or better " : ""));
               ExpertRemove(); // end operation
            }
         }
      }
   }
}

```

Let's try to run the Expert Advisor in the tester with different tick generation modes by choosing a common combination of EURUSD H1.

The RequireTickModel parameter in the Expert Advisor is set to OHLC M1. If the tester mode is "Every tick", we will receive a corresponding message in the log, and the Expert Advisor will continue working.

```
                 [time]   [bid]   [ask]  [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.04.01 00:00:30 1.10656 1.10679 1.10656        0 1648771230000      14       0.00000
NOT_ENOUGH_MEMORY
1 TICK_MODEL_GENERATED
                 [time]   [bid]   [ask]  [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.04.01 00:01:00 1.10656 1.10680 1.10656        0 1648771260000      12       0.00000
2 TICK_MODEL_GENERATED
                 [time]   [bid]   [ask]  [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.04.01 00:01:30 1.10608 1.10632 1.10608        0 1648771290000      14       0.00000
3 TICK_MODEL_GENERATED

```

The OHLC M1 and real ticks modes are also suitable, and in the latter case, there will be no error code.

```
                 [time]   [bid]   [ask] [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.04.01 00:00:00 1.10656 1.10687 0.0000        0 1648771200122     134       0.00000
1 TICK_MODEL_REAL
                 [time]   [bid]   [ask] [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.04.01 00:00:00 1.10656 1.10694 0.0000        0 1648771200417       4       0.00000
2 TICK_MODEL_REAL
                 [time]   [bid]   [ask] [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.04.01 00:00:00 1.10656 1.10691 0.0000        0 1648771200816       4       0.00000
3 TICK_MODEL_REAL

```

However, if you change the mode in the tester to "Open prices only", the Expert Advisor will stop after the second tick.

```
                 [time]   [bid]   [ask]  [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.04.01 00:00:00 1.10656 1.10679 1.10656        0 1648771200000      14       0.00000
FUNCTION_NOT_ALLOWED
1 TICK_MODEL_OPEN_PRICES
                 [time]   [bid]   [ask]  [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.04.01 01:00:00 1.10660 1.10679 1.10660        0 1648774800000      14       0.00000
2 TICK_MODEL_OPEN_PRICES
Tick model is incorrect (TICK_MODEL_OHLC_M1 or better is required), terminating
ExpertRemove() function called

```

This method requires running a test and waiting for a couple of ticks in order to determine the mode. In other words, we cannot stop the test early by returning an error from OnInit. Even more, when starting an optimization with the wrong type of tick generation, we will not be able to stop the optimization, which can only be done from the [OnTesterInit](/en/book/automation/tester/tester_ontester_init_pass_deinit) function. Thus, the tester will try to complete all passes during the optimization, although they will be stopped at the very beginning. This is the current platform limitation.
