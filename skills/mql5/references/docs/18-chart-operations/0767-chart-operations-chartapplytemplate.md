# ChartApplyTemplate

Applies a specific template from a specified file to the chart. The command is added to chart messages queue and will be executed after processing of all previous commands.

```
bool  ChartApplyTemplate(
   long          chart_id,     // Chart ID
   const string  filename      // Template file name
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

filename

[in]  The name of the file containing the template.

Return Value

Returns true if the command has been added to chart queue, otherwise false. To get an information about the [error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The Expert Advisor will be unloaded and will not be able to continue operating in case of successful loading of a new template to the chart it is attached to.

When applying the template to the chart, trade permissions may be limited due to security reasons:

```
Live trading permission cannot be extended for the Expert Advisors launched by applying the template using ChartApplyTemplate() function.

```

If the mql5-program calling ChartApplyTemplate() function has no permission to trade, the Expert Advisor launched via the template will also not be able to trade regardless of the template settings.

If the mql5-program calling ChartApplyTemplate() function has permission to trade, while there is no such permission in the template settings, the Expert Advisor launched via the template will not be able to trade.

## Using Templates

The resources of the MQL5 language allow setting multiple chart properties, including colors using the [ChartSetInteger()](/en/docs/chart_operations/chartsetinteger) function:

- Chart background color;
- Color of the axes, scale and the OHLC line;
- Grid color;
- Color of volumes and position open levels;
- Color of the up bar, shadow and edge of a bullish candlestick;
- Color of the down bar, shadow and edge of a bearish candlestick;
- Color of the chart line and Doji candlesticks;
- Color of the bullish candlestick body;
- Color of the bearish candlestick body;
- Color of the Bid price line;
- Color of the Ask price line;
- Color of the line of the last deal price (Last);
- Color of the stop order levels (Stop Loss and Take Profit).

Besides, there can be multiple [graphical objects](/en/docs/objects) and [indicators](/en/docs/indicators) on a chart. You may set up a chart with all the necessary indicators once and then save it as a template. Such a template can be applied to any chart.

The [ChartApplyTemplate()](/en/docs/chart_operations/chartapplytemplate) function is intended for using a previously saved template, and it can be used in any mql5 program. The path to the file that stores the template is passed as the second parameter to ChartApplyTemplate(). The template file is searched according to the following rules:

- if the backslash "\" separator (written as "\\") is placed at  the beginning of the path, the template is searched for relative to the path _terminal_data_directory\MQL5,
- if there is no backslash, the template is searched for relative to the executable EX5 file, in which ChartApplyTemplate() is called;
- if a template is not found in the first two variants, the search is performed in the folder terminal_directory\Profiles\Templates\.

Here terminal_directory is the folder from which the MetaTrader 5 Client Terminal is running, and terminal_data_directory is the folder, in which editable files are stored, its location depends on the operating system, user name and computer's security settings. Normally they are different folders, but in some cases they may coincide.

The location of folders terminal_data_directory and terminal_directory can be obtained using the [TerminalInfoString()](/en/docs/check/terminalinfostring) function.

```
//--- directory from which the terminal is started
   string terminal_path=TerminalInfoString(TERMINAL_PATH);
   Print("Terminal directory:",terminal_path);
//--- terminal data directory, in which the MQL5 folder with EAs and indicators is located
   string terminal_data_path=TerminalInfoString(TERMINAL_DATA_PATH);
   Print("Terminal data directory:",terminal_data_path);

```

For example:

```
//--- search for a template in terminal_data_directory\MQL5\
ChartApplyTemplate(0,"\\first_template.tpl"))
//--- search for a template in directory_of_EX5_file\, then in folder terminal_data_directory\Profiles\Templates\
ChartApplyTemplate(0,"second_template.tpl"))
//--- search for a template in directory_of_EX5_file\My_templates\, then in folder terminal_directory\Profiles\Templates\My_templates\
ChartApplyTemplate(0,"My_templates\\third_template.tpl"))

```

Templates are not resources, they cannot be included into an executable EX5 file.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- example of applying template, located in \MQL5\Files
   if(FileIsExist("my_template.tpl"))
     {
      Print("The file my_template.tpl found in \Files'");
      //--- apply template
      if(ChartApplyTemplate(0,"\\Files\\my_template.tpl"))
        {
         Print("The template 'my_template.tpl' applied successfully");
         //--- redraw chart
         ChartRedraw();
        }
      else
         Print("Failed to apply 'my_template.tpl', error code ",GetLastError());
     }
   else
     {
      Print("File 'my_template.tpl' not found in "
            +TerminalInfoString(TERMINAL_PATH)+"\\MQL5\\Files");
     }
  }

```

See also

[Resources](/en/docs/runtime/resources)
