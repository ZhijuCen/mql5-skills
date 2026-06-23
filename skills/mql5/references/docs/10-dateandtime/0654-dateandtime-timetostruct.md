# TimeToStruct

Converts a value of datetime type (number of seconds since 01.01.1970) into a structure variable [MqlDateTime](/en/docs/constants/structures/mqldatetime).

```
bool  TimeToStruct(
   datetime      dt,            // date and time
   MqlDateTime&  dt_struct      // structure for the adoption of values
   );

```

Parameters

dt

[in]  Date value to convert.

dt_struct

[out]  Variable of structure type MqlDateTime.

Return Value

True if successful, otherwise false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
void OnStart()
  {
//--- get the last known time of the server, declare the date/time structure and fill in the structure fields
   datetime    time=TimeCurrent();
   MqlDateTime tm  ={};
   if(!TimeToStruct(time,tm))
      Print("TimeToStruct() failed. Error ", GetLastError());
   
//--- display the obtained server time and the result of filling the MqlDateTime structure using TimeToStruct() in the log
   PrintFormat("Server time: %s\n- Year: %u\n- Month: %02u\n- Day: %02u\n- Hour: %02u\n- Min: %02u\n- Sec: %02u\n- Day of Year: %03u\n- Day of Week: %u (%s)",
               (string)time, tm.year, tm.mon, tm.day, tm.hour, tm.min, tm.sec, tm.day_of_year, tm.day_of_week, EnumToString((ENUM_DAY_OF_WEEK)tm.day_of_week));
   /*
   result:
   Server time: 2024.04.18 15:47:27
   - Year: 2024
   - Month: 04
   - Day: 18
   - Hour: 15
   - Min: 47
   - Sec: 27
   - Day of Year: 108
   - Day of Week: 4 (THURSDAY)
   */
  }

```
