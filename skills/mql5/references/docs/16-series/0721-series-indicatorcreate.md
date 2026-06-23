# IndicatorCreate

The function returns the handle of a specified technical indicator created based on the array of parameters of [MqlParam](/en/docs/constants/structures/mqlparam) type.

```
int  IndicatorCreate(
   string           symbol,                            // symbol name
   ENUM_TIMEFRAMES  period,                            // timeframe
   ENUM_INDICATOR   indicator_type,                    // indicator type from the enumeration ENUM_INDICATOR
   int              parameters_cnt=0,                  // number of parameters
   const MqlParam&  parameters_array[]=NULL,           // array of parameters
   );

```

Parameters

symbol

[in] Name of a symbol, on data of which the indicator is calculated. [NULL](/en/docs/basis/types/void) means the current symbol.

period

[in]  The value of the timeframe can be one of values of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration, 0 means the current timeframe.

indicator_type

[in]  Indicator type, can be one of values of the [ENUM_INDICATOR](/en/docs/constants/indicatorconstants/enum_indicator) enumeration.

parameters_cnt

[in] The number of parameters passed in the parameters_array[] array. The array elements have a special structure type [MqlParam](/en/docs/constants/structures/mqlparam). By default, zero - parameters are not passed. If you specify a non-zero number of parameters, the parameter parameters_array is obligatory. You can pass no more than 64 parameters.

parameters_array[]=NULL

[in]  An array of MqlParam type, whose elements contain the type and value of each input parameter of a [technical indicator](/en/docs/indicators).

Return Value

Returns the handle of a specified technical indicator,  in case of failure returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants).

Note

If the indicator handle of IND_CUSTOM type is created, the type field of the first element of the array of input parameters parameters_array must have the TYPE_STRING value of the  [ENUM_DATATYPE](/en/docs/constants/indicatorconstants/enum_datatype) enumeration, and the string_value field of the first element must contain the name of the custom indicator. The custom indicator must be compiled (file with EX5 extension) and located in the directory MQL5/Indicators of the client terminal or in a subdirectory.

Indicators that require testing are defined automatically from the call of the iCustom() function, if the corresponding parameter is set through a [constant string](/en/docs/basis/types/stringconst). For all other cases (use of the [IndicatorCreate()](/en/docs/series/indicatorcreate) function or use of a non-constant string in the parameter that sets the indicator name) the property [#property tester_indicator](/en/docs/basis/preprosessor/compilation) is required:

```
#property tester_indicator "indicator_name.ex5"

```

If [the first form of the call](/en/docs/event_handlers/oncalculate) is used in a custom indicator, you can additionally indicate as the last parameter on what data it will be calculated when passing input parameters. If the "Apply to" parameter is not specified explicitly, the default calculation is based on the [PRICE_CLOSE](/en/docs/constants/indicatorconstants/prices#enum_applied_price_enum) values.

Example:

```
void OnStart()
  {
   MqlParam params[];
   int      h_MA,h_MACD;
//--- create iMA("EURUSD",PERIOD_M15,8,0,MODE_EMA,PRICE_CLOSE);
   ArrayResize(params,4);
//--- set ma_period
   params[0].type         =TYPE_INT;
   params[0].integer_value=8;
//--- set ma_shift
   params[1].type         =TYPE_INT;
   params[1].integer_value=0;
//--- set ma_method
   params[2].type         =TYPE_INT;
   params[2].integer_value=MODE_EMA;
//--- set applied_price
   params[3].type         =TYPE_INT;
   params[3].integer_value=PRICE_CLOSE;
//--- create MA
   h_MA=IndicatorCreate("EURUSD",PERIOD_M15,IND_MA,4,params);
//--- create iMACD("EURUSD",PERIOD_M15,12,26,9,h_MA);
   ArrayResize(params,4);
//--- set fast ma_period
   params[0].type         =TYPE_INT;
   params[0].integer_value=12;
//--- set slow ma_period
   params[1].type         =TYPE_INT;
   params[1].integer_value=26;
//--- set smooth period for difference
   params[2].type         =TYPE_INT;
   params[2].integer_value=9;
//--- set indicator handle as applied_price
   params[3].type         =TYPE_INT;
   params[3].integer_value=h_MA;
//--- create MACD based on moving average
   h_MACD=IndicatorCreate("EURUSD",PERIOD_M15,IND_MACD,4,params);
//--- use indicators
//--- . . .
//--- release indicators (first h_MACD)
   IndicatorRelease(h_MACD);
   IndicatorRelease(h_MA);
  }

```
