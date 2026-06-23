# PositionGetString

The function returns the requested property of an open position, pre-selected using [PositionGetSymbol](/en/docs/trading/positiongetsymbol) or [PositionSelect](/en/docs/trading/positionselect). The position property should be of the string type. There are 2 variants of the function.

1. Immediately returns the property value.

```
string  PositionGetString(
   ENUM_POSITION_PROPERTY_STRING  property_id      // Property identifier
   );

```

2. Returns true or false, depending on the success of the function execution. If successful, the value of the property is placed in a receiving variables passed by reference by the last parameter.

```
bool  PositionGetString(
   ENUM_POSITION_PROPERTY_STRING  property_id,     // Property identifier
   string&                        string_var       // Here we accept the property value
   );

```

Parameters

property_id

[in]  Identifier of a position property. The value can be one of the values of the [ENUM_POSITION_PROPERTY_STRING](/en/docs/constants/tradingconstants/positionproperties#enum_position_property_string) enumeration.

string_var

[out]  Variable of the string type accepting the value of the requested property.

Return Value

Value of the [string](/en/docs/basis/types/stringconst) type. If the function fails, an empty string is returned.

Note

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol.

To ensure receipt of fresh data about a position, it is recommended to call [PositionSelect()](/en/docs/trading/positionselect) right before referring to them.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- in a loop by all account positions
   int total=PositionsTotal();
   for(int i=0; i<total; i++)
     {
      //--- get the ticket of the next position by automatically selecting a position to access its properties
      ulong ticket=PositionGetTicket(i);
      if(ticket==0)
         continue;
      
      //--- get the position type and display the header for the list of position string properties
      string type=(PositionGetInteger(POSITION_TYPE)==POSITION_TYPE ? "Buy" : "Sell");
      PrintFormat("String properties of an open position %s #%I64u:", type, ticket);
      
      //--- print all the string properties of the selected position under the header
      PositionPropertiesStringPrint(15);
     }
   /*
   result:
   String properties of an open position Buy #2810798881:
   Symbol:        EURUSD
   Comment:       Test PositionGetString
   External ID:   
   */
  }
//+------------------------------------------------------------------+
//| Display string properties of the selected position in the journal|
//+------------------------------------------------------------------+
void PositionPropertiesStringPrint(const uint header_width=0)
  {
   uint   w=0;
   string header="";
   string value="";
   
//--- define the header text and the width of the header field
//--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
   header="Symbol:";
   w=(header_width==0 ? header.Length()+1 : header_width);
//--- get and display the position symbol with the specified header width in the journal
   if(!PositionGetString(POSITION_SYMBOL, value))
      return;
   PrintFormat("%-*s%-s", w, header, value);
   
//--- display the position comment in the journal
   header="Comment:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!PositionGetString(POSITION_COMMENT, value))
      return;
   PrintFormat("%-*s%-s", w, header, value);
   
//--- display the position ID in an external system in the journal 
   header="External ID:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!PositionGetString(POSITION_EXTERNAL_ID, value))
      return;
   PrintFormat("%-*s%-s", w, header, value);
  }

```

See also

[PositionGetSymbol()](/en/docs/trading/positiongetsymbol), [PositionSelect()](/en/docs/trading/positionselect), [Position Properties](/en/docs/constants/tradingconstants/positionproperties)
