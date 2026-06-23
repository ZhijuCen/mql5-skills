# CheckOpen

Checks conditions to open a position.

```
virtual bool  CheckOpen()

```

Return Value

true - a trade operation has been executed, otherwise - false.

Note

It checks the necessity to open long ([CheckOpenLong()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertcheckopenlong)) and short ([CheckOpenShort()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertcheckopenshort)) positions.

Implementation

```
//+------------------------------------------------------------------+
//| Check for position open or limit/stop order set                  |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation processed, false otherwise.      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::CheckOpen()
  {
   if(CheckOpenLong())  return(true);
   if(CheckOpenShort()) return(true);
//--- return without operations
   return(false);
  }

```
