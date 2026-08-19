# OnDeinit

The function is called in indicators and EAs when the [Deinit](/en/docs/runtime/event_fire#deinit) event occurs. It is used to deinitialize a running MQL5 program.

```
void  OnDeinit(
   const int  reason         // deinitialization reason code
   );

```

Parameters

reason

[in]  Deinitialization reason code.

Return Value

No return value

Note

Deinit event is generated for EAs and indicators in the following cases:

- before a re-initialization due to the change of a symbol or a chart period the mql5 program is attached to;
- before a re-initialization due to the change of the [inputs](/en/docs/basis/variables/inputvariables);
- before unloading an mql5 program.

The reason parameter may have the following values:

| Constant | Value | Description |
| --- | --- | --- |
| REASON_PROGRAM | 0 | The EA has stopped working calling the  ExpertRemove()  function |
| REASON_REMOVE | 1 | Program removed from a chart |
| REASON_RECOMPILE | 2 | Program recompiled |
| REASON_CHARTCHANGE | 3 | A symbol or a chart period is changed |
| REASON_CHARTCLOSE | 4 | Chart closed |
| REASON_PARAMETERS | 5 | Inputs changed by a user |
| REASON_ACCOUNT | 6 | Another account has been activated or reconnection to the trade server has occurred due to changes in the account settings |
| REASON_TEMPLATE | 7 | Another chart template applied |
| REASON_INITFAILED | 8 | The  OnInit()  handler returned a non-zero value |
| REASON_CLOSE | 9 | Terminal closed |

[EA](/en/docs/mql5_guide#expert) deinitialization reason codes can be received by the [UninitializeReason()](/en/docs/check/uninitializereason) function or from the predefined [_UninitReason](/en/docs/predefined/_uninitreason) variable.

Sample OnInit() and OnDeinit() functions for the EA

```
input int fake_parameter=3;      // useless parameter
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- Get the number of a build where the program is compiled
   Print(__FUNCTION__," Build #",__MQLBUILD__);
//--- Reset reason code can also be obtained in OnInit()
   Print(__FUNCTION__," Deinitialization reason code can be received during the EA reset");
//--- The first way to get a deinitialization reason code
   Print(__FUNCTION__," _UninitReason = ",getUninitReasonText(_UninitReason));
//--- The second way to get a deinitialization reason code  
   Print(__FUNCTION__," UninitializeReason() = ",getUninitReasonText(UninitializeReason()));
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- The first way to get a deinitialization reason code
   Print(__FUNCTION__," Deinitialization reason code = ",reason);
//--- The second way to get a deinitialization reason code
   Print(__FUNCTION__," _UninitReason = ",getUninitReasonText(_UninitReason));
//--- The third way to get a deinitialization reason code  
   Print(__FUNCTION__," UninitializeReason() = ",getUninitReasonText(UninitializeReason()));
  }
//+------------------------------------------------------------------+
//| Return a textual description of the deinitialization reason code |
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

```

See also

[OnInit](/en/docs/event_handlers/oninit),[ Event handling functions](/en/docs/basis/function/events), [Program running](/en/docs/runtime/running), [Client terminal events](/en/docs/runtime/event_fire), [Uninitialization reason codes](/en/docs/constants/namedconstants/uninit), [Visibility scope and lifetime of variables](/en/docs/basis/variables/variable_scope), [Creating and deleting objects](/en/docs/basis/variables/object_live)
