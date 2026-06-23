# Uninitialization Reason Codes

Uninitialization reason [codes](/en/docs/mql5_guide#expert) are returned by the [UninitializeReason()](/en/docs/check/uninitializereason) function. The possible values are the following:

| Constant | Value | Description |
| --- | --- | --- |
| REASON_PROGRAM | 0 | Expert Advisor terminated its operation by calling the  ExpertRemove()  function |
| REASON_REMOVE | 1 | Program has been deleted from the chart |
| REASON_RECOMPILE | 2 | Program has been recompiled |
| REASON_CHARTCHANGE | 3 | Symbol or chart period has been changed |
| REASON_CHARTCLOSE | 4 | Chart has been closed |
| REASON_PARAMETERS | 5 | Input parameters have been changed by a user |
| REASON_ACCOUNT | 6 | Another account has been activated or reconnection to the trade server has occurred due to changes in the account settings |
| REASON_TEMPLATE | 7 | A new template has been applied |
| REASON_INITFAILED | 8 | This value means that  OnInit()  handler has returned a nonzero value |
| REASON_CLOSE | 9 | Terminal has been closed |

The uninitialization reason code is also passed as a parameter of the predetermined function [OnDeinit](/en/docs/event_handlers/ondeinit)(const int reason).

Example:

```
//+------------------------------------------------------------------+
//| get text description                                             |
//+------------------------------------------------------------------+
string getUninitReasonText(int reasonCode)
  {
   string text="";
//---
   switch(reasonCode)
     {
      case REASON_ACCOUNT:
         text="Account was changed";break;
      case REASON_CHARTCHANGE:
         text="Symbol or timeframe was changed";break;
      case REASON_CHARTCLOSE:
         text="Chart was closed";break;
      case REASON_PARAMETERS:
         text="Input-parameter was changed";break;
      case REASON_RECOMPILE:
         text="Program "+__FILE__+" was recompiled";break;
      case REASON_REMOVE:
         text="Program "+__FILE__+" was removed from chart";break;
      case REASON_TEMPLATE:
         text="New template was applied to chart";break;
      default:text="Another reason";
     }
//---
   return text;
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- The first way to get the uninitialization reason code
   Print(__FUNCTION__,"_Uninitalization reason code = ",reason);
//--- The second way to get the uninitialization reason code
   Print(__FUNCTION__,"_UninitReason = ",getUninitReasonText(_UninitReason));
  }

```
