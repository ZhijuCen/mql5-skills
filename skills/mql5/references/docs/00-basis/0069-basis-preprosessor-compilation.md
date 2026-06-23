# Program Properties (#property)

Every mql5-program allows to specify additional specific parameters named #property that help client terminal in proper servicing for programs without the necessity to launch them explicitly. This concerns external settings of indicators, first of all. Properties described in included files are completely ignored. Properties must be specified in the main mq5-file.

```
#property identifier value

```

The compiler will write declared values in the configuration of the module executed.

| Constant | Type | Description |
| --- | --- | --- |
| icon | string | Path to the file of an image that will be used as an icon of the EX5 program. Path specification rules are the same as for  resources . The property must be specified in the main module with the MQL5 source code. The icon file must be in the  ICO  format. |
| link | string | Link to the company website |
| copyright | string | The company name |
| version | string | Program version, maximum 31 characters |
| description | string | Brief text description of a mql5-program. Several  description  can be present, each of them describes one line of the text. The total length of all  description  can not exceed 511 characters including line feed. |
| stacksize | int | MQL5 program  stack  size. The stack of sufficient size is necessary when executing function recursive calls. 
 When launching a script or an Expert Advisor on the chart, the stack of at least 8 MB is allocated. In case of indicators, the stack size is always fixed and equal to 1 MB. 
 When a program is launched in the strategy tester, the stack of 16 MB is always allocated for it. |
| library |  | A library; no start function is assigned, functions with  the export modifier  can be  imported  in other mql5-programs |
| indicator_applied_price | int | Specifies the default value for the  "Apply to"  field. You can specify one of the values of  ENUM_APPLIED_PRICE . If the property is not specified, the default value is PRICE_CLOSE |
| indicator_chart_window |  | Show the indicator in the chart window |
| indicator_separate_window |  | Show the indicator in a separate window |
| indicator_height | int | Fixed height of the indicator subwindow in pixels (property  INDICATOR_HEIGHT ) |
| indicator_buffers | int | Number of buffers for indicator calculation |
| indicator_plots | int | Number of  graphic series  in the indicator |
| indicator_minimum | double | The bottom scaling limit for a separate indicator window |
| indicator_maximum | double | The top scaling limit for a separate indicator window |
| indicator_labelN | string | Sets a label for the N-th  graphic series  displayed in DataWindow. For graphic series requiring multiple indicator buffers (DRAW_CANDLES, DRAW_FILLING and others), the label names are defined using the separator ';'. |
| indicator_colorN | color | The color for displaying line N, where N is the number of  graphic series ; numbering starts from 1 |
| indicator_widthN | int | Line thickness in  graphic series , where N is the number of graphic series; numbering starts from 1 |
| indicator_styleN | int | Line style in  graphic series , specified by the values of  ENUM_LINE_STYLE . N is the number of graphic series; numbering starts from 1 |
| indicator_typeN | int | Type of graphical plotting, specified by the values of  ENUM_DRAW_TYPE . N is the number of graphic series; numbering starts from 1 |
| indicator_levelN | double | Horizontal level of N in a separate indicator window |
| indicator_levelcolor | color | Color of horizontal levels of the indicator |
| indicator_levelwidth | int | Thickness of horizontal levels of the indicator |
| indicator_levelstyle | int | Style of horizontal levels of the indicator |
| script_show_confirm |  | Display a confirmation window before running the script |
| script_show_inputs |  | Display a window with the properties before running the script and disable this confirmation window |
| tester_indicator | string | Name of a custom indicator in the format of " indicator_name.ex5".  Indicators that require testing are defined automatically from the call of the  iCustom()  function, if the corresponding parameter is set through a constant string. For all other cases (use of the  IndicatorCreate()  function or use of a non-constant string in the parameter that sets the indicator name) this property is required |
| tester_file | string | File name for a tester with the indication of extension, in double quotes (as a constant string). The specified file will be passed to tester. Input files to be tested, if there are necessary ones, must always be specified. |
| tester_library | string | Library name with the extension, in double quotes. A library can have 'dll' or 'ex5' as file extension. Libraries that require testing are defined automatically. However, if any of libraries is used by a  custom  indicator, this property is required |
| tester_set | string | Name of the set file with the values ​​and the step of the input parameters. The file is passed to tester before testing and optimization. The file name is specified with an extension and double quotes as a constant string.  
   
 If you specify the EA name and the version number as "<expert_name>_<number>.set" in a set file name, then it is automatically added to the parameter versions download menu under the <number> version number. For example, the name "MACD Sample_4.set" means that this is a set file for the "MACD Sample.mq5" EA with the version number equal to 4. 
   
 To study the format, we recommend that you manually save the test/optimization settings in the strategy tester and then open the set file created in this way. |
| tester_no_cache | string | When performing  optimization , the strategy tester saves all results of executed passes to the  optimization cache , in which the test result is saved for each set of the  input parameters . This allows using the ready-made results during re-optimization on the same parameters without wasting time on re-calculation.  
   
 But in some tasks (for example, in math calculations), it may be necessary to carry out calculations regardless of the availability of ready-made results in the optimization cache. In this case, the file should include the  tester_no_cache  property. The test results are still stored in the cache, so that you can see all the data on performed passes in the strategy tester. |
| tester_everytick_calculate | string | In the Strategy Tester, indicators are only calculated when their data are accessed, i.e. when the values of indicator buffers are requested. This provides a significantly faster testing and optimization speed, if you do not need to obtain indicator values on each tick. 
   
 By specifying the  tester_everytick_calculate  property, you can enable the forced calculation of the indicator on  every tick .  
   
 Indicators in the Strategy Tester are also forcibly calculated on every tick in the following cases: 
 
 when testing in the  visual mode ; 
 if the indicator has any of the following functions:  EventChartCustom ,  OnChartEvent ,  OnTimer ; 
 if the indicator was created using the compiler with  build number  below 1916. 
 
   
 This feature only applies in the Strategy Tester, while in the terminal indicators are always calculated on each received tick. |
| optimization_chart_mode | string | Specifies the chart type and the names of two  input parameters  which will be used for the visualization of optimization results. For example, "3d, InpX, InpY" means that the results will be shown in a 3D chart with the coordinate axes based on the tested InpX and InpY parameter values. Thus, the property enables the specification of parameters that will be used to display the optimization chart and the chart type, directly in the program code. 
 Possible options: 
 
 "3d, input_parameter_name1, input_parameter_name2" means a  3D visualization chart , which can be rotated, zoomed in and out. The chart is built using two parameters. 
 "2d, input_parameter_name1, input_parameter_name2" means a 2D grid chart, in which each cell is painted in a certain color depending on the result. The chart is built using two parameters. 
 "1d, input_parameter_name1, input_parameter_name2" means a  linear chart , in which the results are sorted by the specified parameter. Each pass is displayed as a point. The chart is built based on one parameter. 
 "0d, input_parameter_name1, input_parameter_name2" means a regular chart with results sorted by the pass result arrival time. Each pass is displayed as a point in the chart. Parameter indication is not required, but the specified parameters can be used for the manual switch to other chart types. 
 
 Optionally, you can indicate only the chart type, without specifying one or two input parameters. In this case, the terminal will select the required parameters to show the optimization chart. |

Sample Task of Description and Version Number

```
#property version     "3.70"      // Current version of the Expert Advisor
#property description "ZigZag universal with Pesavento Patterns"
#property description "At the moment in the indicator several ZigZags with different algorithms are included"
#property description "It is possible to embed a large number of other indicators showing the highs and"
#property description "lows and automatically build from these highs and lows various graphical tools"

```

![Example of displaying description and version at program startup](pics/property_description.png)

Examples of Specifying a Separate Label for Each Indicator Buffer ( "C open; C high; C low; C close")

```
#property indicator_chart_window
#property indicator_buffers 4
#property indicator_plots   1
#property indicator_type1   DRAW_CANDLES
#property indicator_width1  3
#property indicator_label1  "C open;C high;C low;C close"

```

![Example of displaying a label for each indicator buffer](pics/plot_label.png)
