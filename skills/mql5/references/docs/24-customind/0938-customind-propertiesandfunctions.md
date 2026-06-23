# Connection between Indicator Properties and Corresponding Functions

Every custom indicator has numerous [properties](/en/docs/basis/preprosessor/compilation), some of which are obligatory and are always positioned at the beginning of description. They are the following properties:

- indication of a window to plot the indicator – indicator_separate_window or indicator_chart_window;
- number of indicator buffers – indicator_buffers;
- number of plots of the indicator – indicator_plots.

Also there are other properties that can be set both through [preprocessor](/en/docs/basis/preprosessor) directives and through functions intended for custom indicator creation. These properties and corresponding functions are described in the following table.

| Directives for properties of indicator subwindow | Functions of IndicatorSet...() type | Description of the adjusted property of the subwindow |
| --- | --- | --- |
| indicator_height | IndicatorSetInteger ( INDICATOR_INDICATOR_HEIGHT , nHeight) | The fixed value of the subwindow height |
| indicator_minimum | IndicatorSetDouble ( INDICATOR_MINIMUM , dMaxValue) | Minimal value of the vertical axis |
| indicator_maximum | IndicatorSetDouble ( INDICATOR_MAXIMUM , dMinValue) | Maximal value of the vertical axis |
| indicator_levelN | IndicatorSetDouble ( INDICATOR_LEVELVALUE , N-1, nLevelValue) | Vertical axis value for N level |
| no preprocessor directive | IndicatorSetString ( INDICATOR_LEVELTEXT , N-1, sLevelName) | Name of a displayed level |
| indicator_levelcolor | IndicatorSetInteger ( INDICATOR_LEVELCOLOR , N-1, nLevelColor) | Color of N level |
| indicator_levelwidth | IndicatorSetInteger ( INDICATOR_LEVELWIDTH , N-1, nLevelWidth) | Line width for N level |
| indicator_levelstyle | IndicatorSetInteger ( INDICATOR_LEVELSTYLE , N-1, nLevelStyle) | Line style for N level |
| Directives for plotting properties | Functions of PlotIndexSet...() type | Description of the adjusted property of a plot |
| indicator_labelN | PlotIndexSetString (N-1, PLOT_LABEL ,sLabel) | Short name of the number N plot. It is displayed in DataWindow and in the pop-up tooltip when pointing the mouse cursor over it |
| indicator_colorN | PlotIndexSetInteger (N-1,  PLOT_LINE_COLOR , nColor) | Line color for N plot |
| indicator_styleN | PlotIndexSetInteger (N-1,  PLOT_LINE_STYLE , nType) | Line style for N plot |
| indicator_typeN | PlotIndexSetInteger (N-1,  PLOT_DRAW_TYPE , nType) | Line type for N plot |
| indicator_widthN | PlotIndexSetInteger (N-1,  PLOT_LINE_WIDTH , nWidth) | Line width for N plot |
| Common indicator properties | Functions of IndicatorSet...() type | Description |
| no preprocessor directive | IndicatorSetString ( INDICATOR_SHORTNAME , sShortName) | Sets the convenient short name of the indicator that will be displayed in the list of indicators (opened in the terminal by pressing  Ctrl+I ). |
| no preprocessor directive | IndicatorSetInteger ( INDICATOR_DIGITS , nDigits) | Sets required accuracy of display of indicator values - number of decimal places |
| no preprocessor directive | IndicatorSetInteger ( INDICATOR_LEVELS , nLevels) | Sets number of levels in the indicator window |
| indicator_applied_price | No function, the property can be set only by the preprocessor directive. | Default price type used for the indicator calculation. It is specified when necessary, only if OnCalculate() of the first type is used. 
 The property value can also be set from the dialog of indicator properties in the "Parameters" tab -  "Apply to" . |

It should be noted that numeration of levels and plots in preprocessor terms starts with one, while numeration of the same properties at using functions starts with zero, i.e. the indicated value must be by 1 less than that indicated for #property.

There are several directives, for which there are no corresponding functions:

| Directive | Description |
| --- | --- |
| indicator_chart_window | Indicator is displayed in the main window |
| indicator_separate_window | Indicator is displayed in a separate subwindow |
| indicator_buffers | Number of required indicator buffers |
| indicator_plots | Number of  plots  in the indicator |
