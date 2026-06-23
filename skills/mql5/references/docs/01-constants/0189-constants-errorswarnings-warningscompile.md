# Compiler Warnings

Compiler warnings are shown for informational purposes only and are not error messages.

| Code | Description |
| --- | --- |
| 21 | Incomplete record of a date in the datetime string |
| 22 | Wrong number in the datetime string for the date. Requirements: 
    Year 1970 <= X <= 3000 
    Month 0 <X <= 12 
    Day 0 <X <= 31/30/28 (29 ).... |
| 23 | Wrong number of datetime string for time. Requirements: 
    Hour    0 <= X <24 
    Minute 0 <= X <60 |
| 24 | Invalid color in RGB format: one of RGB components is less than 0 or greater than 255 |
| 25 | Unknown character of the escape sequences. 
    Known: \n \r \t \\ \" \' \X \x |
| 26 | Too large volume of local variables (> 512Kb) of the function, reduce the number |
| 29 | Enumeration already defined (duplication) - members will be added to the first definition |
| 30 | Overriding macro |
| 31 | The variable is declared but is not used anywhere |
| 32 | Constructor must be of void type |
| 33 | Destructor must be of void type |
| 34 | Constant does not fit in the range of integers (X> _UI64_MAX | | X <_I64_MIN) and will be converted to the double type |
| 35 | Too long HEX - more than 16 significant characters (senior nibbles are cut) |
| 36 | No nibbles in HEX string "0x" |
| 37 | No function - nothing to be performed |
| 38 | A non-initialized variable is used |
| 41 | Function has no body, and is not called |
| 43 | Possible loss of data at typecasting. Example: int x = (double) z; |
| 44 | Loss of accuracy (of data) when converting a constant. Example: int x = M_PI |
| 45 | Difference between the signs of operands in the operations of comparison. Example: (char) c1> (uchar) c2 |
| 46 | Problems with function importing - declaration of #import is required or import of functions is closed |
| 47 | Too large description - extra characters will not be included in the executable file |
| 48 | The number of indicator buffers declared is less than required |
| 49 | No color to plot a graphical series in the indicator |
| 50 | No graphical series to draw the indicator |
| 51 | 'OnStart' handler function not found in the script |
| 52 | 'OnStart' handler function is defined with wrong parameters |
| 53 | 'OnStart' function can be defined only in a script |
| 54 | 'OnInit' function is defined with wrong parameters |
| 55 | 'OnInit' function is not used in scripts |
| 56 | 'OnDeinit' function is defined with wrong parameters |
| 57 | 'OnDeinit' function is not used in scripts |
| 58 | Two 'OnCalculate' functions are defined.  OnCalculate () at one price array  will be used |
| 59 | Overfilling detected when calculating a complex  integer  constant |
| 60 | Probably, the variable is  not initialized . |
| 61 | This declaration makes it impossible to refer to the  local variable  declared on the specified line |
| 62 | This declaration makes it impossible to refer to the  global variable  declared on the specified line |
| 63 | Cannot be used for  static allocated array |
| 64 | This variable declaration hides  predefined variable |
| 65 | The value of the expression is always  true / false |
| 66 | Using a variable or  bool  type expression in mathematical operations is unsafe |
| 67 | The result of applying the unary minus operator to an unsigned  ulong  type is undefined |
| 68 | The version specified in the  #property version  property is unacceptable for the  Market  section; the correct format of #property version id "XXX.YYY" |
| 69 | Empty controlled statement found |
| 70 | Invalid function return type or incorrect parameters during declaration of the  event handler function |
| 71 | An implicit  cast of structures  to one type is required |
| 72 | This declaration makes direct access to the member of a  class  declared in the specified string impossible. Access will be possible only with the  scope resolution operation :: |
| 73 | Binary constant is too big, high-order digits will be truncated |
| 74 | Parameter in the method of the  inherited class  has a different  const  modifier, the derived function has  overloaded  the parent function |
| 75 | Negative or too large shift value in  shift bitwise operation , execution result is undefined |
| 76 | Function must  return a value |
| 77 | void  function returns a value |
| 78 | Not all control paths return a value |
| 79 | Expressions are not allowed on a  global scope |
| 80 | Check  operator precedence  for possible error; use parentheses to clarify precedence |
| 81 | Two  OnCalCulate()  are defined. OHLC version will be used |
| 82 | Struct  has no members, size assigned to 1 byte |
| 83 | Return value of the function should be checked |
| 84 | Resource indicator is compiled for debugging. That slows down the performance. Please recompile the indicator to increase performance |
| 85 | Too great character code in the string, must be in the range 0 to 65535 |
| 86 | Unrecognized character in the string |
| 87 | No indicator window property (setting the display in the main window or a subwindow) is defined. Property  #property indicator_chart_window  is applied |
