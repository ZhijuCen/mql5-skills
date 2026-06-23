# UninitializeReason

Returns the code of a [reason for deinitialization](/en/docs/constants/namedconstants/uninit).

```
int  UninitializeReason();

```

Return Value

Returns the value of [_UninitReason](/en/docs/predefined/_uninitreason) which is formed before [OnDeinit()](/en/docs/event_handlers/ondeinit) is called. Value depends on the reasons that led to deinitialization.

Example:

```
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- get the deinitialization reason code into the 'reason' variable
   int reason=UninitializeReason();
//--- create a message string with a deinitialization reason and send the message to the journal
   string message=StringFormat("%s: Uninitialize reason code: %d (%s)",__FUNCTION__, reason, UninitializeReasonDescription(reason));
   Print(message);
//--- successful
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- create a message string with a deinitialization reason code from the 'reason' formal variable and send the message to the journal
   string message=StringFormat("%s: Uninitialize reason code: %d (%s)",__FUNCTION__, reason, UninitializeReasonDescription(reason));
   Print(message);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
  }
//+------------------------------------------------------------------+
//| Return a description of the deinitialization reason code         |
//+------------------------------------------------------------------+
string UninitializeReasonDescription(const int reason)
  {
   switch(reason)
     {
      //--- the EA has stopped working calling the ExpertRemove() function
      case REASON_PROGRAM :
        return("Expert Advisor terminated its operation by calling the ExpertRemove() function");
      //--- program removed from a chart
      case REASON_REMOVE :
        return("Program has been deleted from the chart");
      //--- program recompiled
      case REASON_RECOMPILE :
        return("Program has been recompiled");
      //--- symbol or chart period changed
      case REASON_CHARTCHANGE :
        return("Symbol or chart period has been changed");
      //--- chart closed
      case REASON_CHARTCLOSE :
        return("Chart has been closed");
      //--- inputs changed by user
      case REASON_PARAMETERS :
        return("Input parameters have been changed by a user");
      //--- another account has been activated or reconnection to the trade server has occurred due to changes in the account settings
      case REASON_ACCOUNT :
        return("Another account has been activated or reconnection to the trade server has occurred due to changes in the account settings");
      //--- another chart template applied
      case REASON_TEMPLATE :
        return("A new template has been applied");
      //--- OnInit() handler returned a non-zero value
      case REASON_INITFAILED :
        return("This value means that OnInit() handler has returned a nonzero value");
      //--- terminal closed
      case REASON_CLOSE :
        return("Terminal has been closed");
     }
 
//--- deinitialization reason unknown
   return("Unknown reason");
  }

```
