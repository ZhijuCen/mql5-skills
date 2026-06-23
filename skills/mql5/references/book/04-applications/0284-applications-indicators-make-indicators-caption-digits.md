# General properties of indicators: title and value accuracy

For all indicators, a couple of important properties are supported that are not related to calculations but improve the user experience. Their correct setting in the OnInit handler became part of the indicator development standard.

The integer property INDICATOR_DIGITS is set using the previously discussed function IndicatorSetInteger and affects the accuracy of the representation of real numbers on the graph and in the Data Window. By default, the terminal outputs 6 digits after the decimal point. If the indicator readings are related to the price of the current instrument, then it makes sense to set this property equal to the accuracy of the price representation: IndicatorSetInteger(INDICATOR_DIGITS, _Digits).

In the case of WPR, the values are analogous to percentages, and therefore it makes sense to limit the displayed values to two decimal places.

```
   IndicatorSetInteger(INDICATOR_DIGITS, 2);

```

The second commonly used property is the string INDICATOR_SHORTNAME — it uses the IndicatorSetString function. This is the title of the indicator displayed in tooltips and also in the upper left corner of the subwindow if the indicator has its own window. When not explicitly specified, the indicator file name is used. In particular, in the screenshot in the previous section, we see the title IndWPR.

It is customary to display the main input variables and operating modes (if there are several of them) in the indicator header.

For example, for WPR, as a rule, the period selected by the user is included in the title.

In addition, the title allows you to shorten the name. This is important because the title is limited to 63 characters.

For the updated version of WPR, we will use the following setting:

```
   IndicatorSetString(INDICATOR_SHORTNAME, "%R" + "(" + (string)WPRPeriod + ")");

```

We will check the results of these improvements in the next section after we color the overbought and oversold zones in different colors (see the example IndColorWPR.mq5).
