# Overview of functions for working with the complete set of chart properties

Chart properties are readable and editable via groups ChartSet- and ChartGet-functions, each of which contains properties of a certain type: real numbers (double), whole numbers (long, int, datetime, color, bool, enums), and strings.

All functions receive the chart ID as the first parameter. The value 0 means the current chart, that is, it is equivalent to passing the result of the call ChartID(). However, this does not mean that the ID of the current chart is 0.

The constants describing all properties form three enumerations ENUM_CHART_PROPERTY_INTEGER, ENUM_CHART_PROPERTY_DOUBLE, ENUM_CHART_PROPERTY_STRING, which are used as function parameters for the corresponding type. A summary table of all properties can be found in the MQL5 documentation, on the page about [chart properties](https://www.mql5.com/ru/docs/constants/chartconstants/enum_chart_property). In the following sections of this chapter, we will gradually cover virtually all the properties, grouping them according to their purpose. The only exception is the properties of managing events on the chart - we will describe them in the [relevant section](/en/book/applications/events/events_properties) of the chapter on events.

The elements of all three enumerations are assigned such values that they form a single list without intersections (repetitions). This allows you to determine the type of enumeration by a specific value. For example, given a constant, we can consistently try to convert it to a string with the name of one of the enums until we succeed.

```
int value = ...;
   
ResetLastError(); // clear the error code if there was one
EnumToString((ENUM_CHART_PROPERTY_INTEGER)value); // resulting string is not important
if(_LastError == 0) // analyze if there is a new error
{
   // success is an element of ENUM_CHART_PROPERTY_INTEGER
   return ChartGetInteger(0, (ENUM_CHART_PROPERTY_INTEGER)value);
}
   
ResetLastError();
EnumToString((ENUM_CHART_PROPERTY_DOUBLE)value);
if(_LastError == 0)
{
   // success is an ENUM_CHART_PROPERTY_DOUBLE element
   return ChartGetDouble(0, (ENUM_CHART_PROPERTY_DOUBLE)value);
}
   
... // continue a similar check for ENUM_CHART_PROPERTY_STRING

```

Later we will use this approach in test scripts.

Some properties (for example, the number of visible bars) are read-only and cannot be changed. They will be further marked "r/o" (read-only).

Property read functions have a short form and a long form: the short form directly returns the requested value, and the long form returns a boolean attribute of success (true) or error (false), while the value itself is placed in the last parameter passed by reference. When using the short form, it is especially important to check the error code in the _LastError variable, because the value 0 (NULL) returned in case of problems may be generally correct.

When accessing some properties, you must specify an additional parameter window, which is used to indicate the chart window/subwindow. 0 means the main window. Subwindows are numbered starting from 1. Some properties apply to the chart as a whole and thus they have function variants without the window parameter.

Following are the function prototypes for reading and writing integer properties. Please note that the type of values in them is long.

bool ChartSetInteger(long chartId, ENUM_CHART_PROPERTY_INTEGER property, long value)

bool ChartSetInteger(long chartId, ENUM_CHART_PROPERTY_INTEGER property, int window, long value)

long ChartGetInteger(long chartId, ENUM_CHART_PROPERTY_INTEGER property, int window = 0)

bool ChartGetInteger(long chartId, ENUM_CHART_PROPERTY_INTEGER property, int window, long &value)

Functions for real properties are described similarly. There are no writable real properties for subwindows, so there is only one form of ChartSetDouble, which is without the window parameter.

bool ChartSetDouble(long chartId, ENUM_CHART_PROPERTY_DOUBLE property, double value)

double ChartGetDouble(long chartId, ENUM_CHART_PROPERTY_DOUBLE property, int window = 0)

bool ChartGetDouble(long chartId, ENUM_CHART_PROPERTY_DOUBLE property, int window, double &value)

The same applies to string properties, but one more nuance should be taken into account: the length of the string cannot exceed 2045 characters (extra characters will be cut off).

bool ChartSetString(long chartId, ENUM_CHART_PROPERTY_STRING property, string value)

string ChartGetString(long chartId, ENUM_CHART_PROPERTY_STRING property)

bool ChartGetString(long chartId, ENUM_CHART_PROPERTY_STRING property, string &value)

When reading properties using the short form of ChartGetInteger/ChartGetDouble, the window parameter is optional and defaults to the main window (window=0).

Functions for setting chart properties (ChartSetInteger, ChartSetDouble, ChartSetString) are asynchronous and serve to send change commands to the chart. If these functions are successfully executed, the command is added to the common queue of chart events, and true is returned. When an error occurs, the function returns false. In this case, you should check the error code in the _LastError variable.

Chart properties are changed later, during the processing of the event queue of this chart, and, as a rule, with some delay, so you should not expect an immediate update of the chart after applying new settings. To force the update of the appearance and properties of the chart, use the function [ChartRedraw](/en/book/applications/charts/charts_redraw). If you want to change several chart properties at once, then you need to call the corresponding functions in one code block and then once in ChartRedraw.

In general, the chart is updated automatically by the terminal in response to events such as the arrival of a new quote, changes in the chart window size, scaling, scrolling, adding an indicator, etc.

Functions for getting chart properties (ChartGetInteger, ChartGetDouble, ChartGetString) are synchronous, that is, the calling code waits for the result of their execution.
