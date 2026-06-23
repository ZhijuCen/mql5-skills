# Limitations and advantages of indicators

All specialized functions discussed in this chapter are available only in the indicator source codes. It makes no sense to use them in other types of MQL programs: they will return an error.

There are other functions that are prohibited in indicators:

- [OrderCalcMargin](/en/book/automation/experts/experts_ordercalcmargin)
- [OrderCalcProfit](/en/book/automation/experts/experts_ordercalcprofit)
- [OrderCheck](/en/book/automation/experts/experts_ordercheck)
- [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync)
- [SendFTP](/en/book/advanced/network/network_ftp)
- [WebRequest](/en/book/advanced/network/network_http)
- [Socket***](/en/book/advanced/network/network_socket_create_connect)
- [Sleep](/en/book/common/timing/timing_sleep)
- [MessageBox](/en/book/common/output/output_messagebox)
- [ExpertRemove](/en/book/applications/runtime/runtime_remove)

Some of them (with the prefix Order-) refer to trading calculations and are only allowed in Expert Advisors and scripts. Others are intended for executing requests that block the tread execution until the result is returned, while this is not allowed for indicators because they are executed in the terminal's interface thread. For a similar reason, the Sleep and MessageBox functions are prohibited.

Indicators are primarily responsible for visualizing data and, oddly enough, are not suitable for massive calculations. In particular, if you decide to create an indicator that trains a neural network or a decision tree in the process, this will most likely negatively affect the normal functioning of the terminal.

The effect of a long calculation is demonstrated by the indicator IndBarIndex.mq5, which in the normal mode is designed to display bar numbers in the elements of its buffer. However, using the input parameter SimulateCalculation, which should be set to true, you can start an infinite loop on a timer.

```
// Setting to true will freeze the drawing of indicators
// on charts of the same working symbol
// Attention! Don't forget to remove the indicator after the experiment!
input bool SimulateCalculation = false;
 
void OnInit()
{
   ...
   if(SimulateCalculation)
   {
      EventSetTimer(1);
   }
}
...  
void OnTimer()
{
   Comment("Calculation started at ", TimeLocal());
   while(!IsStopped())
   {
   // infinite loop to emulate calculations
   }
   Comment("");
}

```

In this mode, the indicator, as expected, begins to completely occupy 1 processor core, but another side effect also appears. Any indicators on the same symbol where IndBarIndex is placed, stop updating. For example, we can run IndBarIndex on EURUSD (any timeframe), and then on any other EURUSD chart, you can try to apply a regular moving average: it will not be displayed until you remove IndBarIndex from the first chart.

In this regard, all lengthy calculations should be placed in separate threads, that is, scripts or non-trading Expert Advisors, and only their results should be used in indicators. The MQL5 API allows you to create new [charts](/en/book/applications/charts) or [objects with charts](/en/book/applications/objects/objects_chart), in which it is possible to apply [tpl templates](/en/book/applications/charts/charts_tpl) with the required Expert Advisor or script.
