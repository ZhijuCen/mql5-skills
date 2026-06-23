# ChartNext

Returns the chart ID of the chart next to the specified one.

```
long  ChartNext(
   long  chart_id      // Chart ID
   );

```

Parameters

chart_id

[in]  Chart ID. 0 does not mean the current chart. 0 means "return the first chart ID".

Return Value

Chart ID. If this is the end of the chart list, it returns -1.

Example:

```
//--- variables for chart ID
   long currChart,prevChart=ChartFirst();
   int i=0,limit=100;
   Print("ChartFirst =",ChartSymbol(prevChart)," ID =",prevChart);
   while(i<limit)// We have certainly not more than 100 open charts
     {
      currChart=ChartNext(prevChart); // Get the new chart ID by using the previous chart ID
      if(currChart<0) break;          // Have reached the end of the chart list
      Print(i,ChartSymbol(currChart)," ID =",currChart);
      prevChart=currChart;// let's save the current chart ID for the ChartNext()
      i++;// Do not forget to increase the counter
     }

```
