# ArrayPrint

Prints an array of a simple type or a simple structure into journal.

```
void  ArrayPrint(
   const void&   array[],             // printed array
   uint          digits=_Digits,      // number of decimal places
   const string  separator=NULL,      // separator of the structure field values
   ulong         start=0,             // first printed element index
   ulong         count=WHOLE_ARRAY,   // number of printed elements
   ulong         flags=ARRAYPRINT_HEADER|ARRAYPRINT_INDEX|ARRAYPRINT_LIMIT|ARRAYPRINT_ALIGN    
   );

```

Parameters

array[]

[in]  Array of a simple type or a [simple structure](/en/docs/basis/types/classes#simple_structure).

digits=_Digits

[in]  The number of decimal places for real types. The default value is [_Digits](/en/docs/predefined/_digits).

separator=NULL

[in]  Separator of the structure element field values. The default value [NULL](/en/docs/basis/types/void) means an empty line. A space is used as a separator in that case.

start=0

[in]  The index of the first printed array element.  It is printed from the zero index by default.

count=WHOLE_ARRAY

[in]  Number of the array elements to be printed. The entire array is displayed by default (count=[WHOLE_ARRAY](/en/docs/constants/namedconstants/otherconstants)).

flags=ARRAYPRINT_HEADER|ARRAYPRINT_INDEX|ARRAYPRINT_LIMIT|ARRAYPRINT_ALIGN

[in]  Combination of flags setting the output mode. All flags are enabled by default:

- ARRAYPRINT_HEADER – print headers for the structure array
ARRAYPRINT_INDEX – print index at the left side
ARRAYPRINT_LIMIT – print only the first 100 and the last 100 array elements. Use if you want to print only a part of a large array.
ARRAYPRINT_ALIGN – enable alignment of the printed values – numbers are aligned to the right, while lines to the left.
ARRAYPRINT_DATE – when printing datetime, print the date in the dd.mm.yyyy format
ARRAYPRINT_MINUTES – when printing datetime, print the time in the HH:MM format
ARRAYPRINT_SECONDS – when printing datetime, print the time in the HH:MM:SS format

Return Value

No

Note

ArrayPrint() does not print all structure array fields into journal – array and [object pointer](/en/docs/basis/types/object_pointers) fields are skipped. These columns are simply not printed for more convenient presentation. If you need to print all structure fields, you need to write your own mass print function with the desired formatting.

Example:

```
//--- print the values of the last 10 bars
   MqlRates rates[];
   if(CopyRates(_Symbol,_Period,1,10,rates))
     {
      ArrayPrint(rates);
      Print("Check\n[time]\t[open]\t[high]\t[low]\t[close]\t[tick_volume]\t[spread]\t[real_volume]");
      for(int i=0;i<10;i++)
        {
         PrintFormat("[%d]\t%s\t%G\t%G\t%G\t%G\t%G\t%G\t%I64d\t",i,
         TimeToString(rates[i].time,TIME_DATE|TIME_MINUTES|TIME_SECONDS),
         rates[i].open,rates[i].high,rates[i].low,rates[i].close,
         rates[i].tick_volume,rates[i].spread,rates[i].real_volume);
        }
     }
   else
      PrintFormat("CopyRates failed, error code=%d",GetLastError());
//--- example of printing
/*
                    [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
   [0] 2016.11.09 04:00:00 1.11242 1.12314 1.11187 1.12295         18110       10   17300175000
   [1] 2016.11.09 05:00:00 1.12296 1.12825 1.11930 1.12747         17829        9   15632176000
   [2] 2016.11.09 06:00:00 1.12747 1.12991 1.12586 1.12744         13458       10    9593492000
   [3] 2016.11.09 07:00:00 1.12743 1.12763 1.11988 1.12194         15362        9   12352245000
   [4] 2016.11.09 08:00:00 1.12194 1.12262 1.11058 1.11172         16833        9   12961333000
   [5] 2016.11.09 09:00:00 1.11173 1.11348 1.10803 1.11052         15933        8   10720384000
   [6] 2016.11.09 10:00:00 1.11052 1.11065 1.10289 1.10528         11888        9    8084811000
   [7] 2016.11.09 11:00:00 1.10512 1.11041 1.10472 1.10915          7284       10    5087113000
   [8] 2016.11.09 12:00:00 1.10915 1.11079 1.10892 1.10904          8710        9    6769629000
   [9] 2016.11.09 13:00:00 1.10904 1.10913 1.10223 1.10263          8956        7    7192138000
   Check
   [time] [open] [high] [low] [close] [tick_volume] [spread] [real_volume]
   [0] 2016.11.09 04:00:00 1.11242 1.12314 1.11187 1.12295 18110 10 17300175000 
   [1] 2016.11.09 05:00:00 1.12296 1.12825 1.1193 1.12747 17829 9 15632176000 
   [2] 2016.11.09 06:00:00 1.12747 1.12991 1.12586 1.12744 13458 10 9593492000 
   [3] 2016.11.09 07:00:00 1.12743 1.12763 1.11988 1.12194 15362 9 12352245000 
   [4] 2016.11.09 08:00:00 1.12194 1.12262 1.11058 1.11172 16833 9 12961333000 
   [5] 2016.11.09 09:00:00 1.11173 1.11348 1.10803 1.11052 15933 8 10720384000 
   [6] 2016.11.09 10:00:00 1.11052 1.11065 1.10289 1.10528 11888 9 8084811000 
   [7] 2016.11.09 11:00:00 1.10512 1.11041 1.10472 1.10915 7284 10 5087113000 
   [8] 2016.11.09 12:00:00 1.10915 1.11079 1.10892 1.10904 8710 9 6769629000 
   [9] 2016.11.09 13:00:00 1.10904 1.10913 1.10223 1.10263 8956 7 7192138000 
*/

```

See also

[FileSave](/en/docs/files/filesave), [FileLoad](/en/docs/files/fileload)
