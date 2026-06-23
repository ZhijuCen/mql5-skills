# Descriptive chart properties

The ChartSetString/ChartGetString functions enable the reading and setting of the following string properties of the charts.

| Identifier | Description |
| --- | --- |
| CHART_COMMENT | Chart comment text |
| CHART_EXPERT_NAME | Name of the Expert Advisor running on the chart (r/o) |
| CHART_SCRIPT_NAME | Name of the script running on the chart (r/o) |

In chapter [Displaying messages in the chart window](/en/book/common/output/output_comment), we learned about the Comment function which displays a text message in the upper left corner of the chart. The CHART_COMMENT property allows you to read the current chart comment: ChartGetString(0, CHART_COMMENT). It is also possible to access comments on other charts by passing their identifiers to the function. By using ChartSetString, you can change comments on the current and other charts, if you know their ID: ChartSetString(ID, CHART_COMMENT, "text").

If an Expert Advisor or/and a script is running in any chart, we can find out their names using these calls: ChartGetString(ID, CHART_EXPERT_NAME) and ChartGetString(ID, CHART_SCRIPT_NAME).

The script ChartList3.mq5, similar to ChartList2.mq5, supplements the list of charts with information about Expert Advisors and scripts. Later we will add to it information about indicators.

```
void ChartList()
{
   const long me = ChartID();
   long id = ChartFirst();
   int count = 0, used = 0, temp, experts = 0, scripts = 0;
 
   Print("Chart List\nN, ID, Symbol, TF, *active");
   // keep iterating over charts until there are none left
   while(id != -1)
   {
      temp =0;// sign of MQL programs on this chart
      const string header = StringFormat("%d %lld %s %s %s",
         count, id, ChartSymbol(id), PeriodToString(ChartPeriod(id)),
         (id == me ? " *" : ""));
      // fields: N, id, symbol, timeframe, label of the current chart
      Print(header);
      string expert = ChartGetString(id, CHART_EXPERT_NAME);
      string script = ChartGetString(id, CHART_SCRIPT_NAME);
      if(StringLen(expert) > 0) expert = "[E] " + expert;
      if(StringLen(script) > 0) script = "[S] " + script;
      if(expert != NULL || script != NULL)
      {
         Print(expert, " ", script);
         if(expert != NULL) experts++;
         if(script != NULL) scripts++;
         temp++;
      }
      count++;
      if(temp > 0)
      {
         used++;
      }
      id = ChartNext(id);
   }
   Print("Total chart number: ", count, ", with MQL-programs: ", used);
   Print("Experts: ", experts, ", Scripts: ", scripts);
}

```

This is an example of the output of this script.

```
Chart List
N, ID, Symbol, TF, *active
0 132358585987782873 EURUSD M15 
1 132360375330772909 EURUSD H1  *
 [S] ChartList3
2 132544239145024745 XAUUSD H1 
3 132544239145024732 USDRUB D1 
4 132544239145024744 EURUSD H1 
Total chart number: 5, with MQL-programs: 1
Experts: 0, Scripts: 1

```

Here you can see that only one script is being executed.
