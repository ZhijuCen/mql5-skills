<!-- source: https://www.tradingview.com/pine-script-reference/v6/ | fetched 2026-09-23 | examples omitted -->

<!-- anchor: fun_input -->
Adds an input to the Inputs tab of your script's Settings, which allows you to provide configuration options to script users. This function automatically detects the type of the argument used for 'defval' and uses the corresponding input widget.

#### Syntax & Overloads

input(defval, title, tooltip, inline, group, display, active) → input color

input(defval, title, tooltip, inline, group, display, active) → input string

input(defval, title, tooltip, inline, group, display, active) → input int

input(defval, title, tooltip, inline, group, display, active) → input float

input(defval, title, inline, group, tooltip, display, active) → series float

input(defval, title, tooltip, inline, group, display, active) → input bool

#### Arguments

**defval (const int/float/bool/string/color or source-type built-ins) **Determines the default value of the input variable proposed in the script's "Settings/Inputs" tab, from where script users can change it. Source-type built-ins are built-in series float variables that specify the source of the calculation: `close`, `hlc3`, etc.

**title (const string) **Title of the input. If not specified, the variable name is used as the input's title. If the title is specified, but it is empty, the name will be an empty string.

**tooltip (const string) **The string that will be shown to the user when hovering over the tooltip icon.

**inline (const string) **Combines all the input calls using the same argument in one line. The string used as an argument is not displayed. It is only used to identify inputs belonging to the same line.

**group (const string) **Creates a header above all inputs using the same group argument string. The string is also used as the header's text.

**display (const plot_display) **Controls where the script will display the input's information, aside from within the script's settings. This option allows one to remove a specific input from the script's status line or the Data Window to ensure only the most necessary inputs are displayed there. Possible values: display.none, display.data_window, display.status_line, display.all. Optional. The default depends on the type of the value passed to `defval`: display.none for bool and color values, display.all for everything else.

**active (input bool) **Optional. Specifies whether users can change the value of the input in the script's "Settings/Inputs" tab. The script can use this parameter to set the state of the input based on the values of other inputs. If true, users can change the value of the input. If false, the input is grayed out, and users cannot change the value. The default is true.

#### Returns

Value of input variable.

#### Remarks

Result of input() function always should be assigned to a variable, see examples above.

#### See also

input.bool()input.color()input.int()input.float()input.string()input.symbol()input.timeframe()input.text_area()input.session()input.source()input.time()

<!-- anchor: fun_input.int -->
Adds an input to the Inputs tab of your script's Settings, which allows you to provide configuration options to script users. This function adds a field for an integer input to the script's inputs.

#### Syntax & Overloads

input.int(defval, title, options, tooltip, inline, group, confirm, display, active) → input int

input.int(defval, title, minval, maxval, step, tooltip, inline, group, confirm, display, active) → input int

#### Arguments

**defval (const int) **Determines the default value of the input variable proposed in the script's "Settings/Inputs" tab, from where script users can change it. When a list of values is used with the `options` parameter, the value must be one of them.

**title (const string) **Title of the input. If not specified, the variable name is used as the input's title. If the title is specified, but it is empty, the name will be an empty string.

**options (tuple of const int values: [val1, val2, ...]) **A list of options to choose from a dropdown menu, separated by commas and enclosed in square brackets: [val1, val2, ...]. When using this parameter, the `minval`, `maxval` and `step` parameters cannot be used.

**tooltip (const string) **The string that will be shown to the user when hovering over the tooltip icon.

**inline (const string) **Combines all the input calls using the same argument in one line. The string used as an argument is not displayed. It is only used to identify inputs belonging to the same line.

**group (const string) **Creates a header above all inputs using the same group argument string. The string is also used as the header's text.

**confirm (const bool) **If true, then user will be asked to confirm input value before indicator is added to chart. Default value is false.

**display (const plot_display) **Controls where the script will display the input's information, aside from within the script's settings. This option allows one to remove a specific input from the script's status line or the Data Window to ensure only the most necessary inputs are displayed there. Possible values: display.none, display.data_window, display.status_line, display.all. Optional. The default is display.all.

**active (input bool) **Optional. Specifies whether users can change the value of the input in the script's "Settings/Inputs" tab. The script can use this parameter to set the state of the input based on the values of other inputs. If true, users can change the value of the input. If false, the input is grayed out, and users cannot change the value. The default is true.

#### Returns

Value of input variable.

#### Remarks

Result of input.int() function always should be assigned to a variable, see examples above.

#### See also

input.bool()input.float()input.string()input.text_area()input.symbol()input.timeframe()input.session()input.source()input.color()input.time()input()

<!-- anchor: fun_input.bool -->
Adds an input to the Inputs tab of your script's Settings, which allows you to provide configuration options to script users. This function adds a checkmark to the script's inputs.

#### Syntax

```
input.bool(defval, title, tooltip, inline, group, confirm, display, active) → input bool
```

#### Arguments

**defval (const bool) **Determines the default value of the input variable proposed in the script's "Settings/Inputs" tab, from where the user can change it.

**title (const string) **Title of the input. If not specified, the variable name is used as the input's title. If the title is specified, but it is empty, the name will be an empty string.

**tooltip (const string) **The string that will be shown to the user when hovering over the tooltip icon.

**inline (const string) **Combines all the input calls using the same argument in one line. The string used as an argument is not displayed. It is only used to identify inputs belonging to the same line.

**group (const string) **Creates a header above all inputs using the same group argument string. The string is also used as the header's text.

**confirm (const bool) **If true, then user will be asked to confirm input value before indicator is added to chart. Default value is false.

**display (const plot_display) **Controls where the script will display the input's information, aside from within the script's settings. This option allows one to remove a specific input from the script's status line or the Data Window to ensure only the most necessary inputs are displayed there. Possible values: display.none, display.data_window, display.status_line, display.all. Optional. The default is display.none.

**active (input bool) **Optional. Specifies whether users can change the value of the input in the script's "Settings/Inputs" tab. The script can use this parameter to set the state of the input based on the values of other inputs. If true, users can change the value of the input. If false, the input is grayed out, and users cannot change the value. The default is true.

#### Returns

Value of input variable.

#### Remarks

Result of input.bool() function always should be assigned to a variable, see examples above.

#### See also

input.int()input.float()input.string()input.text_area()input.symbol()input.timeframe()input.session()input.source()input.color()input.time()input()

<!-- anchor: fun_input.float -->
Adds an input to the Inputs tab of your script's Settings, which allows you to provide configuration options to script users. This function adds a field for a float input to the script's inputs.

#### Syntax & Overloads

input.float(defval, title, options, tooltip, inline, group, confirm, display, active) → input float

input.float(defval, title, minval, maxval, step, tooltip, inline, group, confirm, display, active) → input float

#### Arguments

**defval (const int/float) **Determines the default value of the input variable proposed in the script's "Settings/Inputs" tab, from where script users can change it. When a list of values is used with the `options` parameter, the value must be one of them.

**title (const string) **Title of the input. If not specified, the variable name is used as the input's title. If the title is specified, but it is empty, the name will be an empty string.

**options (tuple of const int/float values: [val1, val2, ...]) **A list of options to choose from a dropdown menu, separated by commas and enclosed in square brackets: [val1, val2, ...]. When using this parameter, the `minval`, `maxval` and `step` parameters cannot be used.

**tooltip (const string) **The string that will be shown to the user when hovering over the tooltip icon.

**inline (const string) **Combines all the input calls using the same argument in one line. The string used as an argument is not displayed. It is only used to identify inputs belonging to the same line.

**group (const string) **Creates a header above all inputs using the same group argument string. The string is also used as the header's text.

**confirm (const bool) **If true, then user will be asked to confirm input value before indicator is added to chart. Default value is false.

**display (const plot_display) **Controls where the script will display the input's information, aside from within the script's settings. This option allows one to remove a specific input from the script's status line or the Data Window to ensure only the most necessary inputs are displayed there. Possible values: display.none, display.data_window, display.status_line, display.all. Optional. The default is display.all.

**active (input bool) **Optional. Specifies whether users can change the value of the input in the script's "Settings/Inputs" tab. The script can use this parameter to set the state of the input based on the values of other inputs. If true, users can change the value of the input. If false, the input is grayed out, and users cannot change the value. The default is true.

#### Returns

Value of input variable.

#### Remarks

Result of input.float() function always should be assigned to a variable, see examples above.

#### See also

input.bool()input.int()input.string()input.text_area()input.symbol()input.timeframe()input.session()input.source()input.color()input.time()input()

<!-- anchor: fun_input.string -->
Adds an input to the Inputs tab of your script's Settings, which allows you to provide configuration options to script users. This function adds a field for a string input to the script's inputs.

#### Syntax

```
input.string(defval, title, options, tooltip, inline, group, confirm, display, active) → input string
```

#### Arguments

**defval (const string) **Determines the default value of the input variable proposed in the script's "Settings/Inputs" tab, from where the user can change it. When a list of values is used with the `options` parameter, the value must be one of them.

**title (const string) **Title of the input. If not specified, the variable name is used as the input's title. If the title is specified, but it is empty, the name will be an empty string.

**options (tuple of const string values: [val1, val2, ...]) **A list of options to choose from.

**tooltip (const string) **The string that will be shown to the user when hovering over the tooltip icon.

**inline (const string) **Combines all the input calls using the same argument in one line. The string used as an argument is not displayed. It is only used to identify inputs belonging to the same line.

**group (const string) **Creates a header above all inputs using the same group argument string. The string is also used as the header's text.

**confirm (const bool) **If true, then user will be asked to confirm input value before indicator is added to chart. Default value is false.

**display (const plot_display) **Controls where the script will display the input's information, aside from within the script's settings. This option allows one to remove a specific input from the script's status line or the Data Window to ensure only the most necessary inputs are displayed there. Possible values: display.none, display.data_window, display.status_line, display.all. Optional. The default is display.all.

**active (input bool) **Optional. Specifies whether users can change the value of the input in the script's "Settings/Inputs" tab. The script can use this parameter to set the state of the input based on the values of other inputs. If true, users can change the value of the input. If false, the input is grayed out, and users cannot change the value. The default is true.

#### Returns

Value of input variable.

#### Remarks

Result of input.string() function always should be assigned to a variable, see examples above.

#### See also

input.text_area()input.bool()input.int()input.float()input.symbol()input.timeframe()input.session()input.source()input.color()input.time()input()

<!-- anchor: fun_input.source -->
Adds an input to the Inputs tab of your script's Settings, which allows you to provide configuration options to script users. This function adds a dropdown that allows the user to select a source for the calculation, e.g. close, hl2, etc. The user can also select an output from another indicator on their chart as the source.

#### Syntax

```
input.source(defval, title, tooltip, inline, group, display, active, confirm) → series float
```

#### Arguments

**defval (open/high/low/close/hl2/hlc3/ohlc4/hlcc4) **Determines the default value of the input variable proposed in the script's "Settings/Inputs" tab, from where the user can change it.

**title (const string) **Title of the input. If not specified, the variable name is used as the input's title. If the title is specified, but it is empty, the name will be an empty string.

**tooltip (const string) **The string that will be shown to the user when hovering over the tooltip icon.

**inline (const string) **Combines all the input calls using the same argument in one line. The string used as an argument is not displayed. It is only used to identify inputs belonging to the same line.

**group (const string) **Creates a header above all inputs using the same group argument string. The string is also used as the header's text.

**display (const plot_display) **Controls where the script will display the input's information, aside from within the script's settings. This option allows one to remove a specific input from the script's status line or the Data Window to ensure only the most necessary inputs are displayed there. Possible values: display.none, display.data_window, display.status_line, display.all. Optional. The default is display.all.

**active (input bool) **Optional. Specifies whether users can change the value of the input in the script's "Settings/Inputs" tab. The script can use this parameter to set the state of the input based on the values of other inputs. If true, users can change the value of the input. If false, the input is grayed out, and users cannot change the value. The default is true.

**confirm (const bool) **If true, then user will be asked to confirm input value before indicator is added to chart. Default value is false.

#### Returns

Value of input variable.

#### Remarks

Result of input.source() function always should be assigned to a variable, see examples above.

#### See also

input.bool()input.int()input.float()input.string()input.text_area()input.symbol()input.timeframe()input.session()input.color()input.time()input()

<!-- anchor: fun_input.time -->
Adds two inputs to the script's "Settings/Inputs" tab on the same line: one for the date and one for the time. The user can change the price in the settings or by selecting the indicator and dragging the price line. The function returns a date/time value in UNIX format.

#### Syntax

```
input.time(defval, title, tooltip, inline, group, confirm, display, active) → input int
```

#### Arguments

**defval (const int) **Determines the default value of the input variable proposed in the script's "Settings/Inputs" tab, from where the user can change it. The value can be a timestamp() function, but only if it uses a date argument in const string format.

**title (const string) **Title of the input. If not specified, the variable name is used as the input's title. If the title is specified, but it is empty, the name will be an empty string.

**tooltip (const string) **The string that will be shown to the user when hovering over the tooltip icon.

**inline (const string) **Combines all the input calls using the same argument in one line. The string used as an argument is not displayed. It is only used to identify inputs belonging to the same line.

**group (const string) **Creates a header above all inputs using the same group argument string. The string is also used as the header's text.

**confirm (const bool) **Optional. If true, the script prompts the user to set the input's initial value by clicking a point on the chart. If inputs of other types require confirmation, the "Confirm inputs" dialog box also displays this input's field, allowing final adjustments to the value before the script starts to run. The default is false.

**display (const plot_display) **Controls where the script will display the input's information, aside from within the script's settings. This option allows one to remove a specific input from the script's status line or the Data Window to ensure only the most necessary inputs are displayed there. Possible values: display.none, display.data_window, display.status_line, display.all. Optional. The default is display.none.

**active (input bool) **Optional. Specifies whether users can change the value of the input in the script's "Settings/Inputs" tab. The script can use this parameter to set the state of the input based on the values of other inputs. If true, users can change the value of the input. If false, the input is grayed out, and users cannot change the value. The default is true.

#### Returns

Value of input variable.

#### Remarks

The user can change the input's value by specifying a new value in the "Settings/Inputs" tab, or by moving the input's marker on the chart. Alternatively, they can select "Reset points" from the script's "More" menu and set a new input value by clicking a point on the chart.

If an input.time() and input.price() function call in the script share a unique `inline` argument and have matching `group` arguments, those calls create a single interactive point marker on the chart. The user can move that marker to adjust the input time and price values simultaneously.

#### See also

input.bool()input.int()input.float()input.string()input.text_area()input.symbol()input.timeframe()input.session()input.source()input.color()input()
