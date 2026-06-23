# Call of Imported Functions

To import functions during the execution of a mql5-program, the client terminal uses early binding. This means that if a program has call of an imported function, the corresponding module (ex5 or dll) is loaded during the program load. MQL5 and DLL libraries are executed in the thread of a calling module.

It is not recommended to use the fully specified name of the module to be loaded like Drive:\Directory\FileName.Ext. The MQL5 libraries are loaded from the terminal_dir\MQL5\Libraries folder. If the library hasn't been found, then the client terminal performs an attempt to load it from terminal_dir\experts folder.

The system libraries (DLL)  are loaded by the operating system rules. If the library is already loaded (for example, another Expert Advisor, and even from another client terminal, running in parallel), then it uses requests to the library already loaded. Otherwise, it performs a search in the following sequence:

1. Directory, from which the module importing dll was started. The module here is an Expert Advisor, a script, an indicator or EX5 library;
2. Directory terminal_data_directory\MQL5\Libraries ([TERMINAL_DATA_PATH](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_string)\MQL5\Libraries);
3. Directory, from which the MetaTrader 5 client terminal was started;
4. System directory;
5. Windows directory;
6. Current directory;
7. Directories listed in the PATH system variable.

If the DLL library uses another DLL in its work, the first one cannot be loaded in case when there is no second DLL.

Before an Expert Advisor (script, indicator) is loaded, a common list of all EX5 library modules is formed. It's going to be used both from a loaded Expert Advisor (script, indicator) and from libraries of this list. Thus the one-time loading of many times used EX5 library modules is needed. Libraries use [predefined variables](/en/docs/predefined) of the Expert Advisor (script, indicator) they were called by.

The imported library EX5 is searched for in the following sequence:

1. Directory, path to which is set relative to the directory of the Expert Advisor (script, indicator) that imports EX5;
2. Directory terminal_directory\MQL5\Libraries;
3. Directory MQL5\Libraries in the common directory of all MetaTrader 5 client terminals (Common\MQL5\Libraries).

Functions [imported](/en/docs/basis/preprosessor/import) DLL into a mql5-program must ensure the Windows API calls agreement. To ensure such an agreement, in the source text of programs written in C or C++, use the keyword __stdcall, which is specific to the Microsoft(r) compilers. This agreement is characterized by the following:

- caller (in our case it is a mq5-program) should "see" a prototype of a function called (imported from the DLL), in order to properly combine parameters to a stack;
- caller (in our case it is a mql5-program) puts parameters to the stack in a reverse order, from right to left - in this order an imported function reads parameters passed to it;
- parameters are passed by value, except those explicitly passed by reference (in our case strings)
- an imported function cleans the stack independently by reading parameters passed to it.

When describing the prototype of an imported function, default parameters can be used.

If the corresponding library is unable to load, or there is a prohibition on the DLL use, or the imported function is not found - the Expert Advisor stops its operation with the appropriate message "Expert Advisor stopped" in the Journal (log file). In this case the Expert Advisor will not run until it is reinitialized. An Expert Advisor can be reinitialized as a result of recompilation or after the table of its properties is opened and OK is pressed.

## Passing Parameters

All parameters of [simple types](/en/docs/basis/types#base_types) are passed by values unless it is explicitly indicated that they are passed by reference. When a [string](/en/docs/basis/types/stringconst) is passed, the address of the buffer of the copied string is passed; if a string is passed by reference, the address of the buffer of this string without copying it is passed to the function imported from DLL.

[Structures](/en/docs/basis/types/classes) that contain dynamic arrays, strings, classes, other complex structures, as well as static or [dynamic arrays](/en/docs/basis/types/dynamic_array) of the enumerated objects, can't be passed as a parameter to an imported function.

When passing an array to DLL, the address of the beginning of the data buffer is always passed (irrespective of the [AS_SERIES](/en/docs/array/arraygetasseries) flag). A function inside a DLL knows nothing about the AS_SERIES flag, the passed array is a static array of an undefined length; an additional parameter should be used for specifying the array size.
