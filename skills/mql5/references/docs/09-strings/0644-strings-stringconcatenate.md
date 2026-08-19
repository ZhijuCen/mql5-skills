# StringConcatenate

The function forms a string of passed parameters and returns the size of the formed string. Parameters can be of any type. Number of parameters can't be less than 2 or more than 64.

```
int  StringConcatenate(
   string&  string_var,   // string to form
   void argument1         // first parameter of any simple type
   void argument2         // second parameter of any simple type
   ...                    // next parameter of any simple type
   );

```

Parameters

string_var

[out]  String that will be formed as a result of concatenation.

argumentN

[in]  Any comma separated values. From 2 to 63 parameters of any simple type.

Return Value

Returns the string length, formed by concatenation of parameters transformed into string type. Parameters are transformed into strings according to the same rules as in [Print()](/en/docs/common/print) and [Comment()](/en/docs/common/comment).

Example:

```
void OnStart()
  {
//--- declare and define variables participating in concatenation
   string text="";
   string text1="This script shows how the StringConcatenate() function works.\n";
   string text2="This is the second line, at the end of which there is a line break control code.\n";
   string text3="This is line number ";
   int    num3=3;
   string text31=", the number of which is entered into the function as a separate parameter.";
   string textN="\n";
   string text4="This is line number 4, preceded by a separate parameter with a line break code.";
   int    length=StringConcatenate(text, text1, text2, text3, num3, text31, textN, text4, "\nLine 5 includes a real number: ", 0.12345);
   Print(text, "\nLength of the resulting string = ", length);
   
   /*
   Result
   This script shows how the StringConcatenate() function works.
   This is the second line, at the end of which there is a line break control code.
   This is line number 3, the number of which is entered into the function as a separate parameter.
   This is line number 4, preceded by a separate parameter with a line break code.
   Line 5 includes a real number: 0.12345
   Length of the resulting string = 358
   */
  }

```

See also

[StringAdd](/en/docs/strings/stringadd), [StringSplit](/en/docs/strings/stringsplit), [StringSubstr](/en/docs/strings/stringsubstr)
