# Writing and reading variables (text files)

Text files have their own set of functions for atomic (element-by-element) saving and for reading data. It is slightly different from the binary files set in the previous section. It should also be noted that there are no analog functions for writing/reading a structure or an array of structures to a text file. If you try to use any of these functions with a text file, they will have no effect but will raise an internal error code of 5011 (FILE_NOTBIN).

As we already know, text files in MQL5 have two forms: plain text and text in CSV format. The corresponding mode, FILE_TXT or FILE_CSV, is set when the file is opened and cannot be changed without closing and reacquiring the handle. The difference between them appears only when reading files. Both modes are recorded in the same way.

In the TXT mode, each call to the read function (any of the functions we'll look at in this section) finds the next newline in the file (a '\n' character or a pair of '\r\n') and processes everything up to it. The point of processing is to convert the text from the file into a value of a specific type corresponding to the called function. In the simplest case, if the FileReadString function is called, no processing is performed (the string is returned "as is").

In the CSV mode, each time the read function is called, the text in the file is logically split not only by newlines but also by an additional delimiter specified when opening the file. The rest of the processing of the fragment from the current position of the file to the nearest delimiter is similar.

In other words, reading the text and transferring the internal position within the file is done in fragments from delimiter to delimiter, where delimiter means not only the delimiter character in the FileOpen parameter list but also a newline ('\n', '\r\n'), as well as the beginning and end of the file.

The additional delimiter has the same effect on writing text to FILE_TXT and FILE_CSV files, but only when using the FileWrite function: it automatically inserts this character between the recorded elements. The FileWriteString function separator is ignored.

Let's view the formal descriptions of the functions, and then consider an example in FileTxtCsv.mq5.

uint FileWrite(int handle, ...)

The function belongs to the category of functions that take a variable number of parameters. Such parameters are indicated in the function prototype with an ellipsis. Only built-in data types are supported. To write structures or class objects, you must dereference their elements and pass them individually.

The function writes all arguments passed after the first one to a text file with the handle descriptor. Arguments are separated by commas, as in a normal argument list. The number of arguments output to the file cannot exceed 63.

When output, numeric data is converted to text format according to the rules of the standard conversion to (string). Values or type double output to 16 significant digits, either in traditional format or scientific exponent format (the more compact option is chosen). Data of the float type is displayed with an accuracy of 7 significant digits. To display real numbers with a different precision or in an explicitly specified format, use the DoubleToString function (see [Numbers to strings and vice versa](/en/book/common/conversions/conversions_numbers)).

Values of the datetime type are output in the format "YYYY.MM.DD hh:mm:ss" (see [Date and time](/en/book/common/conversions/conversions_datetime)).

A standard color (from the list of web colors) is displayed as a name, a non-standard color is displayed as a triple of RGB component values (see [Color](/en/book/common/conversions/conversions_color)), separated by commas (note: comma is the most common separator character in CSV).

For enumerations, an integer denoting the element is displayed instead of its identifier (name). For example, when writing FRIDAY (from ENUM_DAY_OF_WEEK, see [Enumerations](/en/book/basis/builtin_types/enums)) we get number 5 in the file.

Values of the bool type are output as the strings "true" or "false".

If a delimiter character other than 0 was specified when opening the file, it will be inserted between two adjacent lines resulting from the conversion of the corresponding arguments.

Once all arguments are written to the file, a line terminator '\r\n' is added.

The function returns the number of bytes written, or 0 in case of an error.

uint FileWriteString(int handle, const string text, int length = -1)

The function writes the text string parameter to a text file with the handle descriptor. The length parameter is only applicable for binary files and is ignored in this context (the line is written in full).

The FileWriteString function can also work with binary files. This application of the function is described in the previous section.

Any separators (between elements in a line) and newlines must be inserted/added by the programmer.

The function returns the number of bytes written (in FILE_UNICODE mode this will be 2 times the length of the string in characters) or 0 in case of an error.

string FileReadString(int handle, int length = -1)

The function reads a string up to the next delimiter from a file with the handle descriptor (delimiter character in a CSV file, linefeed character in any file, or until the end of the file). The length parameter only applies to binary files and is ignored in this context.

The resulting string can be converted to a value of the required type using standard [reduction rules](/en/book/basis/conversion/conversion_explicit) or using [conversion functions](/en/book/common/conversions). Alternatively, specialized read functions can be used: FileReadBool, FileReadDatetime, FileReadNumber are described below.

In case of an error, an empty string will be returned. The error code can be found through the variable _LastError or function [GetLastError](/en/book/common/environment/env_last_error). In particular, when the end of the file is reached, the error code will be 5027 (FILE_ENDOFFILE).

bool FileReadBool(int handle)

The function reads a fragment of a CSV file up to the next delimiter, or until the end of the line and converts it to a value of type bool. If the fragment contains the text "true" (in any case, including mixed case, for example, "True"), or a non-zero number, we get true. In other cases, we get false.

The word "true" must occupy the entire read element. Even if the string starts with "true", but has a continuation (for example, "True Volume"), we get false.

datetime FileReadDatetime(int handle)

The function reads from a CSV file a string of one of the following formats: "YYYY.MM.DD hh:mm:ss", "YYYY.MM.DD" or "hh:mm:ss", and converts it to a value of the datetime type. If the fragment does not contain a valid textual representation of the date and/or time, the function will return zero or "weird" time, depending on what characters it can interpret as date and time fragments. For empty or non-numeric strings, we get the current date with zero time.

More flexible date and time reading (with more formats supported) can be achieved by combining two functions: StringToTime(FileReadString(handle)). For further details about StringToTime see [Date and time](/en/book/common/conversions/conversions_datetime).

double FileReadNumber(int handle)

The function reads a fragment from the CSV file up to the next delimiter or until the end of the line, and converts it to a value of type double according to standard [type casting](/en/book/common/conversions/conversions_numbers) rules.

Please note that the double may lose the precision of very large values, which can affect the reading of large numbers of types long/ulong (the value after which integers inside double are distorted is 9007199254740992: an example of such a phenomenon is given in the section [Unions](/en/book/oop/structs_and_unions/unions)).

Functions discussed in the previous section, including FileReadDouble, FileReadFloat, FileReadInteger, FileReadLong, and FileReadStruct, cannot be applied to text files.

The FileTxtCsv.mq5 script demonstrates how to work with text files. Last time we uploaded quotes to a binary file. Now let's do it in TXT and CSV formats.

Basically, MetaTrader 5 allows you to export and import quotes in CSV format from the "Symbols" dialog. But for educational purposes, we will reproduce this process. In addition, the software implementation allows you to deviate from the exact format that is generated by default. A fragment of the XAUUSD H1 history exported in the standard way is shown below.

```
<DATE> » <TIME> » <OPEN> » <HIGH> » <LOW> » <CLOSE> » <TICKVOL> » <VOL> » <SPREAD>
2021.01.04 » 01:00:00 » 1909.07 » 1914.93 » 1907.72 » 1913.10 » 4230 » 0 » 5
2021.01.04 » 02:00:00 » 1913.04 » 1913.64 » 1909.90 » 1913.41 » 2694 » 0 » 5
2021.01.04 » 03:00:00 » 1913.41 » 1918.71 » 1912.16 » 1916.61 » 6520 » 0 » 5
2021.01.04 » 04:00:00 » 1916.60 » 1921.89 » 1915.49 » 1921.79 » 3944 » 0 » 5
2021.01.04 » 05:00:00 » 1921.79 » 1925.26 » 1920.82 » 1923.19 » 3293 » 0 » 5
2021.01.04 » 06:00:00 » 1923.20 » 1923.71 » 1920.24 » 1922.67 » 2146 » 0 » 5
2021.01.04 » 07:00:00 » 1922.66 » 1922.99 » 1918.93 » 1921.66 » 3141 » 0 » 5
2021.01.04 » 08:00:00 » 1921.66 » 1925.60 » 1921.47 » 1922.99 » 3752 » 0 » 5
2021.01.04 » 09:00:00 » 1922.99 » 1925.54 » 1922.47 » 1924.80 » 2895 » 0 » 5
2021.01.04 » 10:00:00 » 1924.85 » 1935.16 » 1924.59 » 1932.07 » 6132 » 0 » 5

```

Here, in particular, we may not be satisfied with the default separator character (tab, denoted as '"'), the order of the columns, or the fact that the date and time are divided into two fields.

In our script, we will choose comma as a separator, and we will generate the columns in the order of the fields of the MqlRates structure. Unloading and subsequent test reading will be performed in the FILE_TXT and FILE_CSV modes.

```
const string txtfile = "MQL5Book/atomic.txt";
const string csvfile = "MQL5Book/atomic.csv";
const short delimiter = ',';

```

Quotes will be requested at the beginning of the function OnStart in the standard way:

```
void OnStart()
{
   MqlRates rates[];   
   int n = PRTF(CopyRates(_Symbol, _Period, 0, 10, rates)); // 10

```

We will specify the names of the columns in the array separately, and also combine them using the helper function StringCombine. Separate titles are required because we combine them into a common title using a selectable delimiter character (an alternative solution could be based on StringReplace). We encourage you to work with the source code StringCombine independently: it does the opposite operation with respect to the built-in [StringSplit](/en/book/common/strings/strings_find_replace_split).

```
   const string columns[] = {"DateTime", "Open", "High", "Low", "Close", 
                             "Ticks", "Spread", "True"};
   const string caption = StringCombine(columns, delimiter) + "\r\n";

```

The last column should have been called "Volume", but we will use its example to check the performance of the function FileReadBool. You may assume that the current name implies "True Volume" (but such a string would not be interpreted as true).

Next, let's open two files in the FILE_TXT and FILE_CSV modes, and write the prepared header into them.

```
   int fh1 = PRTF(FileOpen(txtfile, FILE_TXT | FILE_ANSI | FILE_WRITE, delimiter));//1
   int fh2 = PRTF(FileOpen(csvfile, FILE_CSV | FILE_ANSI | FILE_WRITE, delimiter));//2
  
   PRTF(FileWriteString(fh1, caption)); // 48
   PRTF(FileWriteString(fh2, caption)); // 48

```

Since the FileWriteString function does not automatically add a newline, we have added "\r\n" to the caption variable.

```
   for(int i = 0; i < n; ++i)
   {
      FileWrite(fh1, rates[i].time, 
         rates[i].open, rates[i].high, rates[i].low, rates[i].close, 
         rates[i].tick_volume, rates[i].spread, rates[i].real_volume);
      FileWrite(fh2, rates[i].time, 
         rates[i].open, rates[i].high, rates[i].low, rates[i].close, 
         rates[i].tick_volume, rates[i].spread, rates[i].real_volume);
   }
   
   FileClose(fh1);
   FileClose(fh2);

```

Writing structure fields from the rates array is done in the same way, by calling FileWrite in a loop for each of the two files. Recall that the FileWrite function automatically inserts a delimiter character between arguments and adds "\r\n" at the string ends. Of course, it was possible to independently convert all output values to strings and send them to a file using FileWriteString, but then we would have to take care of separators and newlines ourselves. In some cases, they are not needed, for example, if you are writing in JSON format in a compact form (essentially in one giant line).

Thus, at the recording stage, both files were managed in the same way and turned out to be the same. Here is an example of their content for XAUUSD,H1 (your results may vary):

```
DateTime,Open,High,Low,Close,Ticks,Spread,True
2021.08.19 12:00:00,1785.3,1789.76,1784.75,1789.06,4831,5,0
2021.08.19 13:00:00,1789.06,1790.02,1787.61,1789.06,3393,5,0
2021.08.19 14:00:00,1789.08,1789.95,1786.78,1786.89,3536,5,0
2021.08.19 15:00:00,1786.78,1789.86,1783.73,1788.82,6840,5,0
2021.08.19 16:00:00,1788.82,1792.44,1782.04,1784.02,9514,5,0
2021.08.19 17:00:00,1784.04,1784.27,1777.14,1780.57,8526,5,0
2021.08.19 18:00:00,1780.55,1784.02,1780.05,1783.07,5271,6,0
2021.08.19 19:00:00,1783.06,1783.15,1780.73,1782.59,3571,7,0
2021.08.19 20:00:00,1782.61,1782.96,1780.16,1780.78,3236,10,0
2021.08.19 21:00:00,1780.79,1780.9,1778.54,1778.65,1017,13,0

```

Differences in working with these files will begin to appear at the reading stage.

Let's open a text file for reading and "scan" it using the FileReadString function in a loop, until it returns an empty string (i.e., until the end of the file).

```
   string read;
   fh1 = PRTF(FileOpen(txtfile, FILE_TXT | FILE_ANSI | FILE_READ, delimiter)); // 1
   Print("===== Reading TXT");
   do
   {
      read = PRTF(FileReadString(fh1));
   }
   while(StringLen(read) > 0);

```

The log will show something like this:

```
===== Reading TXT
FileReadString(fh1)=DateTime,Open,High,Low,Close,Ticks,Spread,True / ok
FileReadString(fh1)=2021.08.19 12:00:00,1785.3,1789.76,1784.75,1789.06,4831,5,0 / ok
FileReadString(fh1)=2021.08.19 13:00:00,1789.06,1790.02,1787.61,1789.06,3393,5,0 / ok
FileReadString(fh1)=2021.08.19 14:00:00,1789.08,1789.95,1786.78,1786.89,3536,5,0 / ok
FileReadString(fh1)=2021.08.19 15:00:00,1786.78,1789.86,1783.73,1788.82,6840,5,0 / ok
FileReadString(fh1)=2021.08.19 16:00:00,1788.82,1792.44,1782.04,1784.02,9514,5,0 / ok
FileReadString(fh1)=2021.08.19 17:00:00,1784.04,1784.27,1777.14,1780.57,8526,5,0 / ok
FileReadString(fh1)=2021.08.19 18:00:00,1780.55,1784.02,1780.05,1783.07,5271,6,0 / ok
FileReadString(fh1)=2021.08.19 19:00:00,1783.06,1783.15,1780.73,1782.59,3571,7,0 / ok
FileReadString(fh1)=2021.08.19 20:00:00,1782.61,1782.96,1780.16,1780.78,3236,10,0 / ok
FileReadString(fh1)=2021.08.19 21:00:00,1780.79,1780.9,1778.54,1778.65,1017,13,0 / ok
FileReadString(fh1)= / FILE_ENDOFFILE(5027)

```

Every call of FileReadString reads the entire line (up to '\r\n') in the FILE_TXT mode. To separate it into elements, we should implement additional processing. Optionally, we can use the FILE_CSV mode.

Let's do the same for the CSV file.

```
   fh2 = PRTF(FileOpen(csvfile, FILE_CSV | FILE_ANSI | FILE_READ, delimiter)); // 2
   Print("===== Reading CSV");
   do
   {
      read = PRTF(FileReadString(fh2));
   }
   while(StringLen(read) > 0);

```

This time there will be many more entries in the log:

```
===== Reading CSV
FileReadString(fh2)=DateTime / ok
FileReadString(fh2)=Open / ok
FileReadString(fh2)=High / ok
FileReadString(fh2)=Low / ok
FileReadString(fh2)=Close / ok
FileReadString(fh2)=Ticks / ok
FileReadString(fh2)=Spread / ok
FileReadString(fh2)=True / ok
FileReadString(fh2)=2021.08.19 12:00:00 / ok
FileReadString(fh2)=1785.3 / ok
FileReadString(fh2)=1789.76 / ok
FileReadString(fh2)=1784.75 / ok
FileReadString(fh2)=1789.06 / ok
FileReadString(fh2)=4831 / ok
FileReadString(fh2)=5 / ok
FileReadString(fh2)=0 / ok
...
FileReadString(fh2)=2021.08.19 21:00:00 / ok
FileReadString(fh2)=1780.79 / ok
FileReadString(fh2)=1780.9 / ok
FileReadString(fh2)=1778.54 / ok
FileReadString(fh2)=1778.65 / ok
FileReadString(fh2)=1017 / ok
FileReadString(fh2)=13 / ok
FileReadString(fh2)=0 / ok
FileReadString(fh2)= / FILE_ENDOFFILE(5027)

```

The point is that the FileReadString function in the FILE_CSV mode takes into account the delimiter character and splits the strings into elements. Every FileReadString call returns a single value (cell) from a CSV table. Obviously, the resulting strings need to be subsequently converted to the appropriate types.

This problem can be solved in a generalized form using specialized functions FileReadDatetime, FileReadNumber, FileReadBool. However, in any case, the developer must keep track of the number of the current readable column and determine its practical meaning. An example of such an algorithm is given in the third step of the test. It uses the same CSV file (for simplicity, we close it at the end of each step and open it at the beginning of the next one).

To simplify the assignment of the next field in the MqlRates structure by the column number, we have created a child structure MqlRates that contains one template method set:

```
struct MqlRatesM : public MqlRates
{
   template<typename T>
   void set(int field, T v)
   {
      switch(field)
      {
         case 0: this.time = (datetime)v; break;
         case 1: this.open = (double)v; break;
         case 2: this.high = (double)v; break;
         case 3: this.low = (double)v; break;
         case 4: this.close = (double)v; break;
         case 5: this.tick_volume = (long)v; break;
         case 6: this.spread = (int)v; break;
         case 7: this.real_volume = (long)v; break;
      }
   }
};

```

In the OnStart function, we have described an array of one such structure, where we will add the incoming values. The array was required to simplify logging with ArrayPrint (there is no ready-made function in MQL5 for printing a structure by itself).

```
   Print("===== Reading CSV (alternative)");
   MqlRatesM r[1];
   int count = 0;
   int column = 0;
   const int maxColumn = ArraySize(columns);

```

The count variable that counts the records was required not only for statistics but also as a means to skip the first line, which contains headers and not data. The current column number is tracked in the column variable. Its maximum value should not exceed the number of columns maxColumn.

Now we only have to open the file and read elements from it in a loop using various functions until an error occurs, in particular, an expected error such as 5027 (FILE_ENDOFFILE), that is, the end of the file is reached.

When the column number is 0, we apply the FileReadDatetime function. For other columns use FileReadNumber. The exception is the case of the first line with headers: for this we call the FileReadBool function to demonstrate how it would react to the "True" header that was deliberately added to the last column.

```
   fh2 = PRTF(FileOpen(csvfile, FILE_CSV | FILE_ANSI | FILE_READ, delimiter)); // 1
   do
   {
      if(column)
      {
         if(count == 1) // demo for FileReadBool on the 1st record with headers
         {
            r[0].set(column, PRTF(FileReadBool(fh2)));
         }
         else
         {
            r[0].set(column, FileReadNumber(fh2));
         }
      }
      else // 0th column is the date and time
      {
         ++count;
         if(count >1) // the structure from the previous line is ready
         {
            ArrayPrint(r, _Digits, NULL, 0, 1, 0);
         }
         r[0].time = FileReadDatetime(fh2);
      }
      column = (column + 1) % maxColumn;
   }
   while(_LastError == 0); // exit when end of file 5027 is reached (FILE_ENDOFFILE)
   
   // printing the last structure
   if(column == maxColumn - 1)
   {
      ArrayPrint(r, _Digits, NULL, 0, 1, 0);
   }

```

This is what is logged:

```
===== Reading CSV (alternative)
FileOpen(csvfile,FILE_CSV|FILE_ANSI|FILE_READ,delimiter)=1 / ok
FileReadBool(fh2)=false / ok
FileReadBool(fh2)=false / ok
FileReadBool(fh2)=false / ok
FileReadBool(fh2)=false / ok
FileReadBool(fh2)=false / ok
FileReadBool(fh2)=false / ok
FileReadBool(fh2)=true / ok
2021.08.19 00:00:00   0.00   0.00  0.00    0.00          0     0       1
2021.08.19 12:00:00 1785.30 1789.76 1784.75 1789.06       4831     5       0
2021.08.19 13:00:00 1789.06 1790.02 1787.61 1789.06       3393     5       0
2021.08.19 14:00:00 1789.08 1789.95 1786.78 1786.89       3536     5       0
2021.08.19 15:00:00 1786.78 1789.86 1783.73 1788.82       6840     5       0
2021.08.19 16:00:00 1788.82 1792.44 1782.04 1784.02       9514     5       0
2021.08.19 17:00:00 1784.04 1784.27 1777.14 1780.57       8526     5       0
2021.08.19 18:00:00 1780.55 1784.02 1780.05 1783.07       5271     6       0
2021.08.19 19:00:00 1783.06 1783.15 1780.73 1782.59       3571     7       0
2021.08.19 20:00:00 1782.61 1782.96 1780.16 1780.78       3236    10       0
2021.08.19 21:00:00 1780.79 1780.90 1778.54 1778.65       1017    13       0

```

As you see, of all the headers, only the last one is converted to the true value, and all the previous ones are false.

The content of the read structures is the same as the original data.
