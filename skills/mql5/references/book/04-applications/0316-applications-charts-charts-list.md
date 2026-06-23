# Getting the list of charts

An MQL program can get a list of charts opened in the terminal (both windows and [graph objects](/en/book/applications/objects/objects_chart)) using the functions ChartFirst and ChartNext.

long ChartFirst()

long ChartNext(long chartId)

The ChartFirst function returns the identifier of the first chart in the client terminal. MetaTrader 5 maintains an internal list of all charts, the order in which may differ from what we see on the screen, for example, in window tabs when they are maximized. In particular, the order in the list can change as a result of dragging tabs, undocking, and docking windows. After loading the terminal, the visible order of the bookmarks is the same as the internal list view.

The ChartNext function returns the ID of the chart following the chart with the specified chartId.

Unlike other functions for working with graphs, the value 0 in the ChartId parameter means not the current chart, but the beginning of the list. In other words, ChartNext(0) call is equivalent to ChartFirst.

If the end of the list is reached, the function returns -1.

The script ChartList1.mq5 outputs the list of charts into the log. The main work is performed by the ChartList function which is called from OnStart. At the very beginning of the function, we get the identifier of the current chart using [ChartID](/en/book/applications/charts/charts_id) and then we mark it with an asterisk in the list. At the end, the total number of charts is output.

```
void OnStart()
{
   ChartList();
}
   
void ChartList()
{
   const long me = ChartID();
   long id = ChartFirst();
   // long id = ChartNext(0); - analogue of calling ChartFirst()
   int count = 0, used = 0;
   Print("Chart List\nN, ID, *active");
   // keep iterating over charts until there are none left
   while(id != -1)
   {
      const string header = StringFormat("%d %lld %s",
         count, id, (id == me ? " *" : ""));
    
      // fields: N, id, label of the current chart
      Print(header);
      count++;
      id = ChartNext(id);
   }
   Print("Total chart number: ", count);
}

```

An example result is shown below.

```
Chart List
N, ID, *active
0 132358585987782873 
1 132360375330772909  *
2 132544239145024745 
3 132544239145024732 
4 132544239145024744 
Total chart number: 5

```
