# CheckReverseShort

Checks necessity and conditions to reverse a short position.

```
virtual bool  CheckReverseLong()

```

Return Value

true - a trade operation has been executed, otherwise - false.

Note

It checks the necessity to reverse a short position (CheckReverseShort() method of Signal object) and perform reverse operation of the current short position with the parameters set by Signal object ([ReverseShort()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertreverseshort) method) if the conditions are met.

Implementation

```
//+------------------------------------------------------------------+
//| Check for short position reverse                                 |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation processed, false otherwise.      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::CheckReverseShort()
  {
   double   price=EMPTY_VALUE;
   double   sl=0.0;
   double   tp=0.0;
   datetime expiration=TimeCurrent();
//--- check signal for short reverse operations
   if(m_signal.CheckReverseShort(price,sl,tp,expiration)) return(ReverseShort(price,sl,tp));
//--- return without operations
   return(false);
  }

```
