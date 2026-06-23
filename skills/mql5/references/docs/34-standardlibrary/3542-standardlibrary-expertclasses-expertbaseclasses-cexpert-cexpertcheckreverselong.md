# CheckReverseLong

Checks necessity and conditions to reverse a long position.

```
virtual bool  CheckReverseLong()

```

Return Value

true - a trade operation has been executed, otherwise - false.

Note

It checks the necessity to reverse a long position (CheckReverseLong() method of Signal object) and perform reverse operation of the current long position with the parameters set by Signal object ([ReverseLong(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertreverselong) method) if the conditions are met.

Implementation

```
//+------------------------------------------------------------------+
//| Check for long position reverse                                  |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation processed, false otherwise.      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::CheckReverseLong()
  {
   double   price=EMPTY_VALUE;
   double   sl=0.0;
   double   tp=0.0;
   datetime expiration=TimeCurrent();
//--- check signal for long reverse operations
   if(m_signal.CheckReverseLong(price,sl,tp,expiration)) return(ReverseLong(price,sl,tp));
//--- return without operations
   return(false);
  }

```
