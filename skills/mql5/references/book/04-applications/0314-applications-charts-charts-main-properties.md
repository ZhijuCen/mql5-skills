# Functions for getting the basic properties of the current chart

In many examples in the book, we have already had to use [Predefined Variables](/en/book/common/environment/env_variables), containing the main properties of the chart and its working symbol. MQL programs also have access to functions that return the values of some of these variables. It does not matter what is used, a variable or a function, and thus you can use your preferred source code styles.

Each chart is characterized by a working symbol and timeframe. They can be found using the Symbol and Period functions, respectively. In addition, MQL5 provides simplified access to the two most commonly used symbol properties: price point size (Point) and the associated number of significant digits (Digits) after the decimal point in the price.

string Symbol()

The Symbol function returns the symbol name of the current chart, i.e. the value of the system variable _Symbol. To get the symbol of an arbitrary chart, there is the [ChartSymbol](/en/book/applications/charts/charts_symbol_period) function which operates based on the chart identifier. We will discuss the methods for obtaining chart identifiers a little later.

ENUM_TIMEFRAMES Period()

The Period function returns the timeframe value ([ENUM_TIMEFRAMES](/en/book/applications/timeseries/timeseries_symbol_period)) of the current chart, which corresponds to the _Period variable. To get the timeframe of an arbitrary chart, use the function [ChartPeriod](/en/book/applications/charts/charts_symbol_period), and it also needs an identifier as a parameter.

double Point()

The Point function returns the point size of the current instrument in the quote currency, which is the same as the value of the _Point variable.

int Digits()

The function returns the number of decimal places after the decimal point, which determines the accuracy of measuring the price of the symbol of the current chart, which is equivalent to the variable _Digits.

Other properties of the current tool allow you to get [SymbolInfo](/en/book/automation/symbols/symbols_info)[-functions](/en/book/automation/symbols/symbols_info), which in a more general case provide an analysis of all instruments.

The following simple example of the script ChartMainProperties.mq5 logs the properties described in this section.

```
void OnStart()
{
   PRTF(_Symbol);
   PRTF(Symbol());
   PRTF(_Period);
   PRTF(Period());
   PRTF(_Point);
   PRTF(Point());
   PRTF(_Digits);
   PRTF(Digits());
   PRTF(DoubleToString(_Point, _Digits));
   PRTF(EnumToString(_Period));
}

```

For the EURUSD,H1 chart, we will get the following log entries.

```
_Symbol=EURUSD / ok
Symbol()=EURUSD / ok
_Period=16385 / ok
Period()=16385 / ok
_Point=1e-05 / ok
Point()=1e-05 / ok
_Digits=5 / ok
Digits()=5 / ok
DoubleToString(_Point,_Digits)=0.00001 / ok
EnumToString(_Period)=PERIOD_H1 / ok

```
