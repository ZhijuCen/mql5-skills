# Changing the character case and trimming spaces

Working with texts often implies the use of some standard operations, such as converting all characters to upper or lower case and removing extra empty characters (for example, spaces) at the beginning or end of a string. For these purposes, the MQL5 API provides four corresponding functions. All of them modify the string in place, that is, directly in the available buffer (if it is already allocated).

The input parameter of all functions is a reference to a string, i.e., only variables (not expressions) can be passed to them, and not constant variables since the functions involve modifying the argument.

The test script for all functions follows the relevant descriptions.

bool StringToLower(string &variable)

bool StringToUpper(string &variable)

The functions convert all characters of the specified string to the appropriate case: StringToLower to lowercase letters, and StringToUpper to uppercase. This includes support for national languages available at the Windows system level.

If successful, it returns true. In case of an error, it returns false.

int StringTrimLeft(string &variable)

int StringTrimRight(string &variable)

The function removes carriage return ('\r'), line feed ('\n'), spaces (' '), tabs ('\t') and some other non-displayable characters at the beginning (for StringTrimLeft) or end (for StringTrimRight) of a string. If there are empty spaces inside the string (between the displayed characters), they will be preserved.

The function returns the number of characters removed.

The StringModify.mq5 file demonstrates the operation of the above functions.

```
void OnStart()
{
   string text = "  \tAbCdE F1  ";
               // ↑        ↑  ↑
               // |        |  └2 spaces
               // |        └space
               // └2 spaces and tab
   PRT(StringToLower(text));   // 'true'
   PRT(text);                  // '  \tabcde f1  '
   PRT(StringToUpper(text));   // 'true'
   PRT(text);                  // '  \tABCDE F1  '
   PRT(StringTrimLeft(text));  // '3'
   PRT(text);                  // 'ABCDE F1  '
   PRT(StringTrimRight(text)); // '2'
   PRT(text);                  // 'ABCDE F1'
   PRT(StringTrimRight(text)); // '0'  (there is nothing else to delete)
   PRT(text);                  // 'ABCDE F1'
                               //       ↑
                               //       └the space inside remains
   
   string russian = "Russian text";
   PRT(StringToUpper(russian));  // 'true'
   PRT(russian);                 // 'RUSSIAN TEXT'  
   string german = "straßenführung";
   PRT(StringToUpper(german));   // 'true'
   PRT(german);                  // 'STRAßENFÜHRUNG'
}

```
