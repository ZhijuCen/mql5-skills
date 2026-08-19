# GetLastError

Returns the contents of the system variable [_LastError](/en/docs/predefined/_lasterror).

```
int  GetLastError();

```

Return Value

Returns the value of the last [error](/en/docs/constants/errorswarnings/errorcodes) that occurred during the execution of an mql5 program.

Note

After the function call, the contents of _LastError are not reset. To reset this variable, you need to call [ResetLastError()](/en/docs/common/resetlasterror).

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   MqlRates rates[1]={};   // display the current bar data here
   
//--- intentionally call a function with inappropriate parameters
   int res=CopyRates(NULL, PERIOD_CURRENT, 0, 2, rates);
   if(res!=2)
      PrintFormat("CopyRates() returned %d. LastError %d", res, GetLastError());
 
//--- reset the last error code before copying the current bar data to the MqlRates structure
   ResetLastError();
//--- if the function does not work correctly, the error code will differ from 0
   CopyRates(NULL, PERIOD_CURRENT, 0, 1, rates);
   Print("CopyRates() error ", GetLastError());
     
//--- print the array of obtained values
   ArrayPrint(rates);
  }

```

See also

[Trade Server Return Codes](/en/docs/constants/errorswarnings/enum_trade_return_codes)
