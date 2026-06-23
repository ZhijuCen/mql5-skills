# MQLInfoString

Returns the value of a corresponding property of a running mql5 program.

```
string  MQLInfoString(
   int  property_id      // Identifier of a property
   );

```

Parameters

property_id

[in] Identifier of a property. Can be one of the [ENUM_MQL_INFO_STRING](/en/docs/constants/environment_state/mql5_programm_info#enum_mql_info_string) enumeration.

Return Value

Value of string type.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the launched program data
   string name = MQLInfoString(MQL_PROGRAM_NAME);  // name of the launched MQL5 program
   string path = MQLInfoString(MQL_PROGRAM_PATH);  // running program path
   
//--- send the obtained data to the journal
   PrintFormat("Name of the running MQL program: '%s'\nPath of the running MQL program: %s", name, path);
   /*
   result:
   Name of the running MQL program: 'MQLInfoString'
   Path of the running MQL program: E:\MetaQuotes\MetaTrader 5\MQL5\Scripts\MQLInfoString.ex5
   */
  }

```
