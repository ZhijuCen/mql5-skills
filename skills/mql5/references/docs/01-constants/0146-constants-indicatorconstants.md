# Indicators Constants

There are 37 predefined [technical indicators](/en/docs/indicators), which can be used in programs written in the MQL5 language. In addition, there is an opportunity to create custom indicators using the [iCustom()](/en/docs/indicators/icustom) function. All constants required for that are divided into 5 groups:

- [Price constants](/en/docs/constants/indicatorconstants/prices) – for selecting the type of price or volume, on which an indicator is calculated;
- [Smoothing methods](/en/docs/constants/indicatorconstants/enum_ma_method) – built-in smoothing methods used in indicators;
- [Indicator lines](/en/docs/constants/indicatorconstants/lines) – identifiers of indicator buffers when accessing indicator values using [CopyBuffer()](/en/docs/series/copybuffer);
- [Drawing styles](/en/docs/constants/indicatorconstants/drawstyles) – for indicating one of 18 types of drawing and setting the line drawing style;
- [Custom indicators properties](/en/docs/constants/indicatorconstants/customindicatorproperties) are used in functions for working with [custom](/en/docs/customind) indicators;
- [Types of indicators](/en/docs/constants/indicatorconstants/enum_indicator) are used for specifying the type of technical indicator when creating a handle using [IndicatorCreate()](/en/docs/series/indicatorcreate);
- [Identifiers of data types](/en/docs/constants/indicatorconstants/enum_datatype) are used for specifying the type of data passed in an array of the [MqlParam](/en/docs/constants/structures/mqlparam) type into the [IndicatorCreate()](/en/docs/series/indicatorcreate) function.
