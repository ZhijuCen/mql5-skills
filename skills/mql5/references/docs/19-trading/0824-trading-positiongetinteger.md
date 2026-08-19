# PositionGetInteger

The function returns the requested property of an open position, pre-selected using [PositionGetSymbol](/en/docs/trading/positiongetsymbol) or [PositionSelect](/en/docs/trading/positionselect). The position property should be of datetime, int type. There are 2 variants of the function.

1. Immediately returns the property value.

```
long  PositionGetInteger(
   ENUM_POSITION_PROPERTY_INTEGER  property_id      // Property identifier
   );

```

2. Returns true or false, depending on the success of the function execution. If successful, the value of the property is placed in a receiving variables passed by reference by the last parameter.

```
bool  PositionGetInteger(
   ENUM_POSITION_PROPERTY_INTEGER  property_id,     // Property identifier
   long&                           long_var         // Here we accept the property value
   );

```

Parameters

property_id

[in]  Identifier of a position property. The value can be one of the values of the [ENUM_POSITION_PROPERTY_INTEGER](/en/docs/constants/tradingconstants/positionproperties#enum_position_property_integer) enumeration.

long_var

[out]  Variable of the long type accepting the value of the requested property.

Return Value

Value of the [long](/en/docs/basis/types/integer/integertypes#long) type. If the function fails, 0 is returned.

Note

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol.

To ensure receipt of fresh data about a position, it is recommended to call [PositionSelect()](/en/docs/trading/positionselect) right before referring to them.

Example:

```
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
//--- check if a position is present and display the time of its changing
   if(PositionSelect(_Symbol))
     {     
//--- receive position ID for further work
      ulong position_ID=PositionGetInteger(POSITION_IDENTIFIER);
      Print(_Symbol," position #",position_ID);
//--- receive the time of position forming in milliseconds since 01.01.1970
      long create_time_msc=PositionGetInteger(POSITION_TIME_MSC);
      PrintFormat("Position #%d  POSITION_TIME_MSC = %i64 milliseconds => %s",position_ID,
                  create_time_msc,TimeToString(create_time_msc/1000));
//--- receive the time of the position's last change in seconds since 01.01.1970
      long update_time_sec=PositionGetInteger(POSITION_TIME_UPDATE);
      PrintFormat("Position #%d  POSITION_TIME_UPDATE = %i64 seconds => %s",
                  position_ID,update_time_sec,TimeToString(update_time_sec));
//--- receive the time of the position's last change in milliseconds since 01.01.1970
      long update_time_msc=PositionGetInteger(POSITION_TIME_UPDATE_MSC);
      PrintFormat("Position #%d  POSITION_TIME_UPDATE_MSC = %i64 milliseconds => %s",
                  position_ID,update_time_msc,TimeToString(update_time_msc/1000));
     }
//---
  }

```

See also

[PositionGetSymbol()](/en/docs/trading/positiongetsymbol), [PositionSelect()](/en/docs/trading/positionselect), [Position Properties](/en/docs/constants/tradingconstants/positionproperties)
