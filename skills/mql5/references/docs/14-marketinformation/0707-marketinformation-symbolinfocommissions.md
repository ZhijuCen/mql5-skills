# SymbolInfoCommissions

Returns commission charging rules for the specified financial instrument.

```
int  SymbolInfoCommissions(
   string           name,              // symbol name
   MqlCommission&   commissions[]      // array of commission rules
   );

```

Parameters

name

[in]  Symbol name. If the parameter is [NULL](/en/docs/basis/types/void), the current symbol is used.

commissions

[out]  Dynamic array of [MqlCommission](/en/docs/marketinformation/symbolinfocommissions#mqlcommission) structures, to which commission charging rules for the specified symbol are written.

Return Value

If successful, the function returns the number of elements written to commissions.

In case of an error, -1 is returned. To obtain information about the error, use [GetLastError()](/en/docs/check/getlasterror).

Note

Each element of the commissions array describes a separate commission charging rule. The general conditions for applying the commission are set by the fields of the MqlCommission structure, while specific commission values and ranges are defined in tiers.

If no commission rules are specified for the symbol, the function returns 0.

If name specifies the name of a nonexistent or unavailable symbol, the function returns -1.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare a dynamic array for receiving commission charging rules
   MqlCommission commissions[];
 
//--- get commission rules for the current symbol.
//--- if a symbol name is specified instead of NULL, the function returns commissions for that symbol.
   int total=SymbolInfoCommissions(NULL,commissions);
 
//--- check the function execution result
   if(total<0)
     {
      //--- in case of an error, print the error code
      PrintFormat("SymbolInfoCommissions failed. Error %d",GetLastError());
      return;
     }
 
//--- print the number of received commission rules
   PrintFormat("Commission rules: %d",total);
 
//--- iterate over all commission rules
   for(int i=0;i<total;i++)
     {
      //--- print the main parameters of the commission rule:
      //--- currency, range selection mode and charge mode
      PrintFormat("Rule %d: currency=%s, range mode=%d, charge mode=%d",
                  i,
                  commissions[i].currency,
                  commissions[i].mode_range,
                  commissions[i].mode_charge);
 
      //--- get the number of commission tiers in the current rule
      int tiers_total=ArraySize(commissions[i].tiers);
 
      //--- iterate over commission tiers
      for(int j=0;j<tiers_total;j++)
        {
         //--- print commission tier parameters:
         //--- calculation mode, value, applicable range and currency
         PrintFormat("  Tier %d: mode=%d, value=%G, range=%G - %G, currency=%s",
                     j,
                     commissions[i].tiers[j].mode,
                     commissions[i].tiers[j].value,
                     commissions[i].tiers[j].range_from,
                     commissions[i].tiers[j].range_to,
                     commissions[i].tiers[j].currency);
        }
     }
  }

```

### Symbol Commissions

This section describes enumerations and structures used to represent commission charging rules for a financial instrument.

Commission can be specified as a money amount, points, percent, percent of profit, and can also be calculated by volume, turnover, deal value or profit ranges. A single commission rule can contain multiple tiers, MqlCommissionTier.

ENUM_SYMBOL_COMMISSION_MODE

The ENUM_SYMBOL_COMMISSION_MODE enumeration defines the commission calculation method.

| Identifier | Description |
| --- | --- |
| SYMBOL_COMMISSION_DISABLED | Commission is disabled. |
| SYMBOL_COMMISSION_MONEY_DEPOSIT | Commission is specified in the deposit currency of the trading group/account. |
| SYMBOL_COMMISSION_MONEY_SYMBOL_BASE | Commission is specified in the base currency of the financial instrument. |
| SYMBOL_COMMISSION_MONEY_SYMBOL_PROFIT | Commission is specified in the profit currency of the financial instrument. |
| SYMBOL_COMMISSION_MONEY_SYMBOL_MARGIN | Commission is specified in the margin currency of the financial instrument. |
| SYMBOL_COMMISSION_PIPS | Commission is specified in points. |
| SYMBOL_COMMISSION_PERCENT | Commission is specified as a percentage. |
| SYMBOL_COMMISSION_MONEY_SPECIFIED | Commission is specified in the specified currency. The currency is specified in the corresponding field of the commission structure or commission tier. |
| SYMBOL_COMMISSION_PERCENT_PROFIT | Commission is specified as a percentage of profit. |

ENUM_SYMBOL_COMMISSION_VOLUME_TYPE

The ENUM_SYMBOL_COMMISSION_VOLUME_TYPE enumeration defines how the commission value is applied to a trade operation.

| Identifier | Description |
| --- | --- |
| SYMBOL_COMMISSION_VOLUME_TYPE_TRADE | Commission is charged per deal. |
| SYMBOL_COMMISSION_VOLUME_TYPE_VOLUME | Commission is calculated proportionally to the deal volume. |
| SYMBOL_COMMISSION_VOLUME_TYPE_TURNOVER | Commission is calculated by turnover. |

ENUM_SYMBOL_COMMISSION_RANGE_MODE

The ENUM_SYMBOL_COMMISSION_RANGE_MODE enumeration defines the indicator used to select the commission range.

| Identifier | Description |
| --- | --- |
| SYMBOL_COMMISSION_RANGE_VOLUME | The range is determined by the deal volume. |
| SYMBOL_COMMISSION_RANGE_TURNOVER_MONEY | The range is determined by money turnover. |
| SYMBOL_COMMISSION_RANGE_TURNOVER_VOLUME | The range is determined by volume turnover. |
| SYMBOL_COMMISSION_RANGE_VALUE | The range is determined by deal value. |
| SYMBOL_COMMISSION_RANGE_PROFIT | The range is determined by profit. |

ENUM_SYMBOL_COMMISSION_CHARGE_MODE

The ENUM_SYMBOL_COMMISSION_CHARGE_MODE enumeration defines when commission is charged.

| Identifier | Description |
| --- | --- |
| SYMBOL_COMMISSION_CHARGE_DAILY | Commission is charged at the end of the day. |
| SYMBOL_COMMISSION_CHARGE_MONTHLY | Commission is charged at the end of the month. |
| SYMBOL_COMMISSION_CHARGE_INSTANT | Commission is charged immediately when the deal is executed. |

ENUM_SYMBOL_COMMISSION_ENTRY_MODE

The ENUM_SYMBOL_COMMISSION_ENTRY_MODE enumeration defines at which stage of a trade operation commission is charged.

| Identifier | Description |
| --- | --- |
| SYMBOL_COMMISSION_ENTRY_INOUT | Commission is charged when entering and exiting a position. |
| SYMBOL_COMMISSION_ENTRY_IN | Commission is charged when entering a position. |
| SYMBOL_COMMISSION_ENTRY_OUT | Commission is charged when exiting a position. |

ENUM_SYMBOL_COMMISSION_DIRECTION_MODE

The ENUM_SYMBOL_COMMISSION_DIRECTION_MODE enumeration defines the direction of deals to which commission applies.

| Identifier | Description |
| --- | --- |
| SYMBOL_COMMISSION_DIRECTION_BOTH | Commission applies to buy and sell deals. |
| SYMBOL_COMMISSION_DIRECTION_BUY | Commission applies only to buy deals. |
| SYMBOL_COMMISSION_DIRECTION_SELL | Commission applies only to sell deals. |

ENUM_SYMBOL_COMMISSION_PROFIT_MODE

The ENUM_SYMBOL_COMMISSION_PROFIT_MODE enumeration defines whether commission is applied depending on the financial result of the deal.

| Identifier | Description |
| --- | --- |
| SYMBOL_COMMISSION_PROFIT_ALL | Commission applies to all deals. |
| SYMBOL_COMMISSION_PROFIT_PROFIT | Commission applies only to profitable deals. |
| SYMBOL_COMMISSION_PROFIT_LOSS | Commission applies only to losing deals. |

MqlCommissionTier

The MqlCommissionTier structure describes one commission tier.

```
struct MqlCommissionTier
  {
   ENUM_SYMBOL_COMMISSION_MODE           mode;
   ENUM_SYMBOL_COMMISSION_VOLUME_TYPE    volume_type;
   double                                value;
   double                                min_value;
   double                                max_value;
   double                                range_from;
   double                                range_to;
   string                                currency;
  };

```

Field Description

| Field | Type | Description |
| --- | --- | --- |
| mode | ENUM_SYMBOL_COMMISSION_MODE | Commission calculation method for this tier. |
| volume_type | ENUM_SYMBOL_COMMISSION_VOLUME_TYPE | Method for applying the commission value: per deal, by volume or by turnover. |
| value | double | Commission value. Interpretation of the value depends on the mode field: money amount, number of points, percentage or percentage of profit. |
| min_value | double | Minimum commission value for this tier. |
| max_value | double | Maximum commission value for this tier. |
| range_from | double | Lower bound of the range to which this commission tier applies. |
| range_to | double | Upper bound of the range to which this commission tier applies. |
| currency | string | Commission currency. Used for modes in which commission is specified in an explicitly set currency, for example SYMBOL_COMMISSION_MONEY_SPECIFIED. |

Note

The commission tier range is determined by the range_from and range_to. The indicator used to select the range is specified in the mode_range field of the MqlCommission structure.

If commission is disabled using SYMBOL_COMMISSION_DISABLED, the other tier parameters are not used for commission charging.

MqlCommission

The MqlCommission structure describes a commission charging rule for a financial instrument.

```
struct MqlCommission
  {
   string                                   currency;
   ENUM_SYMBOL_COMMISSION_RANGE_MODE        mode_range;
   ENUM_SYMBOL_COMMISSION_CHARGE_MODE       mode_charge;
   ENUM_SYMBOL_COMMISSION_ENTRY_MODE        mode_entry;
   ENUM_SYMBOL_COMMISSION_DIRECTION_MODE    mode_direction;
   ENUM_SYMBOL_COMMISSION_PROFIT_MODE       mode_profit;
   MqlCommissionTier                        tiers[];
  };

```

Field Description

| Field | Type | Description |
| --- | --- | --- |
| currency | string | Currency specified for the commission rule. Used when calculating commission in modes that require an explicitly set currency. |
| mode_range | ENUM_SYMBOL_COMMISSION_RANGE_MODE | Indicator used to select the commission range: volume, money turnover, volume turnover, deal value or profit. |
| mode_charge | ENUM_SYMBOL_COMMISSION_CHARGE_MODE | Commission charging time: at the end of the day, at the end of the month or immediately when the deal is executed. |
| mode_entry | ENUM_SYMBOL_COMMISSION_ENTRY_MODE | Stage of the trade operation at which commission is charged: entry, exit, or entry and exit. |
| mode_direction | ENUM_SYMBOL_COMMISSION_DIRECTION_MODE | Direction of deals to which commission applies: buy, sell or both directions. |
| mode_profit | ENUM_SYMBOL_COMMISSION_PROFIT_MODE | Condition for applying commission depending on the financial result of the deal. |
| tiers | MqlCommissionTier[] | Dynamic array of commission tiers. Each array element describes a separate range and commission calculation parameters for that range. |

Note

The MqlCommission structure sets the general conditions for applying commission, while the tiers array contains commission tiers with specific values and ranges.

When calculating commission, the general rule conditions are checked first: deal direction, entry or exit stage, financial result, charging time and charging reason. Then, based on the mode_range value, the appropriate tier is selected from the tiers array.

If the tiers array is empty, no commission tiers are specified for this rule.

See also

[SymbolsTotal](/en/docs/marketinformation/symbolstotal), [SymbolSelect](/en/docs/marketinformation/symbolselect), [SymbolInfoMarginRate](/en/docs/marketinformation/symbolinfomarginrate)
