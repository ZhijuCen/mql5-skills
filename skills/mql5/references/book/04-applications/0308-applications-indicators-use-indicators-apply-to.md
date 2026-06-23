# Defining data source for an indicator

Among the MQL program [built-in variables](/en/book/common/environment/env_variables), there is one that can only be used in indicators. This is the _AppliedTo variable of type int, which allows you to read the Apply to property from the indicator settings dialog. In addition, if the indicator is created by calling the iCustom function, to which the handle of the third-party indicator was passed, then the _AppliedTo variable will contain this handle.

The following table describes the possible values for the _AppliedTo variable.

| Value | Description of data for calculation |
| --- | --- |
| 0 | The indicator uses the full form of  OnCalculate , and the data for the calculation is not set by one data array |
| 1 | Close Price |
| 2 | Open price |
| 3 | High Price |
| 4 | Low price |
| 5 | Average Price = (High+Low)/2 |
| 6 | Typical Price = (High+Low+Close)/3 |
| 7 | Weighted Price = (Open+High+Low+Close)/4 |
| 8 | Data of the indicator that was launched on the chart before this indicator |
| 9 | Data of the indicator that was launched on the chart the very first |
| 10+ | Data of indicator with the handle contained in  _AppliedTo;  this handle was passed as a last parameter to the  iCustom  function when creating the indicator |

For the convenience of analyzing the values, attached to this book is a header file AppliedTo.mqh with the enumeration.
