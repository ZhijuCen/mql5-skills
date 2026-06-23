# Logging messages

Logging is the most common way to inform the user of current information about the program's operation. This may be the status of a regular completion, an indication of progress during a long calculation, or debugging data for finding and reproducing errors.

Unfortunately, no programmer is immune to errors in their code. Therefore, developers usually try to leave the so-called "breadcrumb trail": logging the main stages of program execution (at least, the sequence of function calls).

We are already familiar with two logging functions − Print and PrintFormat. We used them in the examples in previous sections. We had to "put them into use" ahead of time in a simplified mode since it is almost impossible to do without them.

One function call generates, as a rule, one record. However, if a newline character ('\n') is encountered in the output string, it will split the information into two parts.

Note that all Print and PrintFormat calls are transformed into log entries on the Experts tab of the Toolbox window. Although the tab is called Experts, it collects the results of all print instructions, regardless of the [MQL program type](/en/book/applications/runtime/runtime_features_by_progtype).

Logs are stored in files organized according to the principle "one day = one file": they have the names YYYYMMDD.log (Y for year, M for month, and D for day). Files are located in <data directory>/MQL5/Logs (do not confuse them with the terminal system logs in the folder <data directory>/Logs).

Note that during bulk logging (if Print function calls generate a large amount of information in a short time), the terminal displays only some entries in the window. This is done to optimize performance. In addition, the user is in any case not able to see all the messages on the go. In order to see the full version of the log, you need to run the View command of the context menu. As a result, a window with a log will open.  

   

It should also be kept in mind that information from the log is cached when written to disk, that is, it is written to files in large blocks in a lazy mode, which is why at any given time the log file, as a rule, does not contain the most recent entries (although they are visible in a window). To initiate a cache flush to the disk, you can run the command View or Open in the log context menu.

Each log entry is preceded by a time to the nearest millisecond, as well as the name of the program (and its graphics) that generated or caused this message.

void Print(argument, ...)

The function prints one or more values to the expert log, in one line (if the output data does not contain the character '\n').

Arguments can be of any [built-in type](/en/book/basis/builtin_types). They are separated by commas. The number of parameters cannot exceed 64. Their variable number is indicated by an ellipsis in the prototype, but MQL5 does not allow you to describe your own functions with a similar characteristic: only some built-in API functions have a variable number of parameters (in particular, [StringFormat](/en/book/common/strings/strings_format), Print, PrintFormat, and [Comment](/en/book/common/output/output_comment)).

For structures and classes, you should implement a built-in print method, or display their fields separately.

Also, the function is not capable of handling arrays. You can display them element by element, or use the function [ArrayPrint](/en/book/common/arrays/arrays_print).

Values of type double are output by the function with an accuracy of up to 16 significant digits (together in the mantissa and the fractional part). A number can be displayed in either traditional or scientific format (with an exponent), whichever is more compact. Values of type float are displayed with an accuracy of 7 decimal places. To display real numbers with a different precision, or to explicitly specify the format, you must use the PrintFormat function.

Values of type bool output as the strings "true" or "false".

Dates are displayed with the day and time specified with maximum accuracy (up to a second), in the format "YYYY.MM.DD hh:mm:ss". To display the date in a different format, use the TimeToString function (see section [Date and time](/en/book/common/conversions/conversions_datetime)).

Enumeration values are displayed as integers. To display element names use the EnumToString function (see section [Enumerations](/en/book/common/conversions/conversions_enums)).

Single-byte and double-byte characters are also output as integers. To display symbols as characters or letters, use the functions CharToString or ShortToString see section [Working with symbols and code pages](/en/book/common/strings/strings_codepages)).

Values of the color type are displayed either as a string with a triple of numbers indicating the intensity of each color component ("R, G, B") or as a color name if this color is present in the color set.

For more information about converting values of different types to strings, see the chapter [Data Conversion of Built-in Types](/en/book/common/conversions) (particularly in sections [Numbers to strings and vice versa](/en/book/common/conversions/conversions_numbers), [Date and time](/en/book/common/conversions/conversions_datetime), [Color](/en/book/common/conversions/conversions_color)).

When working in the strategy tester in single pass mode ([testing](/en/book/common/environment/env_mode) Expert Advisor or indicator), results of the function Print are output to the test agent log.

When working in the strategy tester in the mode [optimization](/en/book/common/environment/env_mode), logging is suppressed for performance reasons, so the Print function has no visible effect. However, all expressions given as arguments are evaluated.

All arguments, after being converted to a string representation, are concatenated into one common string without any delimiter characters. If required, such characters must be explicitly written in the argument list. For example,

```
int x;
bool y;
datetime z;
...
Print(x, ", ", y, ", ", z);

```

Here, 3 variables are logged, separated by commas. If it were not for the intermediate literals ", ", the values of the variables would be stuck together in the log entry.

Lots of cases of applying Print can be found starting from the very first sections of the book (for example, [First program](/en/book/intro/first_program), [Assignment and initialization, expressions and arrays](/en/book/intro/init_assign_express), and in others).

As a new way of working with Print we will implement a simple class that will allow you to display a sequence of arbitrary values without specifying a separator character between each neighboring value. We use the '<<' operator overload approach, similar to what is used in the C++ I/O streams (std::cout).

The class definition will be placed in a separate header file OutputStream.mqh. A class is shown below in a simplified form.

```
class OutputStream
{
protected:
   ushort delimiter;
   string line;
   
   // add the next argument, separated by a separator (if any)
   void appendWithDelimiter(const string v)
   {
      line += v;
      if(delimiter != 0)
      {
         line += ShortToString(delimiter);
      }
   }
   
public:
   OutputStream(ushort d = 0): delimiter(d) { }
   
   template<typename T>
   OutputStream *operator<<(const T v)
   {
      appendWithDelimiter((string)v);
      return &this;
   }
   
   OutputStream *operator<<(OutputStream &self)
   {
      if(&this == &self)
      {
         print(line);// output of the composed string
         line = NULL;
      }
      return &this;
   }
};

```

Its point is to accumulate in a string variable line string representations of any arguments passed using the '<<' operator. If a separator character is specified in the class constructor, it will automatically be inserted between the arguments. Since the overloaded operator returns a pointer to an object, we can chainpass a sequence of arguments:

```
OutputStream out(',');
out << x << y << z << out;

```

As an attribute of the end of data collection, and for the actual output of the content line into the log, an overload of the same operator for the object itself is used.

The real class is somewhat more complicated. In particular, it allows you to set not only the separator character but also the accuracy of displaying real numbers, as well as flags for selecting fields in date and time values. In addition, the class supports character printing, ushort, in the form of characters (instead of integer codes), the simplified output of arrays (into a separate string), colors in hexadecimal format as a single value (and not a triple of numbers separated by commas, since the comma is often used as a separator character, and then the color components in the log look like 3 different variables).

A demonstration of using the class is given in the script OutputStream.mq5.

```
void OnStart()
{
   OutputStream os(5, ',');
   
   bool b = true;
   datetime dt = TimeCurrent();
   color clr = C'127, 128, 129';
   int array[] = {100, 0, -100};
   os << M_PI << "text" << clrBlue << b << array << dt << clr << '@' << os;
   
   /*
      output example
      
      3.14159,text,clrBlue,true
      [100,0,-100]
      2021.09.07 17:38,clr7F8081,@
   */
}

```

void PrintFormat(const string format, ...) ≡ void printf(const string format, ...)

The function logs a set of arguments based on the specified format string. The format parameter not only provides a free text output string template that is displayed "as is", but can also contain escape sequences that describe how specific arguments are to be formatted.

The total number of parameters, including the format string, cannot exceed 64. Restrictions on parameter types are similar to functions print.

PrintFormat working and formatting principles are identical to those described for the StringFormat function (see section [Universal formatted data output to a string](/en/book/common/strings/strings_format)). The only difference is that StringFormat returns the formed string to the calling code, and print format sends to the journal. We can say that PrintFormat has the following conditional equivalent:

```
Print(StringFormat(<list of arguments as is, including format>))

```

In addition to the full name PrintFormat you can use a shorter alias printf.

Like the Print function, PrintFormat has some specific features when working in the tester in the optimization mode: its output to the log is suppressed to improve performance.

We have already met in many sections scripts that use PrintFormat, for example, [Return transition](/en/book/basis/statements/statements_return), [Color](/en/book/common/conversions/conversions_color), [Dynamic arrays](/en/book/common/arrays/arrays_dynamic), [File descriptor management](/en/book/common/files/files_handles), [Getting a list of global variables](/en/book/common/globals/globals_list).
