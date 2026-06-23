# PositionSelect

Chooses an open position for further working with it. Returns true if the function is successfully completed. Returns false in case of failure. To obtain information about the error, call [GetLastError()](/en/docs/check/getlasterror).

```
bool  PositionSelect(
   string  symbol      // Symbol name
   );

```

Parameters

symbol

[in]  Name of the financial security.

Return Value

Value of the bool type.

Note

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol. In this case, PositionSelect will select a position with the lowest ticket.

Function PositionSelect() copies data about a position into the program environment, and further calls of [PositionGetDouble()](/en/docs/trading/positiongetdouble), [PositionGetInteger()](/en/docs/trading/positiongetinteger) and [PositionGetString()](/en/docs/trading/positiongetstring) return the earlier copied data. This means that the position itself may no longer exist (or its volume, direction, etc. has changed), but data of this position still can be obtained. To ensure receipt of fresh data about a position, it is recommended to call PositionSelect() right before referring to them.

Example:

```
#define   SYMBOL_NAME   "EURUSD"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- select a position on a specified symbol
   if(!PositionSelect(SYMBOL_NAME))
     {
      PrintFormat("PositionSelect(%s) failed. Error %d",SYMBOL_NAME, GetLastError());
      return;
     }
 
//--- if a position is selected, we can obtain its data using PositionGetDouble(), PositionGetInteger() and PositionGetString()
//--- get the selected position ticket
   ResetLastError();
   long ticket=PositionGetInteger(POSITION_TICKET);
   if(ticket==0)
     {
      PrintFormat("Failed to get %s position ticket. Error %d", SYMBOL_NAME, GetLastError());
      return;
     }
     
//--- if a ticket is successfully received, print the selected position symbol and ticket in the journal
   PrintFormat("The position that is selected on the %s symbol has ticket %I64d", SYMBOL_NAME, ticket);
   /*
   result:
   The position that is selected on the EURUSD symbol has ticket 2810846623
   */
  }

```

See also

[PositionGetSymbol()](/en/docs/trading/positiongetsymbol), [PositionsTotal()](/en/docs/trading/positionstotal), [Position Properties](/en/docs/constants/tradingconstants/positionproperties)
