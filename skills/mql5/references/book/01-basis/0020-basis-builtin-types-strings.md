# String type

String type is intended for storing text-based information and is marked by keyword string. String is a sequence of the ushort characters and supports the complete Unicode range, including multiple national scripts. For instance, names of financial instruments and comments in trading orders are strings.

By reason of the specific nature of strings, their size is a variable value that is equal to the doubled length of the text (quantity of characters multiplied by the "width" of a character, i.e., 2 bytes) plus one more character. This additional character is intended for the 'terminating zero' (a char coded as 0) that denotes the end of the line. Moreover, MQL5 uses some space to store service information, i.e., a reference to the place in memory where the string starts.

Unlike C++, no address of a string or any other variable can be obtained in MQL5. Direct memory access is prohibited in MQL5.

A string literal is recorded in the source code as a sequence of characters embedded in double-quotes. For example: "EURUSD" or "$". We should distinguish between strings consisting of one character, like "$", and the same single characters, like '$'. These are different data types.

An empty string appears as "". Considering the implicit terminating zero, it consumes 2 bytes, apart from service information.

Should it be necessary to use the double quote character inside the string, it must be preceded by the backslash character, transforming into a control sequence, such as "Press \"OK\"".

String initialization examples are given in script MQL5/Scripts/MQL5Book/p2/TypeString.mq5.

```
void OnStart()
{
   string h = "Hello";          // Hello
   string b = "Press \"OK\"";   // Press "OK"
   string z = "";               //
   string t = "New\nLine";      // New
                                // Line
   string n = "123";            // 123, text (not an integer value)
   string m = "very long message "
              "can be presented " 
              "by parts";
   // equivalent:
   // string m = "very long message can be presented by parts"; 
}

```

The string "Hello" is placed in variable h.

Text containing double quotes is written in variable b.

Variable z is initialized by an empty string. This is basically equivalent to describing z without initialization, but there are some finer points here. Further, as the text goes, in the section of [Initialization of variables](/en/book/basis/variables/initialization), we will get to know that uninitialized strings get a special value, NULL, unlike "", for which, as previously stated, the memory is allocated for the terminating zero. This difference affects the execution of string [comparison operators](/en/book/basis/expressions/operators_relational) and some others. As the story unfolds, we will touch upon all such aspects.

Variable t will get a text that, when printed in the log using the Print function or displayed by other methods, will be divided into 2 strings.

String "123" recorded in variable n is not a number, although it looks like that. There are some functions in MQL5 to convert text into numbers and back (see section [Data transformation](/en/book/common/conversions/conversions_numbers)). Moreover, there is a separate set of functions for [working with strings](/en/book/common/strings).

For convenience, long literals can be written in several strings, as for variable m. The general rule is as follows: All literals up to the semicolon that marks the end of the variable description are merged by the compiler. In such formatting, the key is not to forget to add an intervening space inside each fragment of the string, if necessary (for instance, to separate the words in the message as in the example above).

For strings, the summation (concatenation) operation is defined, denoted with the character '+'. We will discuss it in the chapter dealing with expressions (see [Arithmetic operations](/en/book/basis/expressions/operators_arithmetic)).

String characters can be read separately, referring to them as array elements (see [Use of arrays](/en/book/basis/arrays/arrays_usage)): If s is a string, then s[i] is the code of the ith character in it, type ushort.
