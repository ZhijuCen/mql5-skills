# Alert

Displays a message in a separate window.

```
void  Alert(
   argument,     // first value
   ...           // other values
   );

```

Parameters

argument

[in]  Any values separated by commas. To split the information output in several lines you can use the line feed character "\n" or "\r\n". The number of parameters can not exceed 64.

Return Value

No return value.

Note

Arrays can't be passed to the Alert() function. Arrays should be output elementwise. Data of the double type are output with 8 digits after the decimal point, data of the float type are displayed with 5 digits after the decimal point. To output the real numbers with a different precision or in a scientific format, use the [DoubleToString()](/en/docs/convert/doubletostring) function.

Data of the bool type is output as "true" or "false" strings. Dates are output as YYYY.MM.DD HH:MI:SS. To display a date in another format use the [TimeToString()](/en/docs/convert/timetostring) function. Data of the color type are output either as an R,G,B string or as a color name, if the color is present in a color set.

Alert() function does not work in the [Strategy Tester](/en/docs/runtime/testing#alert_etc).

Example:

```
//--- enums
enum ENUM_INTERSECT_DIRECTION
  {
   INTERSECT_DIRECTION_NONE= 0,  // no crossing
   INTERSECT_DIRECTION_UP  = 1,  // upward crossing
   INTERSECT_DIRECTION_DOWN=-1,  // downward crossing
  };
 
//--- input parameters
input    uint               InpPeriod = 10;            // MA Period
input    int                InpShift  = 0;             // MA Shift
input    ENUM_MA_METHOD     InpMethod = MODE_SMA;      // MA Method
input    ENUM_APPLIED_PRICE InpPrice  = PRICE_CLOSE;   // MA Applied price
 
//--- global variables
int      ExtMaHandle;
int      ExtMaPeriod;
double   ExtData[2];
MqlRates ExtRates[2];
 
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- the period for calculating the moving average will be equal to the default value (10) if zero is specified in the input parameter
   ExtMaPeriod=int(InpPeriod<1 ? 10 : InpPeriod);
//--- create a handle for the Moving Average indicator with the specified parameters
   ExtMaHandle=iMA(Symbol(),PERIOD_CURRENT,ExtMaPeriod,InpShift,InpMethod,InpPrice);
   ResetLastError();
   if(ExtMaHandle==INVALID_HANDLE)
     {
      PrintFormat("Failed to create iMA() handle. Error code: %d",GetLastError());
      return(INIT_FAILED);
     }
     
//--- get the time of the last price update
   datetime tick_time=TickTime();
//--- get moving average data and price data from the last two bars
   if(GetData(ExtMaHandle,ExtData,ExtRates) && tick_time!=0)
     {
      //--- if the price is above the MA
      if(ExtRates[1].close>ExtData[1])
        {
         //--- create a message text and display Alert
         string message=StringFormat("Bar time: %s. The price is above the moving average",TimeToString(ExtRates[1].time));
         Alert(message+" at "+TimeToString(tick_time,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
         /*
         Result:
         Alert: Bar time: 2024.02.16 18:00. The price is above the moving average at 2024.02.16 18:47:43
         */
        }
      else
        {
         //--- if the price is below the MA
         if(ExtRates[1].close<ExtData[1])
           {
            //--- create a message text and display Alert
            string message=StringFormat("Bar time: %s. The price is below the moving average.",TimeToString(ExtRates[1].time));
            Alert(message+" at "+TimeToString(tick_time,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
            /*
            Result:
            Alert: Bar time: 2024.02.16 19:00. The price is below the moving average at 2024.02.16 19:33:14
            */
           }
         else
           {
            //--- create a message text and display Alert
            string message=StringFormat("Bar time: %s. The price and moving average are equal.",TimeToString(ExtRates[1].time));
            Alert(message+" at "+TimeToString(tick_time,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
            /*
            Result:
            Alert: Bar time: 2024.02.16 20:00. The price and moving average are equal at 2024.02.16 20:12:22
            */
           }
        }
     }
     
//--- successful
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   ResetLastError();
//--- get moving average data and price data from the last two bars
   if(!GetData(ExtMaHandle,ExtData,ExtRates))
      return;
//--- get the direction of the price crossing the moving average on the current bar
   ENUM_INTERSECT_DIRECTION intersect=GetIntersectDirection(ExtData,ExtRates);
 
//--- variable for saving the previous message
   static string message_prev="";
 
//--- if the price has crossed the moving average on the current bar upwards
   if(intersect==INTERSECT_DIRECTION_UP)
     {
      //--- get the tick time, at which the crossing occurred
      datetime tick_time=TickTime();
      if(tick_time==0)
         return;
      //--- create a message text
      string message=StringFormat("Bar time: %s. The price crossed the MA from bottom to top",TimeToString(ExtRates[1].time));
      //--- if the previous message is not equal to the current one, display Alert with the message and tick time
      if(message!=message_prev)
        {
         Alert(message+" at "+TimeToString(tick_time,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
         message_prev=message;
         /*
         Result:\
         Alert: Bar time: 2024.02.16 09:00. The price crossed the MA from bottom to top at 2024.02.16 09:20:35
         */
        }
     }
 
//--- if the price has crossed the moving average on the current bar downwards
   if(intersect==INTERSECT_DIRECTION_DOWN)
     {
      //--- get the tick time, at which the crossing occurred
      datetime tick_time=TickTime();
      if(tick_time==0)
         return;
      //--- create a message text
      string message=StringFormat("Bar time: %s. The price crossed the MA from top to bottom",TimeToString(ExtRates[1].time));
      //--- if the previous message is not equal to the current one, display Alert with the message and tick time
      if(message!=message_prev)
        {
         Alert(message+" at "+TimeToString(tick_time,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
         message_prev=message;
         /*
         Result:\
         Alert: Bar time: 2024.02.16 10:00. The price crossed the MA from top to bottom at 2024.02.16 10:42:15
         */
        }
     }
  }
//+------------------------------------------------------------------+
//| Get price and moving average data into arrays                    |
//+------------------------------------------------------------------+
bool GetData(int handle,double &ma_data[],MqlRates &price_data[])
  {
   ResetLastError();
//--- get moving average data from the last two bars
   if(CopyBuffer(handle,0,0,2,ma_data)!=2)
     {
      PrintFormat("CopyBuffer() failed. Error code: %d",GetLastError());
      return(false);
     }
//--- get price data for the last two bars
   if(CopyRates(Symbol(),PERIOD_CURRENT,0,2,price_data)!=2)
     {
      PrintFormat("CopyRates() failed. Error code: %d",GetLastError());
      return(false);
     }
 
   return(true);
  }
//+------------------------------------------------------------------+
//| Return the direction of the price crossing the moving average    |
//+------------------------------------------------------------------+
ENUM_INTERSECT_DIRECTION GetIntersectDirection(double &ma_data[],MqlRates &price_data[])
  {
   double ma0=ma_data[1];
   double ma1=ma_data[0];
   double close0=price_data[1].close;
   double close1=price_data[0].close;
 
   if(close1<=ma1 && close0>ma0)
      return(INTERSECT_DIRECTION_UP);
   else
     {
      if(close1>=ma1 && close0<ma0)
         return(INTERSECT_DIRECTION_DOWN);
      else
         return(INTERSECT_DIRECTION_NONE);
     }
  }
//+------------------------------------------------------------------+
//| Return the tick time in seconds                                  |
//+------------------------------------------------------------------+
datetime TickTime()
  {
   MqlTick tick={};
 
   ResetLastError();
   if(!SymbolInfoTick(Symbol(),tick))
     {
      PrintFormat("SymbolInfoTick() failed. Error code: %d",GetLastError());
      return(0);
     }
 
   return(tick.time);
  }

```
