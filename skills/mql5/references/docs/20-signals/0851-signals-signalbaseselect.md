# SignalBaseSelect

Selects a signal from signals, available in terminal for further working with it.

```
bool  SignalBaseSelect(
   int     index     // signal index
   );

```

Parameters

index

[in]  Signal index in base of trading signals.

Return Value

Returns true if successful, otherwise returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

Example:

```
void OnStart()
  {
//--- get total amount of signals in the terminal
   int total=SignalBaseTotal();
//--- process all signals
   for(int i=0;i<total;i++)
     {
      //--- select the signal by index
      if(SignalBaseSelect(i))
        {
         //--- get signal properties
         long   id    =SignalBaseGetInteger(SIGNAL_BASE_ID);          // signal id
         long   pips  =SignalBaseGetInteger(SIGNAL_BASE_PIPS);        // profit in pips
         long   subscr=SignalBaseGetInteger(SIGNAL_BASE_SUBSCRIBERS); // number of subscribers
         string name  =SignalBaseGetString(SIGNAL_BASE_NAME);         // signal name
         double price =SignalBaseGetDouble(SIGNAL_BASE_PRICE);        // signal price
         string curr  =SignalBaseGetString(SIGNAL_BASE_CURRENCY);     // signal currency
         //--- print all profitable free signals with subscribers
         if(price==0.0 && pips>0 && subscr>0)
            PrintFormat("id=%d, name=\"%s\", currency=%s, pips=%d, subscribers=%d",id,name,curr,pips,subscr);
        }
      else PrintFormat("Error in call of SignalBaseSelect. Error code=%d",GetLastError());
     }
  }

```
