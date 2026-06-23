# CheckOpenLong

Checks necessity and conditions to open long position.

```
virtual bool  CheckOpenLong()

```

Return Value

true - a trade operation has been executed, otherwise - false.

Note

It checks the necessity to open a long position (CheckOpenLong() method of Signal object) and does that with the parameters set by Signal object ([OpenLong()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertopenlong) method) if the conditions are met.

Implementation

```
//+------------------------------------------------------------------+
//| Check for long position open or limit/stop order set             |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation processed, false otherwise.      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::CheckOpenLong()
  {
   double   price=EMPTY_VALUE;
   double   sl=0.0;
   double   tp=0.0;
   datetime expiration=TimeCurrent();
//--- check signal for long enter operations
   if(m_signal.CheckOpenLong(price,sl,tp,expiration))
     {
      if(!m_trade.SetOrderExpiration(expiration))
        {
         m_expiration=expiration;
        }
      return(OpenLong(price,sl,tp));
     }
//--- return without operations
   return(false);
  }

```
