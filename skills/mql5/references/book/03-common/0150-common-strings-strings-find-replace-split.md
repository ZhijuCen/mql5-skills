# Finding, replacing, and extracting string fragments

Perhaps the most popular operations when working with strings are finding and replacing fragments, as well as extracting them. In this section, we will study the MQL5 API functions that will help solve these problems. Examples of their use are summarized in the StringFindReplace.mq5 file.

int StringFind(string value, string wanted, int start = 0)

The function searches for the substring wanted in the string value, starting from the position start. If the substring is found, the function will return the position where it starts, with the characters in the string numbered starting from 0. Otherwise, the function will return -1. Both parameters are passed by value, which allows processing not only variables but also intermediate results of calculations (expressions, function calls).

The search is performed based on a strict match of characters, i.e., it is case-sensitive. If you want to search in a case-insensitive way, you must first convert the source string to a single case using [StringToLower](/en/book/common/strings/strings_case_trim)[ or ](/en/book/common/strings/strings_case_trim)[StringToUpper](/en/book/common/strings/strings_case_trim).

Let's try to count the number of occurrences of the desired substring in the text using StringFind. To do this, let's write a helper function CountSubstring which will call StringFind in a loop, gradually shifting the search starting position in the last parameter start. The loop continues as long as new occurrences of the substring are found.

```
int CountSubstring(const string value, const string wanted)
{
   // indent back because of the increment at the beginning of the loop
   int cursor = -1;
   int count = -1;
   do
   {
      ++count;
      ++cursor; // search continues from the next position
      // get the position of the next substring, or -1 if there are no matches
      cursor = StringFind(value, wanted, cursor);
   }
   while(cursor > -1);
   return count;
}

```

It is important to note that the presented implementation looks for substrings that can overlap. This is because the current position is changed by 1 (++cursor) before it starts looking for the next occurrence. As a result, when searching for, let's say, the substring "AAA" in the string "AAAAA", 3 matches will be found. The technical requirements for searching may differ from this behavior. In particular, there is a practice to continue searching after the position where the previously found fragment ended. In this case, it will be necessary to modify the algorithm so that the cursor moves with a step equal to StringLen(wanted).

Let's call CountSubstring for different arguments in the OnStart function.

```
void OnStart()
{
   string abracadabra = "ABRACADABRA";
   PRT(CountSubstring(abracadabra, "A"));    // 5
   PRT(CountSubstring(abracadabra, "D"));    // 1
   PRT(CountSubstring(abracadabra, "E"));    // 0
   PRT(CountSubstring(abracadabra, "ABRA")); // 2
   ...
}

```

int StringReplace(string &variable, const string wanted, const string replacement)

The function replaces all found wanted substrings with the replacement substring in the variable string.

The function returns the number of replacements made or -1 in case of an error. The error code can be obtained by calling the function [GetLastError](/en/book/common/environment/env_last_error). In particular, these can be out-of-memory errors or the use of an uninitialized string (NULL) as an argument. The variables and wanted parameters must be strings of non-zero length.

When an empty string "" is given as the replacement argument, all occurrences of wanted are simply cut from the original string.

If there were no substitutions, the result of the function is 0.

Let's use the example of StringFindReplace.mq5 to check StringReplace in action.

```
   string abracadabra = "ABRACADABRA";
   ...
   PRT(StringReplace(abracadabra, "ABRA", "-ABRA-")); // 2
   PRT(StringReplace(abracadabra, "CAD", "-"));      // 1
   PRT(StringReplace(abracadabra, "", "XYZ"));      // -1, error
   PRT(GetLastError());      // 5040, ERR_WRONG_STRING_PARAMETER
   PRT(abracadabra);                              // '-ABRA---ABRA-'
   ...

```

Next, using the StringReplace function, let's try to execute one of the tasks encountered in the processing of arbitrary texts. We will try to ensure that a certain separator character is always used as a single character, i.e., sequences of several such characters must be replaced by one. Typically, this refers to spaces between words, but there may be other separators in technical data. Let's test our program for the separator '-'.

We implement the algorithm as a separate function NormalizeSeparatorsByReplace:

```
int NormalizeSeparatorsByReplace(string &value, const ushort separator = ' ')
{
   const string single = ShortToString(separator);
   const string twin = single + single;
   int count = 0;
   int replaced = 0;
   do
   {
      replaced = StringReplace(value, twin, single);
      if(replaced > 0) count += replaced;
   }
   while(replaced > 0);
   return count;
}

```

The program tries to replace a sequence of two separators with one in a do-while loop, and the loop continues as long as the StringReplace function returns values greater than 0 (i.e., there is still something to replace). The function returns the total number of replacements made.

In the function OnStart let's "clear" our inscription from multiple characters '-'.

```
   ...
   string copy1 = "-" + abracadabra + "-";
   string copy2 = copy1;
   PRT(copy1);                                    // '--ABRA---ABRA--'
   PRT(NormalizeSeparatorsByReplace(copy1, '-')); // 4
   PRT(copy1);                                    // '-ABRA-ABRA-'
   PRT(StringReplace(copy1, "-", ""));            // 1
   PRT(copy1);                                    // 'ABRAABRA'
   ...

```

int StringSplit(const string value, const ushort separator, string &result[])

The function splits the passed value string into substrings based on the given separator and puts them into the result array. The function returns the number of received substrings or -1 in case of an error.

If there is no separator in the string, the array will have one element equal to the entire string.

If the source string is empty or NULL, the function will return 0.

To demonstrate the operation of this function, let's solve the previous problem in a new way using StringSplit. To do this, let's write the function NormalizeSeparatorsBySplit.

```
int NormalizeSeparatorsBySplit(string &value, const ushort separator = ' ')
{
   const string single = ShortToString(separator);
   
   string elements[];
   const int n = StringSplit(value, separator, elements);
   ArrayPrint(elements); // debug
   
   StringFill(value, 0); // result will replace original string
   
   for(int i = 0; i < n; ++i)
   {
      // empty strings mean delimiters, and we only need to add them
      // if the previous line is not empty (i.e. not a separator either)
      if(elements[i] == "" && (i == 0 || elements[i - 1] != ""))
      {
         value += single;
      }
      else // all other lines are joined together "as is"
      {
         value += elements[i];
      }
   }
   
   return n;
}

```

When separators occur one after another in the source text, the corresponding element in the output array StringSplit turns out to be an empty string "". Also, an empty string will be at the beginning of the array if the text starts with a separator, and at the end of the array if the text ends with the separator.

To get "cleared" text, you need to add all non-empty strings from the array, "gluing" them with single separator characters. Moreover, only those empty elements in which the previous element of the array is also not empty should be converted into a separator.

Of course, this is only one of the possible options for implementing this functionality. Let's check it in the OnStart function.

```
   ...
   string copy2 = "-" + abracadabra + "-";        // '--ABRA---ABRA--'
   PRT(NormalizeSeparatorsBySplit(copy2, '-'));   // 8
   // debug output of split array (inside function):
   // ""     ""     "ABRA" ""     ""     "ABRA" ""     ""
   PRT(copy2);                                    // '-ABRA-ABRA-'

```

string StringSubstr(string value, int start, int length = -1)

The function extracts from the passed text value a substring starting at the specified position start, of the length length. The starting position can be from 0 to the length of the string minus 1. If the length length is -1 or more than the number of characters from start to the end of the string, the rest of the string will be extracted in full.

The function returns a substring or an empty string if the parameters are incorrect.

Let's see how it works.

```
   PRT(StringSubstr("ABRACADABRA", 4, 3));        // 'CAD'
   PRT(StringSubstr("ABRACADABRA", 4, 100));      // 'CADABRA'
   PRT(StringSubstr("ABRACADABRA", 4));           // 'CADABRA'
   PRT(StringSubstr("ABRACADABRA", 100));         // ''

```
