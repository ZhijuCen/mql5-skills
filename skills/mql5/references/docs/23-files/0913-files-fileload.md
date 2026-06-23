# FileLoad

Reads all data of a specified binary file into a passed array of numeric types or simple structures. The function allows you to quickly read data of a known type into the appropriate array.

```
long  FileLoad(
   const string  file_name,         // File name
   void&         buffer[],          // An array of numeric types or simple structures
   int           common_flag=0      // A file flag, is searched in <data_folder>\MQL5\Files\ by default
   );

```

Parameters

file_name

[in]  The name of the file from which data will be read.

buffer

[out]  An array of numeric types or [simple structures](/en/docs/basis/types/classes#simple_structure).

common_flag=0

[in]  [A file flag](/en/docs/constants/io_constants/fileflags) indicating the operation mode. If the parameter is not specified, the file is searched in the subfolder MQL5\Files (or in <testing_agent_directory>\MQL5\Files in case of testing).

Return Value

The number of elements read or -1 in case of an error.

Note

The FileLoad() function reads from a file the number of bytes multiple of the array element size. Suppose the file size is 10 bytes, and the function reads data into an array of type double ([sizeof](/en/docs/basis/operations/other#sizeof)(double)=8). In this case the function will read only 8 bytes, the remaining 2 bytes at the end of the file will be dropped, and the function FileLoad() will return 1 (1 element read).

Example:

```
//+------------------------------------------------------------------+
//|                                                Demo_FileLoad.mq5 |
//|                        Copyright 2016, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property script_show_inputs
//--- input parameters
input int      bars_to_save=10; // Number of bars
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   string  filename=_Symbol+"_rates.bin";
   MqlRates rates[];
//---
   int copied=CopyRates(_Symbol,_Period,0,bars_to_save,rates);
   if(copied!=-1)
     {
      PrintFormat(" CopyRates(%s) copied %d bars",_Symbol,copied);
      //---  Writing quotes to a file
      if(!FileSave(filename,rates,FILE_COMMON))
         PrintFormat("FileSave() failed, error=%d",GetLastError());
     }
   else
      PrintFormat("Failed CopyRates(%s), error=",_Symbol,GetLastError());
//--- Now reading these quotes back to the file
   ArrayFree(rates);
   long count=FileLoad(filename,rates,FILE_COMMON);
   if(count!=-1)
     {
      Print("Time\tOpen\tHigh\tLow\tClose\tTick Voulme\tSpread\tReal Volume");
      for(int i=0;i<count;i++)
        {
         PrintFormat("%s\t%G\t%G\t%G\t%G\t%I64u\t%d\t%I64u",
                     TimeToString(rates[i].time,TIME_DATE|TIME_SECONDS),
                     rates[i].open,rates[i].high,rates[i].low,rates[i].close,
                     rates[i].tick_volume,rates[i].spread,rates[i].real_volume);
        }
     }
  }

```

See also

[Structures and Classes](/en/docs/basis/types/classes), [FileReadArray](/en/docs/files/filereadarray), [FileReadStruct](/en/docs/files/filereadstruct), [FileSave](/en/docs/files/filesave)
