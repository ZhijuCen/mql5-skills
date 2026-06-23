# Checking the number of calculated bars: BarsCalculated

When we create a third-party indicator by calling iCustom or other functions that we will see later in this chapter, it takes some time to calculate. As we know, the main measure of indicator data readiness is the number of calculated bars, which it returns from its OnCalculate function. Having the handle of the indicator, we can find out this number.

int BarsCalculated(int handle)

The function returns the number of bars for which data is calculated in the indicator specified by handle. In case of an error, we get -1.

While the data has not yet been calculated, the result is 0. Later this number should be compared with the size of the timeseries (for example, with rates_total if the calling indicator checks BarsCalculated in the context of its own OnCalculate function) to analyze the processing of new bars by the indicator.

In the UseWPR2.mq5 indicator, we will try to create IndWPR while changing the WPR period in the input argument.

```
input int WPRPeriod = 0;

```

Its default value is 0, which is an invalid value. It is proposed intentionally to demonstrate an abnormal situation. Recall that in the source IndWPR.mq5 code there are checks in OnInit and in OnCalculate.

```
// IndWPR.mq5
void OnInit()
{
   if(WPRPeriod < 1)
   {
      Alert(StringFormat("Incorrect Period value (%d). Should be 1 or larger",
         WPRPeriod));
   }
   ...
}
   
int OnCalculate(ON_CALCULATE_STD_FULL_PARAM_LIST)
{
   if(rates_total < WPRPeriod || WPRPeriod < 1) return 0;
   ...
}

```

Thus, at zero period, we should receive an error message, and BarsCalculated should always return 0. After we enter a positive value for the period, the auxiliary indicator should start calculating normally (and given the ease of calculating WPR, almost immediately), and BarsCalculated should return the total number of bars.

Now let's present the source code for creating a handle in UseWPR2.mq5.

```
// UseWPR2.mq5
int handle; // handle to global variable
   
int OnInit()
{
   // passing name and parameter
   handle = PRTF(iCustom(_Symbol, _Period, "IndWPR", WPRPeriod));
   // next check is useless here because you have to wait,
   // when the indicator is loaded, run and calculate
   // (here it is for demonstration purposes only)
   PRTF(BarsCalculated(handle));
   // successful initialization depends on the descriptor
   return handle == INVALID_HANDLE ? INIT_FAILED : INIT_SUCCEEDED;
}

```

In OnCalculate we just log the values BarsCalculated and rates_total.

```
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const int begin,
                const double &data[])
{
   // wait until the slave indicator is calculated on all bars
   if(PRTF(BarsCalculated(handle)) != PRTF(rates_total))
   {
      return prev_calculated;
   }
   
   // ... here is usually further work using handle
   
   return rates_total;
}

```

Compile and run UseWPR2, first with the parameter 0, and then with some valid value, for example, 21. Here are the log entries for period zero.

```
iCustom(_Symbol,_Period,IndWPR,WPRPeriod)=10 / ok
BarsCalculated(handle)=-1 / INDICATOR_DATA_NOT_FOUND(4806)
Alert: Incorrect Period value (0). Should be 1 or larger
BarsCalculated(handle)=0 / ok
rates_total=20000 / ok
...

```

Immediately after the creation of the handle, the data is not yet available, so the INDICATOR_DATA_NOT_FOUND(4806) error is shown, and the result BarsCalculated equals -1. This is followed by a notification about an incorrect input parameter, which confirms the successful loading and launch of the indicator IndWPR. In the following segment, we get the BarsCalculated value equal to 0.

In order for the indicator to be calculated, we will enter the correct input parameter. In this case, BarsCalculated equals rates_total.

```
iCustom(_Symbol,_Period,IndWPR,WPRPeriod)=10 / ok
BarsCalculated(handle)=-1 / INDICATOR_DATA_NOT_FOUND(4806)
BarsCalculated(handle)=20000 / ok
rates_total=20000 / ok
...

```

After we have mastered checking the readiness of a slave indicator, we can start reading its data. Let's do this in the next example UseWPR3.mq5, where we will get acquainted with the function CopyBuffer.
