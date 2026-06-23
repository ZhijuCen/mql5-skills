# Enumerations

In MQL5 API, an enumeration value can be converted to a string using the EnumToString function. There is no ready-made inverse transformation.

string EnumToString(enum value)

The function converts the value (i.e., the ID of the passed element) of an enumeration of any type to a string.

Let's use it to solve one of the most popular tasks: to find out the size of the enumeration (how many elements it contains) and exactly what values correspond to all elements. For this purpose, in the header file EnumToArray.mqh we implement the special [template function](/en/book/oop/templates/templates_functions) (due to the template type E, it will work for any enum):

```
template<typename E>
int EnumToArray(E dummy, int &values[],
   const int start = INT_MIN, 
   const int stop = INT_MAX)
{
   const static string t = "::";
   
   ArrayResize(values, 0);
   int count = 0;
   
   for(int i = start; i < stop && !IsStopped(); i++)
   {
      E e = (E)i;
      if(StringFind(EnumToString(e), t) == -1)
      {
         ArrayResize(values, count + 1);
         values[count++] = i;
      }
   }
   return count;
}

```

The concept of its operation is based on the following. Since enumerations in MQL5 are stored as integers of type int, an implicit casting of any enumeration to (int) is supported, and an explicit casting int back to any enum type is also allowed. In this case, if the value corresponds to one of the elements of the enumeration, the EnumToString function returns a string with the ID of this element. Otherwise, the function returns a string of the form ENUM_TYPE::value.

Thus, by looping over integers in the acceptable range and explicitly casting them to an enum type, one can then analyze the output string EnumToString for the presence of '::' to determine whether the given integer is an enum member or not.

The StringFind function used here will be presented in the [next chapter](/en/book/common/strings), just like other string functions.

Let's create the ConversionEnum.mq5 script to test the concept. In it, we implement an auxiliary function process, which will call the EnumToArray template, report the number of elements in the enum, and print the resulting array with matches between the enum elements and their values.

```
template<typename E>
void process(E a)
{
  int result[];
  int n = EnumToArray(a, result, 0, USHORT_MAX);
  Print(typename(E), " Count=", n);
  for(int i = 0; i < n; i++)
  {
    Print(i, " ", EnumToString((E)result[i]), "=", result[i]);
  }
}

```

As an enumeration for research purposes, we will use the built-in enumeration with the ENUM_APPLIED_PRICE price types. Inside the function OnStart, let's first make sure that EnumToString produces strings as described above. So, for the element PRICE_CLOSE, the function will return the string "PRICE_CLOSE", and for the value (ENUM_APPLIED_PRICE)10, which is obviously out of range, it will return "ENUM_APPLIED_PRICE::10".

```
void OnStart()
{
   PRT(EnumToString(PRICE_CLOSE));            // PRICE_CLOSE
   PRT(EnumToString((ENUM_APPLIED_PRICE)10)); // ENUM_APPLIED_PRICE::10
   
   process((ENUM_APPLIED_PRICE)0);
}

```

Next, we call the function process for any value cast to ENUM_APPLIED_PRICE (or a variable of that type) and get the following result:

```
ENUM_APPLIED_PRICE Count=7
0 PRICE_CLOSE=1
1 PRICE_OPEN=2
2 PRICE_HIGH=3
3 PRICE_LOW=4
4 PRICE_MEDIAN=5
5 PRICE_TYPICAL=6
6 PRICE_WEIGHTED=7

```

Here we see that 7 elements are defined in the enumeration, and the numbering does not start from 0, as usual, but from 1 (PRICE_CLOSE). Knowing the values associated with the elements allows in some cases to optimize the writing of algorithms.
