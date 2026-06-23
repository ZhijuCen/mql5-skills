# String comparison

To compare strings in MQL5, you can use the standard [comparison operators](/en/book/basis/expressions/operators_relational), in particular '==', '!=', '>', '<'. All such operators conduct comparisons in a character-by-character, case-sensitive manner.

Each character has a Unicode code which is an integer of type ushort. Accordingly, first the codes of the first characters of two strings are compared, then the codes of the second ones, and so on until the first mismatch or the end of one of the strings is reached.

For example, the string "ABC" is less than "abc", because the codes of uppercase letters in the character table are lower than the codes of the corresponding lowercase letters (on the first character we already get that "A" < "a"). If strings have matching characters at the beginning, but one of them is longer than the other, then the longer string is considered to be greater ("ABCD" > "ABC").

Such string relationships form the lexicographic order. When the string "A" is less than the string "B" ("A" < "B"), "A" is said to precede "B".

To get familiar with the character codes, you can use the standard Windows application "Character Table". In it, the characters are arranged in order of increasing codes. In addition to the general Unicode table, which includes many national languages, there are code pages: ANSI standard tables with single-byte character codes — they differ for each language or group of languages. We will explore this issue in more detail in the section [Working with symbols and code pages](/en/book/common/strings/strings_codepages).

The initial part of the character tables with codes from 0 to 127 is the same for all languages. This part is shown in the following table.

![ASCII character code table](pics/ascii-small.png)

ASCII character code table

To obtain the character code, take the hexadecimal digit on the left (the line number in which the character is located) and add the number on top (the column number in which the character is located): the result is a hexadecimal number. For example, for '!' there is 2 on the left and 1 on the top, which means the character code is 0x21, or 33 in decimal.

Codes up to 32 are control codes. Among them, you can find, in particular, tabulation (code 0x9), line feed (code 0xA), and carriage return (code 0xD).

A pair of characters 0xD 0xA following one another is used in Windows text files to break to a new line. We got acquainted with the corresponding MQL5 literals in the [Character types](/en/book/basis/builtin_types/characters) section: 0xA can be denoted as '\n' and 0xD as '\r'. The tabulation 0x9 also has its own representation: '\t'.

The MQL5 API provides the StringCompare function, which allows you to disable case sensitivity when comparing strings.

int StringCompare(const string &string1, const string &string2, const bool case_sensitive = true)

The function compares two strings and returns one of three values: +1 if the first string is "greater than" the second; 0 if strings are "equal"; -1 if the first string is "less than" the second one. The concepts of "greater than", "less than" and "equal to" depend on the case_sensitive parameter.

When the case_sensitive parameter equals true (which is the default), the comparison is case-sensitive, with uppercase letters being considered greater than similar lowercase ones. This is the reverse of the standard lexicographic order according to character codes.

When case-sensitive, the StringCompare function uses an order of uppercase and lowercase letters that is different from the lexicographical order. For example, we know that the relation "A" < "a" is true, in which the operator '<' is guided by character codes. Therefore, capitalized words should appear in the hypothetical dictionary (array) before words with the same lowercase letter. However, when comparing "A" and "a" using the StringCompare("A", "a") function, we get +1 which means "A" is greater than "a". Thus, in the sorted dictionary, words starting with lowercase letters will come first, and only after them will come words with capital letters.

In other words, the function ranks the strings alphabetically. Besides that, in the case sensitivity mode, an additional rule applies: if there are strings that differ only in case, those that have uppercase letters follow their counterparts with lowercase letters (at the same positions in the word).

If the case_sensitive parameter equals false, the letters are case insensitive, so the strings "A" and "a" are considered equal, and the function returns 0.

You can check different comparison results by the StringCompare function and by the operator using the StringCompare.mq5 script.

```
void OnStart()
{
   PRT(StringCompare("A", "a"));        // 1, which means "A" > "a" (!)
   PRT(StringCompare("A", "a", false)); // 0, which means "A" == "a"
   PRT("A" > "a");                      // false,   "A" < "a"
   
   PRT(StringCompare("x", "y"));        // -1, which means "x" < "y"
   PRT("x" > "y");                      // false,    "x" < "y"
   ...
}

```

In the [Function Templates](/en/book/oop/templates/templates_functions) section, we have created a templated quicksort algorithm. Let's transform it into a template class and use it for several sorting options: using comparison operators, as well as using the StringCompare function both with and without case sensitivity enabled. Let's put the new QuickSortT class in the QuickSortT.mqh header file and connect it to the test script StringCompare.mq5.

The sorting API has remained almost unchanged.

```
template<typename T>
class QuickSortT
{
public:
   void Swap(T &array[], const int i, const int j)
   {
      ...
   }
   
   virtual int Compare(T &a, T &b)
   {
      return a > b ? +1 : (a < b ? -1 : 0);
   }
   
   void QuickSort(T &array[], const int start = 0, int end = INT_MAX)
   {
      ...
         for(int i = start; i <= end; i++)
         {
            //if(!(array[i] > array[end]))
            if(Compare(array[i], array[end]) <= 0)
            {
               Swap(array, i, pivot++);
            }
         }
      ...
   }
};

```

The main difference is that we have added a virtual method Compare, which by default contains a comparison using the '>' and '<' operators, and returns +1, -1, or 0 in the same way as StringCompare. The Compare method is now used in the QuickSort method instead of a simple comparison and must be overridden in child classes in order to use the StringCompare function or any other way of comparison.

In particular, in the StringCompare.mq5 file, we implement the following "comparator" class derived from QuickSortT<string>:

```
class SortingStringCompare : public QuickSortT<string>
{
   const bool caseEnabled;
public:
   SortingStringCompare(const bool sensitivity = true) :
      caseEnabled(sensitivity) { }
      
   virtual int Compare(string &a, string &b) override
   {
      return StringCompare(a, b, caseEnabled);
   }
};

```

The constructor receives 1 parameter, which specifies string comparison sign taking into account (true) or ignoring (false) the register. The string comparison itself is done in the redefined virtual method Compare which calls the function StringCompare with the given arguments and setting.

To test sorting, we need a set of strings that combines uppercase and lowercase letters. We can generate it ourselves: it is enough to develop a class that performs permutations (with repetition) of characters from a predefined set (alphabet) for a given set length (string). For example, you can limit yourself to the small alphabet "abcABC", that is, three fist English letters in both cases, and generate all possible strings of 2 characters from them.

The class PermutationGenerator is supplied in the file PermutationGenerator.mqh and left for independent study. Here we present only its public interface.

```
class PermutationGenerator
{
public:
   struct Result
   {
      int indices[]; // indexes of elements in each position of the set, i.e.
   };                // for example, the numbers of the letters of the "alphabet" in each position of the string 
   PermutationGenerator(const int length, const int elements);
   SimpleArray<Result> *run();
};

```

When creating a generator object, you must specify the length of the generated sets length (in our case, this will be the length of the strings, i.e., 2) and the number of different elements from which the sets will be composed (in our case, this is the number of unique letters, that is, 6). With such input data, 6 * 6 = 36 variants of lines should be obtained.

The process itself is carried out by run method. A template class is used to return an array with results SimpleArray, which we discussed in the [Method Templates](/en/book/oop/templates/templates_methods) section. In this case, it is parameterized by the structure type result.

The call of the generator and the actual creation of strings in accordance with the array of permutations received from it (in the form of letter indices at each position for all possible strings) is performed in the auxiliary function GenerateStringList.

```
void GenerateStringList(const string symbols, const int len, string &result[])
{
   const int n = StringLen(symbols); // alphabet length, unique characters
   PermutationGenerator g(len, n);
   SimpleArray<PermutationGenerator::Result> *r = g.run();
   ArrayResize(result, r.size());
   // loop through all received character permutations
   for(int i = 0; i < r.size(); ++i)
   {
      string element;
      // loop through all characters in the string
      for(int j = 0; j < len; ++j)
      {
         // add a letter from the alphabet (by its index) to the string
         element += ShortToString(symbols[r[i].indices[j]]);
      }
      result[i] = element;
   }
}

```

Here we use several functions that are still unfamiliar to us (ArrayResize, ShortToString), but we'll get to them soon. For now, we should only know that the ShortToString function returns a string consisting of that single character based on the ushort type character code. Using the operator '+=', we concatenate each resulting string from such single-character strings. Recall that the operator [] is defined for strings, so the expression symbols[k] will return the k-th character of the symbols string. Of course, k can in turn be an integer expression, and here r[i].indices[j]  is referring to i-th element of the r array from which the index of the "alphabet" character is read for the j-th position of the string.

Each received string is stored in an array-parameter result.

Let's apply this information in the OnStart function.

```
void OnStart()
{
   ...
   string messages[];
   GenerateStringList("abcABC", 2, messages);
   Print("Original data[", ArraySize(messages), "]:");
   ArrayPrint(messages);
   
   Print("Default case-sensitive sorting:");
   QuickSortT<string> sorting;
   sorting.QuickSort(messages);
   ArrayPrint(messages);
   
   Print("StringCompare case-insensitive sorting:");
   SortingStringCompare caseOff(false);
   caseOff.QuickSort(messages);
   ArrayPrint(messages);
   
   Print("StringCompare case-sensitive sorting:");
   SortingStringCompare caseOn(true);
   caseOn.QuickSort(messages);
   ArrayPrint(messages);
}

```

The script first gets all string options into the messages array and then sorts it in 3 modes: using the built-in comparison operators, using the StringCompare function in the case-insensitive mode and using the same function in the case-sensitive mode.

We will get the following log output:

```
Original data[36]:
[ 0] "aa" "ab" "ac" "aA" "aB" "aC" "ba" "bb" "bc" "bA" "bB" "bC" "ca" "cb" "cc" "cA" "cB" "cC"
[18] "Aa" "Ab" "Ac" "AA" "AB" "AC" "Ba" "Bb" "Bc" "BA" "BB" "BC" "Ca" "Cb" "Cc" "CA" "CB" "CC"
Default case-sensitive sorting:
[ 0] "AA" "AB" "AC" "Aa" "Ab" "Ac" "BA" "BB" "BC" "Ba" "Bb" "Bc" "CA" "CB" "CC" "Ca" "Cb" "Cc"
[18] "aA" "aB" "aC" "aa" "ab" "ac" "bA" "bB" "bC" "ba" "bb" "bc" "cA" "cB" "cC" "ca" "cb" "cc"
StringCompare case-insensitive sorting:
[ 0] "AA" "Aa" "aA" "aa" "AB" "aB" "Ab" "ab" "aC" "AC" "Ac" "ac" "BA" "Ba" "bA" "ba" "BB" "bB"
[18] "Bb" "bb" "bC" "BC" "Bc" "bc" "CA" "Ca" "cA" "ca" "CB" "cB" "Cb" "cb" "cC" "CC" "Cc" "cc"
StringCompare case-sensitive sorting:
[ 0] "aa" "aA" "Aa" "AA" "ab" "aB" "Ab" "AB" "ac" "aC" "Ac" "AC" "ba" "bA" "Ba" "BA" "bb" "bB"
[18] "Bb" "BB" "bc" "bC" "Bc" "BC" "ca" "cA" "Ca" "CA" "cb" "cB" "Cb" "CB" "cc" "cC" "Cc" "CC"

```

The output shows the differences in these three modes.
