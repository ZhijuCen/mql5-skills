# A simple way to create indicator instances: iCustom

MQL5 provides two functions for creating indicator instances from programs: iCustom and IndicatorCreate. The first function involves passing a list of parameters, which must be known at the time of compiling the program. The second one allows you to dynamically form an array with the parameters of the called indicator during the program execution. This advanced mode will be discussed in the section [Advanced way to create indicators: ](/en/book/applications/indicators_use/indicators_indicatorcreate)[IndicatorCreate](/en/book/applications/indicators_use/indicators_indicatorcreate).

int iCustom(const string symbol, ENUM_TIMEFRAMES timeframe, const string pathname, ...)

The function creates an indicator for the specified symbol and timeframe. NULL in the symbol parameter can be used to indicate the symbol of the current chart, while 0 in the timeframe parameter sets the current period.

In the pathname parameter, specify the indicator name (the name of the ex5 file without extension) and, optionally, the path. More details about the path are given below.

The indicator referenced by pathname must be compiled.

The function returns an indicator handle or INVALID_HANDLE in case of an error. The handle will be required to call other functions described in this chapter and included in the indicator program control group. The handle is an integer that uniquely describes the created indicator instance within the calling program.

The ellipsis in the iCustom function prototype indicates a list of actual parameters for the indicator. Their types and order must correspond to the formal parameters (in the indicator code). However, it is allowed to omit values starting from the end of the parameter list. For such parameters not specified in the calling code, the created indicator will use the default values of the corresponding inputs.

For example, if the indicator takes two input variables: period (input int WorkPeriod = 14) and price type (input ENUM_APPLIED_PRICE WorkPrice = PRICE_CLOSE), then you can call iCustom of varying degrees of detail:

- iCustom(_Symbol, _Period, 21, PRICE_TYPICAL): setting values for the entire list of parameters
- iCustom(_Symbol, _Period, 21): setting the first parameter, the second parameter is omitted and will receive the value PRICE_CLOSE
- iCustom(_Symbol, _Period): both parameters are omitted and will get the values 14 and PRICE_CLOSE

You cannot omit a parameter at the beginning or in the middle of the parameter list.

If the indicator being created has a short form of [OnCalculate](/en/book/applications/indicators_make/indicators_oncalculate), then the last additional parameter (in addition to the list of input variables described inside the indicator) can be the type of price used to build the indicator. It's like a drop down list Apply to in the indicator properties dialog. Also, in this additional parameter, you can pass a handle to another previously created indicator (see an example below). In this case, the newly created indicator will be calculated using the first indicator buffer with the specified handle. In other words, the programmer can set the calculation of one indicator from another.

MQL5 does not provide programmatic means to find out if a specific third-party indicator is implemented using the short form or the long form of OnCalculate, that is, whether it is allowed to pass an additional handle when creating via iCustom. Also, MQL5 does not allow selecting the buffer number if the indicator identified by the additional handle has several buffers.

Let's go back to the pathname parameter.

A path is a string containing at least one backslash ('\') or forward slash ('/'), which is a special character used in the file system as a separator in the hierarchy of folders and files. You can use either a forward or a backslash, but the latter requires "escaping", meaning it must be written twice. This is due to the fact that the backslash is a control character that forms many service codes, such as tabulation ('\t'), newline ('\n') and so on (see the section [Character types](/en/book/basis/builtin_types/characters)).

If the path starts with a slash, it is called absolute, and its root folder is the directory of all MQL5 source codes. For example, specifying the string "/MyIndicator" in the parameter pathname will search for the file MQL5/MyIndicator.ex5, and the longer path with the "/Exercise/MyIndicator" directory will refer to MQL5/Exercise/MyIndicator.ex5.

If the pathname parameter contains one or more slashes but does not begin with one, then the path is called relative because it is then considered relative to one of two predefined locations. Firstly, the indicator file is searched relative to the folder where the calling MQL program is located. If it can't be found there, then the search continues inside the common folder of indicators MQL5/Indicators.

In a line with slashes, the fragment that is located to the right of the rightmost slash is treated as the file name, and all previous ones describe the folder hierarchy. For example, the path "Folder/SubFolder/Filename" matches two subfolders: SubFolder inside Folder, and the Filename file inside SubFolder.

The simplest case is when pathname contains no slashes. This way it specifies only the file name. It is also considered in the context of the two starting points of the search mentioned above.

For example, the MyExpert.ex5 Expert Advisor is located in the folder MQL5/Experts/Examples, and it contains the call of iCustom(_Symbol, _Period, "MyIndicator"). Here the relative path is degenerate (empty) and only the file name is present. Thus, the indicator search starts from the folder MQL5/Experts/Examples/ and the name MyIndicator, which gives MQL5/Experts/Examples/MyIndicator.ex5. If such an indicator is not found in this directory, the search will continue in the root folder of the indicators, that is, by the connected path and name MQL5/Indicators/MyIndicator.ex5.

If the indicator is not found in both places, the function will return INVALID_HANDLE and set error code 4802 (ERR_INDICATOR_CANNOT_CREATE) to _LastError.

A more difficult case is if pathname contains not only the name, but also the directory, for example "TradeSignals/MyIndicator". The specified path is then added to the folder of the calling program, resulting in the following search target:MQL5/Experts/Examples/TradeSignals/MyIndicator.ex5. Then, on failure, the same path is added to MQL5/Indicators, that is, the file is searched MQL5/Indicators/TradeSignals/MyIndicator.ex5. Please note that if you use a backslash as a separator, you should not forget to write it twice, for example, iCustom(_Symbol, _Period, "TradeSignals\\MyIndicator").

To free the computer memory from an indicator that is no longer in use, use the [IndicatorRelease](/en/book/applications/indicators_use/indicators_indicatorrelease) function passing the handle of this indicator to it.

Particular attention should be paid to testing a program that uses indicators. If the pathname parameter in iCustom call is specified as a constant string, then the corresponding required indicator is automatically detected by the compiler and passed to the tester along with the program being tested. Otherwise, if the parameter is calculated in an expression or obtained from outside (for example, via input from the user), you must specify the property in the source code #property tester_indicator:

```
#property tester_indicator "indicator_name.ex5"

```

This means that only previously known custom indicators can be tested in programs.

Consider an example of a new indicator UseWPR1.mq5, which, inside its OnInit handler, will be creating a handle of the IndWPR indicator we discussed in the previous chapter (don't forget to compile IndWPR because iCustom downloads ex5 files). The handler received in UseWPR1 is not used in any way yet as we will only study the possibility itself and check the indication of success. Therefore, we do not need buffers in the new indicator.

```
#property indicator_separate_window
#property indicator_buffers 0
#property indicator_plots   0

```

The indicator will create an empty subwindow but will not display anything in it yet. This is normal behavior.

Let's check several options for obtaining a descriptor, with different values of pathname:

1. An absolute path that starts with a slash and therefore includes the entire folder hierarchy (starting from MQL5) with examples of Chapter 5 indicators, that is, "/Indicators/MQL5Book/p5/IndWPR"
2. Only the name "IndWPR" to search in the same folder where the calling indicator UseWPR1.mq5 is located (both indicators are provided in the same folder)
3. Path with folder hierarchy of indicator examples relative to the standard directory MQL5/Indicators, that is, "MQL5Book/p5/IndWPR" (note that there is no slash at the beginning)
4. Only the name as in to point 2 but for the non-existent indicator "IndWPR NonExistent"
5. Absolute path as in point 1 but with backslashes without escaping them, that is, "\Indicators\MQL5Book\p5\IndWPR"
6. Full copy of point 2.

```
int OnInit()
{
   int handle1 = PRTF(iCustom(_Symbol, _Period, "/Indicators/MQL5Book/p5/IndWPR"));
   int handle2 = PRTF(iCustom(_Symbol, _Period, "IndWPR"));
   int handle3 = PRTF(iCustom(_Symbol, _Period, "MQL5Book/p5/IndWPR"));
   int handle4 = PRTF(iCustom(_Symbol, _Period, "IndWPR NonExistent"));
   int handle5 = PRTF(iCustom(_Symbol, _Period, "\Indicators\MQL5Book\p5\IndWPR"));
   int handle6 = PRTF(iCustom(_Symbol, _Period, "IndWPR"));
   return INIT_SUCCEEDED;
}

```

Because handle variables are not used, they are declared local. Let's specifically explain that although local handle variables are deleted upon exit from OnInit, this does not affect the handles: they continue to exist as long as the "parent" indicator UseWPR is executed. We simply lose the values of these handles in our code, which is not a problem though, because they are not used anywhere here. In the real indicator examples that we will consider later, the handles are, of course, stored (usually in global variables) and used.

Don't worry about resource leaks either: when deleting the UseWPR indicator from the chart, all handles created by it will be automatically cleared by the terminal. The principles and the need for explicit release of handles will be described in more detail in the section on [deleting indicator instances](/en/book/applications/indicators_use/indicators_indicatorrelease) by using IndicatorRelease.

The above OnInit code generates the following log entries.

```
iCustom(_Symbol,_Period,/Indicators/MQL5Book/p5/IndWPR)=10 / ok
iCustom(_Symbol,_Period,IndWPR)=11 / ok
iCustom(_Symbol,_Period,MQL5Book/p5/IndWPR)=12 / ok
cannot load custom indicator 'IndWPR NonExistent' [4802]
iCustom(_Symbol,_Period,IndWPR NonExistent)=-1 / INDICATOR_CANNOT_CREATE(4802)
iCustom(_Symbol,_Period,\Indicators\MQL5Book\p5\IndWPR)=13 / ok
iCustom(_Symbol,_Period,IndWPR)=11 / ok

```

As we can see, meaningful handles 10, 11, 12, and 13 are received in all cases except the 4th, with a non-existent called indicator. The value of the handle is -1 (INVALID_HANDLE).

Also note that the 5th line generates several "unrecognized character escape sequence" warnings when compiled. This is a consequence of the fact that we did not escape the backslash. And we were also lucky that the instruction was executed successfully, because if the name of any folder or file began with one of the letters in the supported escape sequences, then the interpretation of the sequence would violate the expected reading of the name. For example, if we had an indicator named "test" in the same folder and tried to create it via the path "MQL5Book\p5\test", we would get INVALID_HANDLE and error 4802.This is because '\t' is a tab character, so the terminal would look for "MQL5Book\p5<nbsp> est". The correct entry should be "MQL5Book\\p5\\test". Therefore, it is easier to use a forward slash.

It is also important to note that although all successful variations refer to the same indicator MQL5/Indicators/MQL5Book/p5/IndWPR.ex5, and in fact paths 1, 2, 3 and 5 are equivalent, the terminal treats them as different strings, which is why we get different descriptor values. And only option 6, which completely duplicates option 2, returns an identical descriptor - 11.

Why does handle numbering start at 10? Smaller values are reserved for the system. As mentioned above, for indicators with a short form of OnCalculate, the last parameter can be used to pass the price type or a handle of another indicator, the buffer of which will be used to calculate the newly created instance. Since the elements of the ENUM_APPLIED_PRICE enumeration have their own constant values, they occupy the area below 10. For further details please see [Defining data source for an indicator](/en/book/applications/indicators_use/indicators_apply_to).

In the next example of UseWPR2.mq5 we will implement an indicator that will create an instance of IndWPR and will check the progress of its calculation using the handle. But for this you need to get familiarized with the new function BarsCalculated.
