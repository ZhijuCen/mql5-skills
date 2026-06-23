# Opening and closing charts

An MQL program can not only analyze the list of charts but also modify it: open new ones or close existing ones. Two functions are allocated for these purposes: ChartOpen and ChartClose.

long ChartOpen(const string symbol, ENUM_TIMEFRAMES timeframe)

The function opens a new chart with the specified symbol and timeframe and returns the ID of the new chart. If an error occurs during execution, the result is 0, and the error code can be read in the built-in variable _LastError.

If the symbol parameter is NULL, it means the symbol of the current chart (on which the MQL program is being executed). The 0 value in the timeframe parameter corresponds to PERIOD_CURRENT.

The maximum possible number of simultaneously open charts in the terminal cannot exceed CHARTS_MAX (100).

We will see an example of using the ChartOpen function in the next section, after studying the functions for working with tpl templates.

Please note that the terminal allows you to create not only full-fledged windows with charts but also [chart objects](/en/book/applications/objects/objects_chart). They are placed inside normal charts in the same way as other graphical objects such as trend lines, channels, price labels, etc. Chart objects allow you to display within one standard chart several small fragments of price series for alternative symbols and timeframes.

bool ChartClose(long chartId = 0)

The function closes the chart with the specified ID (the default value of 0 means the current chart). The function returns a success indicator.

As an example, let's implement the script ChartCloseIdle.mq5, which will close duplicate charts with repeated symbol and timeframe combinations if they do not contain MQL programs and graphical objects.

First, we need to make a list that counts the charts for a particular symbol/timeframe pair. This task is implemented by the ChartIdleList function, which is very similar to what we saw in the script ChartList.mq5. The list itself is formed in the map array MapArray<string,int> chartCounts.

```
#include <MQL5Book/Periods.mqh>
#include <MQL5Book/MapArray.mqh>
   
#define PUSH(A,V) (A[ArrayResize(A, ArraySize(A) + 1) - 1] = V)
   
void OnStart()
{
   MapArray<string,int> chartCounts;
   ulong duplicateChartIDs[];
   // collect duplicate empty charts
   if(ChartIdleList(chartCounts, duplicateChartIDs))
   {
      ...
   }
   else
   {
      Print("No idle charts.");
   }
}

```

Meanwhile, the ChartIdleList function fills the duplicateChartIDs array with identifiers of free charts that match the closing conditions.

```
int ChartIdleList(MapArray<string,int> &map, ulong &duplicateChartIDs[])
{
   // list charts until their list ends
   for(long id = ChartFirst(); id != -1; id = ChartNext(id))
   {
      // skip objects
      if(ChartGetInteger(id, CHART_IS_OBJECT)) continue;
   
      // getting the main properties of the chart
      const int win = (int)ChartGetInteger(id, CHART_WINDOWS_TOTAL);
      const string expert = ChartGetString(id, CHART_EXPERT_NAME);
      const string script = ChartGetString(id, CHART_SCRIPT_NAME);
      const int objectCount = ObjectsTotal(id);
   
      // count the number of indicators
      int indicators = 0;
      for(int i = 0; i < win; ++i)      
      {
         indicators += ChartIndicatorsTotal(id, i);
      }
      
      const string key = ChartSymbol(id) + "/" + PeriodToString(ChartPeriod(id));
      
      if(map[key] == 0     // the first time we always read a new symbol/TF combination
                           // otherwise, only empty charts are counted:
         || (indicators == 0           // no indicators
            && StringLen(expert) == 0  // no Expert Advisor
            && StringLen(script) == 0  // no script
            && objectCount == 0))      // no objects
      {
         const int i = map.inc(key);
         if(map[i] > 1)                // duplicate
         {
            PUSH(duplicateChartIDs, id);
         }
      }
   }
   return map.getSize();
}

```

After the list for deletion is formed, in OnStart we call the ChartClose function in a loop over the list.

```
void OnStart()
{
   ...
   if(ChartIdleList(chartCounts, duplicateChartIDs))
   {
      for(int i = 0; i < ArraySize(duplicateChartIDs); ++i)
      {
         const ulong id = duplicateChartIDs[i];
         // request to bring the chart to the front
         ChartSetInteger(id, CHART_BRING_TO_TOP, true);
         // update the state of the windows, pumping the queue with the request
         ChartRedraw(id);
         // ask user for confirmation
         const int button = MessageBox(
            "Remove idle chart: "
            + ChartSymbol(id) + "/" + PeriodToString(ChartPeriod(id)) + "?",
            __FILE__, MB_YESNOCANCEL);
         if(button == IDCANCEL) break;   
         if(button == IDYES)
         {
            ChartClose(id);
         }
      }
      ...

```

For each chart, first the function ChartSetInteger(id, CHART_BRING_TO_TOP, true) is called to show the user which window is supposed to be closed. Since this function is asynchronous (only puts the command to activate the window in the event queue), you need to additionally call ChartRedraw, which processes all accumulated messages. The user is then prompted to confirm the action. The chart only closes on clicking Yes. Selecting No skips the current chart (leaves it open), and the loop continues. By pressing Cancel, you can interrupt the loop ahead of time.
