# PositionGetDouble

The function returns the requested property of an open position, pre-selected using [PositionGetSymbol](/en/docs/trading/positiongetsymbol) or [PositionSelect](/en/docs/trading/positionselect). The position property must be of the double type. There are 2 variants of the function.

1. Immediately returns the property value.

```
double  PositionGetDouble(
   ENUM_POSITION_PROPERTY_DOUBLE  property_id      // Property identifier
   );

```

2. Returns true or false, depending on the success of the function execution. If successful, the value of the property is placed in a receiving variable passed by reference by the last parameter.

```
bool  PositionGetDouble(
   ENUM_POSITION_PROPERTY_DOUBLE  property_id,     // Property identifier
   double&                        double_var       // Here we accept the property value
   );

```

Parameters

property_id

[in]  Identifier of a position property. The value can be one of the values of the [ENUM_POSITION_PROPERTY_DOUBLE](/en/docs/constants/tradingconstants/positionproperties#enum_position_property_double) enumeration.

double_var

[out]  Variable of the double type, accepting the value of the requested property.

Return Value

Value of the [double](/en/docs/basis/types/double) type. If the function fails, 0 is returned.

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
      
      //--- get the position type and display the header for the list of position real properties
      string type=(PositionGetInteger(POSITION_TYPE)==POSITION_TYPE ? "Buy" : "Sell");
      PrintFormat("Double properties of an open position %s #%I64u:", type, ticket);
      
      //--- print all the real properties of the selected position under the header
      PositionPropertiesDoublePrint(15);
     }
   /*
   result:
   Double properties of an open position Buy #2807075208:
   Volume:        1.00
   Price open:    1.10516
   StopLoss:      0.00000
   TakeProfit:    0.00000
   Price current: 1.10518
   Swap:          0.00
   Profit:        2.00 USD
   */
  }
//+------------------------------------------------------------------+
//| Display real properties of the selected position in the journal  |
//+------------------------------------------------------------------+
void PositionPropertiesDoublePrint(const uint header_width=0)
  {
   uint   w=0;
   string header="";
   double value=0;
   
//--- get the account currency, position symbol and the number of decimal places for the symbol
   string currency=AccountInfoString(ACCOUNT_CURRENCY);
   string symbol  =PositionGetString(POSITION_SYMBOL);
   int    digits  =(int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   
//--- define the header text and the width of the header field
//--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
   header="Volume:";
   w=(header_width==0 ? header.Length()+1 : header_width);
//--- get and display the position volume with the specified header width in the journal
   if(!PositionGetDouble(POSITION_VOLUME, value))
      return;
   PrintFormat("%-*s%-.2f", w, header, value);
   
//--- display the position price value in the journal
   header="Price open:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!PositionGetDouble(POSITION_PRICE_OPEN, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
   
//--- display the StopLoss value in the journal
   header="StopLoss:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!PositionGetDouble(POSITION_SL, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
   
//--- display the TakeProfit value in the journal
   header="TakeProfit:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!PositionGetDouble(POSITION_TP, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
 
//--- display the 'Price current' value in the journal
   header="Price current:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!PositionGetDouble(POSITION_PRICE_CURRENT, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
 
//--- display the accumulated swap value in the journal
   header="Swap:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!PositionGetDouble(POSITION_SWAP, value))
      return;
   PrintFormat("%-*s%-.2f", w, header, value);
 
//--- display the current profit value to the journal
   header="Profit:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!PositionGetDouble(POSITION_PROFIT, value))
      return;
   PrintFormat("%-*s%-.2f %s", w, header, value, currency);
  }

```

See also

[PositionGetSymbol()](/en/docs/trading/positiongetsymbol), [PositionSelect()](/en/docs/trading/positionselect), [Position Properties](/en/docs/constants/tradingconstants/positionproperties)
