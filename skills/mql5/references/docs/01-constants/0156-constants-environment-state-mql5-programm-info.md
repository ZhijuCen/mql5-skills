# Running MQL5 Program Properties

To obtain information about the currently running mql5 program, constants from ENUM_MQL_INFO_INTEGER and ENUM_MQL_INFO_STRING are used.

For function [MQLInfoInteger](/en/docs/check/mqlinfointeger)

ENUM_MQL_INFO_INTEGER

| Identifier | Description | Type |
| --- | --- | --- |
| MQL_HANDLES_USED | The current number of active object handles. These include both dynamic (created via  new ) and non-dynamic objects, global/local variables or class members. The more handles a program uses, the more resources it consumes. | int |
| MQL_MEMORY_LIMIT | Maximum possible amount of dynamic memory for MQL5 program in MB | int |
| MQL_MEMORY_USED | Memory used by MQL5 program in MB | int |
| MQL_PROGRAM_TYPE | Type of the MQL5 program | ENUM_PROGRAM_TYPE |
| MQL_DLLS_ALLOWED | The permission to use DLL  for the given running program | bool |
| MQL_TRADE_ALLOWED | The  permission to trade   for the given running program | bool |
| MQL_SIGNALS_ALLOWED | The permission to modify the Signals  for the given running program | bool |
| MQL_DEBUG | Indication that the program is running in the debugging mode | bool |
| MQL_PROFILER | Indication that the program is running in the code profiling mode | bool |
| MQL_TESTER | Indication that the program is running in the tester | bool |
| MQL_FORWARD | Indication that the program is running in the forward testing process | bool |
| MQL_OPTIMIZATION | Indication that the program is running in the optimization mode | bool |
| MQL_VISUAL_MODE | Indication that the program is running in the visual testing mode | bool |
| MQL_FRAME_MODE | Indication that the Expert Advisor is running in  gathering optimization result frames mode | bool |
| MQL_LICENSE_TYPE | Type of license of the EX5 module. The license refers to the EX5 module, from which a request is made using MQLInfoInteger( MQL_LICENSE_TYPE ). | ENUM_LICENSE_TYPE |
| MQL_STARTED_FROM_CONFIG | Returns  true  if a script/EA is launched from the StartUp section of the  configuration file . This means that the script/EA had been specified in the configuration file the terminal was launched with. | bool |

For function [MQLInfoString](/en/docs/check/mqlinfostring)

ENUM_MQL_INFO_STRING

| Identifier | Description | Type |
| --- | --- | --- |
| MQL_PROGRAM_NAME | Name of the running mql5-program | string |
| MQL5_PROGRAM_PATH | Path  for the given running program | string |

For information about the type of the running program, values of ENUM_PROGRAM_TYPE are used.

ENUM_PROGRAM_TYPE

| Identifier | Description |
| --- | --- |
| PROGRAM_SCRIPT | Script |
| PROGRAM_EXPERT | Expert |
| PROGRAM_INDICATOR | Indicator |
| PROGRAM_SERVICE | Service |

ENUM_LICENSE_TYPE

| Identifier | Description |
| --- | --- |
| LICENSE_FREE | A free unlimited version |
| LICENSE_DEMO | A trial version of a paid product from the Market. It works only in the strategy tester |
| LICENSE_FULL | A purchased licensed version allows at least 5 activations. The number of activations is specified by seller. Seller may increase the allowed number of activations |
| LICENSE_TIME | A version with a limited term license |

Example:

```
   ENUM_PROGRAM_TYPE mql_program=(ENUM_PROGRAM_TYPE)MQLInfoInteger(MQL_PROGRAM_TYPE);
   switch(mql_program)
     {
      case PROGRAM_SCRIPT:
        {
         Print(__FILE__+" is script");
         break;
        }
      case PROGRAM_EXPERT:
        {
         Print(__FILE__+" is Expert Advisor");
         break;
        }
      case PROGRAM_INDICATOR:
        {
         Print(__FILE__+" is custom indicator");
         break;
        }
      default:Print("MQL5 type value is ",mql_program);
   //---
   Print("MQLInfoInteger(MQL_MEMORY_LIMIT)=", MQLInfoInteger(MQL_MEMORY_LIMIT), " MB");
   Print("MQLInfoInteger(MQL_MEMORY_USED)=", MQLInfoInteger(MQL_MEMORY_USED), " MB");
   Print("MQLInfoInteger(MQL_HANDLES_USED)=", MQLInfoInteger(MQL_HANDLES_USED), " handles");

```
