# OnStart

The function is called in scripts and services when the [Start](/en/docs/runtime/event_fire#start) event occurs. The function is intended for one-time execution of actions implemented in a program. There are two function types.

The version that returns the result

```
int  OnStart(void);

```

Return Value

The value of [int](/en/docs/basis/types/integer/integertypes#int) type displayed in the Journal tab.

The entry "script script_name removed (result code N)" is created in the terminal journal after a script execution is complete. Here N is a value returned by the OnStart() function.

The entry "service service_name stopped (result code N)" is created in the terminal journal after a service execution is complete. Here N is a value returned by the OnStart() function.

The OnStart() call that returns the execution result is recommended for use since it not only allows for a script or service execution, but also returns an error code or other useful data to analyze the program execution result.

The version without a result return is left only for compatibility with old codes. It is not recommended for use

```
void  OnStart(void);

```

Note

OnStart() is the only function for handling events in scripts and services. No other events are sent to these programs. In turn, the [Start](/en/docs/runtime/event_fire#start) event is not passed to EAs and custom indicators.

Sample script:

```
//--- macros for working with colors
#define XRGB(r,g,b)    (0xFF000000|(uchar(r)<<16)|(uchar(g)<<8)|uchar(b))
#define GETRGB(clr)    ((clr)&0xFFFFFF)
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set a downward candle color
   Comment("Set a downward candle color"); 
   ChartSetInteger(0,CHART_COLOR_CANDLE_BEAR,GetRandomColor());
   ChartRedraw(); // update the chart immediately without waiting for a new tick
   Sleep(1000);   // pause for 1 second to see all the changes
//--- set an upward candle color
   Comment("Set an upward candle color"); 
   ChartSetInteger(0,CHART_COLOR_CANDLE_BULL,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set the background color
   Comment("Set the background color"); 
   ChartSetInteger(0,CHART_COLOR_BACKGROUND,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set color of Ask line
   Comment("Set color of Ask line"); 
   ChartSetInteger(0,CHART_COLOR_ASK,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set color of Bid line
   Comment("Set color of Bid line"); 
   ChartSetInteger(0,CHART_COLOR_BID,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);    
//--- set color of a downward bar and a downward candle frame
   Comment("Set color of a downward bar and a downward candle frame"); 
   ChartSetInteger(0,CHART_COLOR_CHART_DOWN,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set color of a chart line and Doji candlesticks
   Comment("Set color of a chart line and Doji candlesticks"); 
   ChartSetInteger(0,CHART_COLOR_CHART_LINE,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set color of an upward bar and an upward candle frame  
   Comment("Set color of an upward bar and an upward candle frame"); 
   ChartSetInteger(0,CHART_COLOR_CHART_UP,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set color of axes, scale and OHLC line
   Comment("Set color of axes, scale and OHLC line"); 
   ChartSetInteger(0,CHART_COLOR_FOREGROUND,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set a grid color
   Comment("Set a grid color"); 
   ChartSetInteger(0,CHART_COLOR_GRID,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set Last price color
   Comment("Set Last price color"); 
   ChartSetInteger(0,CHART_COLOR_LAST,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set color of Stop Loss and Take Profit order levels
   Comment("Set color of Stop Loss and Take Profit order levels"); 
   ChartSetInteger(0,CHART_COLOR_STOP_LEVEL,GetRandomColor());
   ChartRedraw(); 
   Sleep(1000);   
//--- set color of volumes and market entry levels
   Comment("Set color of volumes and market entry levels"); 
   ChartSetInteger(0,CHART_COLOR_VOLUME,GetRandomColor());
   ChartRedraw();
  }
//+------------------------------------------------------------------+
//| Return a randomly generated color                                |
//+------------------------------------------------------------------+
color GetRandomColor()
  {
   color clr=(color)GETRGB(XRGB(rand()%255,rand()%255,rand()%255));
   return clr;
  }

```

See also

[Event handling functions](/en/docs/basis/function/events), [Program running](/en/docs/runtime/running), [Client terminal events](/en/docs/runtime/event_fire)
