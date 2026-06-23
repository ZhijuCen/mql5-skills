# Finding objects

There are three functions to search for objects on the chart. The first two, the ObjectsTotal and ObjectName, allow you to sort through objects by name, and then, if necessary, use the name of each object to analyze its other properties (we will describe how this is done in the next section). The third function, ObjectFind, allows you to check the existence of an object by a known name. The same could be done by simply requesting some property via the ObjectGet function: if there is no object with the passed name, we will get an error in _LastError, but this is less convenient than calling ObjectFind. Besides, the function immediately returns the number of the window in which the object is located.

int ObjectsTotal(long chartId, int window = -1, int type = -1)

The function returns the number of objects on the chart with the chartId identifier (0 means current chart). Only objects in the subwindow with the specified window number are considered in the calculation (0 represents the main window, -1 represents the main window and all subwindows). Note that only objects of the specific type specified in the type parameter are taken into account (-1 indicates all types by default). The value of type can be an element from the ENUM_OBJECT enumeration.

The function is executed synchronously, that is, it blocks the execution of the calling MQL program until the result is received.

string ObjectName(long chartId, int index, int window = -1, int type = -1)

The function returns the name of the object under the index number on the chart with the chartId identifier. When compiling the internal list, within which the object is searched, the specified subwindow number (window) and object type (type) are taken into account. The list is sorted by object names in lexicographic order, that is, in particular, alphabetically, case sensitive.

Like ObjectsTotal, during its execution, ObjectName waits for the entire queue of chart commands to be fetched, and then returns the name of the object from the updated list of objects.

In case of an error, an empty string will be obtained, and the OBJECT_NOT_FOUND (4202) error code will be stored in _LastError.

To test the functionality of these two functions, let's create a script called ObjectFinder.mq5 that logs all objects on all charts. It uses [chart iteration](/en/book/applications/charts/charts_list) functions (ChartFirst and ChartNext), as well as functions for getting [chart properties](/en/book/applications/charts/charts_symbol_period) (ChartSymbol, ChartPeriod, and ChartGetInteger).

```
#include <MQL5Book/Periods.mqh>
   
void OnStart()
{
   int count = 0;
   long id = ChartFirst();
   // loop through charts
   while(id != -1)
   {
      PrintFormat("%s %s (%lld)", ChartSymbol(id), PeriodToString(ChartPeriod(id)), id);
      const int win = (int)ChartGetInteger(id, CHART_WINDOWS_TOTAL);
      // loop through windows
      for(int k = 0; k < win; ++k)
      {
         PrintFormat("  Window %d", k);
         const int n = ObjectsTotal(id, k);
         // loop through objects
         for(int i = 0; i < n; ++i)
         {
            const string name = ObjectName(id, i, k);
            const ENUM_OBJECT type = (ENUM_OBJECT)ObjectGetInteger(id, name, OBJPROP_TYPE);
            PrintFormat("    %s %s", EnumToString(type), name);
            ++count;
         }
      }
      id = ChartNext(id);
   }
   
   PrintFormat("%d objects found", count);
}

```

For each chart, we determine the number of subwindows (ChartGetInteger(id, CHART_WINDOWS_TOTAL)), call ObjectsTotal for each subwindow, and call ObjectName in the inner loop. Next, by name, we find the type of object and display them together in the log.

Below is a version of the possible result of the script (with abbreviations).

```
EURUSD H1 (132358585987782873)
  Window 0
    OBJ_FIBO H1 Fibo 58513
    OBJ_TEXT H1 Text 40688
    OBJ_TREND H1 Trendline 3291
    OBJ_VLINE H1 Vertical Line 28732
    OBJ_VLINE H1 Vertical Line 33752
    OBJ_VLINE H1 Vertical Line 35549
  Window 1
  Window 2
EURUSD D1 (132360375330772909)
  Window 0
EURUSD M15 (132544239145024745)
  Window 0
    OBJ_VLINE H1 Vertical Line 27032
...
XAUUSD D1 (132544239145024746)
  Window 0
    OBJ_EVENT ObjShow-2021.11.25 00:00:00
    OBJ_TEXT ObjShow-2021.11.26 00:00:00
    OBJ_ARROW_SELL ObjShow-2021.11.29 00:00:00
    OBJ_ARROW_BUY ObjShow-2021.11.30 00:00:00
    OBJ_ARROW_RIGHT_PRICE ObjShow-2021.12.01 00:00:00
    OBJ_ARROW_LEFT_PRICE ObjShow-2021.12.02 00:00:00
    OBJ_ARROW_CHECK ObjShow-2021.12.03 00:00:00
    OBJ_ARROW_STOP ObjShow-2021.12.06 00:00:00
    OBJ_ARROW_DOWN ObjShow-2021.12.07 00:00:00
    OBJ_ARROW_UP ObjShow-2021.12.08 00:00:00
    OBJ_ARROW_THUMB_DOWN ObjShow-2021.12.09 00:00:00
    OBJ_ARROW_THUMB_UP ObjShow-2021.12.10 00:00:00
    OBJ_HLINE ObjShow-2021.12.13 00:00:00
    OBJ_VLINE ObjShow-2021.12.14 00:00:00
...
35 objects found

```

Here, in particular, you can see that on the XAUUSD, D1 chart there are objects generated by the ObjectSimpleShowcase.mq5 script. There are no objects in some charts and in some subwindows.

int ObjectFind(long chartId, const string name)

The function searches for an object by name on the chart specified by the identifier and, if successful, returns the number of the window where it was found.

If the object is not found, the function returns a negative number. Like the previous functions in this section, the ObjectFind function uses a synchronous call.

We will see an example of using this function in the ObjectCopy.mq5 script in the next section.
