# CheckTrailingStop

It checks Trailing Stop conditions of the opened position.

```
virtual bool  CheckTrailingStop()

```

Return Value

true - a trade operation has been executed, otherwise - false.

Note

It checks Trailing Stop conditions of the opened position ([CheckTrailingStopLong()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertchecktrailingstoplong) or [CheckTrailingStopShort()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertchecktrailingstopshort) for long and short positions).

Implementation

```
//+------------------------------------------------------------------+
//| Check for trailing stop/profit position                          |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation processed, false otherwise.      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::CheckTrailingStop()
  {
//--- position must be selected before call
   if(m_position.PositionType()==POSITION_TYPE_BUY)
     {
      //--- check the possibility of modifying the long position
      if(CheckTrailingStopLong()) return(true);
     }
   else
     {
      //--- check the possibility of modifying the short position
      if(CheckTrailingStopShort()) return(true);
     }
//--- return without operations
   return(false);
  }

```
