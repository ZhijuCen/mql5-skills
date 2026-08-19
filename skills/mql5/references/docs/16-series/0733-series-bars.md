# Bars

Returns the number of bars count in the history for a specified symbol and period. There are 2 variants of functions calls.

Request all of the history bars

```
int  Bars(
   string           symbol_name,     // symbol name
   ENUM_TIMEFRAMES  timeframe        // period
   );

```

Request the history bars for the selected time interval

```
int  Bars(
   string           symbol_name,     // symbol name
   ENUM_TIMEFRAMES  timeframe,       // period
   datetime         start_time,      // start date and time
   datetime         stop_time        // end date and time
   );

```

Parameters

symbol_name

[in]  Symbol name.

timeframe

[in]  Period.

start_time

[in]  Bar time corresponding to the first element.

stop_time

[in]  Bar time corresponding to the last element.

Return Value

If the start_time and stop_time parameters are defined, the function returns the number of bars in the specified time interval, otherwise it returns the total number of bars.

Note

If data for the timeseries with specified parameters are not formed in the terminal by the time of the Bars() function call, or data of the timeseries are not [synchronized](/en/docs/series/timeseries_access#synchronized) with a trade server by the moment of the function call, the function returns a zero value.

When requesting the number of bars in a specified time interval, only bars with an open time falling within the interval are considered. For example, if the current day of the week is Saturday and the request is made for the number of W1 bars with start_time=last_tuesday and stop_time=last_friday, the function will return 0 since the open time of a W1 timeframe is always Sunday and not a single W1 bar falls within the specified interval.

Sample request for the number of all history bars:

```
   int bars=Bars(_Symbol,_Period);
   if(bars>0)
     {
      Print("Number of bars in the terminal history for the symbol-period at the moment = ",bars);
     }
   else  //no available bars
     {
      //--- data on the symbol might be not synchronized with data on the server
      bool synchronized=false;
      //--- loop counter
      int attempts=0;
      // make 5 attempts to wait for synchronization
      while(attempts<5)
        {
         if(SeriesInfoInteger(Symbol(),0,SERIES_SYNCHRONIZED))
           {
            //--- synchronization done, exit
            synchronized=true;
            break;
           }
         //--- increase the counter
         attempts++;
         //--- wait 10 milliseconds till the next iteration
         Sleep(10);
        }
      //--- exit the loop after synchronization
      if(synchronized)
        {
         Print("Number of bars in the terminal history for the symbol-period at the moment = ",bars);
         Print("The first date in the terminal history for the symbol-period at the moment = ",
               (datetime)SeriesInfoInteger(Symbol(),0,SERIES_FIRSTDATE));
         Print("The first date in the history for the symbol on the server = ",
               (datetime)SeriesInfoInteger(Symbol(),0,SERIES_SERVER_FIRSTDATE));
        }
      //--- synchronization of data didn't happen
      else
        {
         Print("Failed to get number of bars for ",_Symbol);
        }
     }

```

Sample request for the number of bars in the specified interval:

```
   int n;
   datetime date1 = D'2016.09.02 23:55'; // Friday
   datetime date2 = D'2016.09.05 00:00'; // Monday
   datetime date3 = D'2016.09.08 00:00'; // Thursday
   //---
   n=Bars(_Symbol,PERIOD_H1,D'2016.09.02 02:05',D'2016.09.02 10:55');
   Print("Number of bars: ",n); // Output: "Number of bars: 8", H2 bar is considered in the calculation, while H11 one is not
   n=Bars(_Symbol,PERIOD_D1,date1,date2);
   Print("Number of bars: ",n); // Output: "Number of bars: 1", since an open time of a single D1 (Monday) bar falls within the interval
   n=Bars(_Symbol,PERIOD_W1,date2,date3);
   Print("Number of bars: ",n); // Output: "Number of bars: 0", since not a single W1 bar open time falls within the specified interval

```

See also

[Event Handling Functions](/en/docs/event_handlers/oncalculate)
