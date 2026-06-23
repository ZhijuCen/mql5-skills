# Date and time

MQL5 provides a special type for storing time data datetime. As follows from its name, the values of datetime include both the date and time. However, where necessary, they can contain only the date or only the time of day.

Values of this type can be used in programs to monitor events, such as trading hours, news publications, or timeouts for temporarily disabling the EA trading after bad transactions.

The datetime size in memory is 8 bytes. The internal representation of data is completely identical with the ulong type, since the quantity of seconds elapsed since January 1, 1970, is stored inside. The maximum date supported is December 31, 3000.

The datetime constants are recorded as a literal string enclosed in single quotes, preceded by the character 'D'. 6 fields are allocated inside the string, with the numbers for all components of date and time in the following formats:

```
D'YYYY.MM.DD HH:mm:ss'
D'DD.MM.YYYY HH:mm:ss'

```

Here, YYYY means year, MM month, DD day, HH hours, mm minutes, and ss seconds. You can skip either date or time. It is also possible not to specify seconds or minutes with seconds.

For the maximum permitted value of date, a special constant, DATETIME_MAX, is provided in MQL5, equaling to the integer value 0x793406fff, which corresponds with  D"3000.12.31 23:59:59".

Examples of recording the values of the datetime type are shown in file MQL5/Scripts/MQL5Book/p2/TypeDateTime.mq5.

```
void OnStart()
{
  // WARNINGS: invalid date
  datetime blank = D'';           // blank = day of compilation
  datetime noday = D'15:45:00';   // noday = day of compilation + 15:45
  datetime feb30 = D'2021.02.30'; // feb30 = 2021.03.02 00:00:00
  datetime mon22 = D'2021.22.01'; // mon22 = 2022.10.01 00:00:00
  // OK
  datetime dt0 = 0;                      // 1970.01.01 00:00:00
  datetime all = D'2021.01.01 10:10:30'; // 2021.01.01 10:10:30
  datetime day = D'2025.12.12 12';       // 2025.12.12 12:00:00
}

```

The first four variables call the compiler warning about the incorrect date. In the case of blank, the literal is completely empty. In the noday variable, there is no day. In both cases, the compiler substitutes the compilation date in the constant. Variables feb30 and mon22 contain incorrect numbers of the day and month. The compiler corrects them automatically, transferring the overflow into the higher-order field (February 30 turns into March 2, while the 22nd month becomes the 10th month of the subsequent year). However, it is always recommended to get rid of warnings.

Variable dt0 demonstrates the initialization of the datetime value with an integer.

Type datetime supports the set of operations inherent in integers (see [Expressions](/en/book/basis/expressions)). This, for instance, allows adding a predefined quantity of seconds to the time (obtaining a moment in the future) or computing the difference between dates.
