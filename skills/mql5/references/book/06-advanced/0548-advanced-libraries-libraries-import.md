# Including libraries; #import of functions

Functions are imported from compiled MQL5 modules (*.ex5 files) and from Windows dynamic library modules (*.dll files). The module name is specified in the #import directive, followed by descriptions of the imported function prototypes. Such a block must end with another #import directive, moreover, it can be without a name and simply close the block itself, or the name of another library can be specified in the directive, and thus the next import block begins at the same time. A series of import blocks should always end with a directive without a library name.

In its simplest form, the directive looks like this:

```
#import "[path] module_name [.extension]"
  function_type function_name([parameter_list]);
  [function_type function_name([parameter_list]);]
   ... 
#import

```

The name of the library file can be specified without the extension: then the DLL is assumed by default. Extension ex5 is required.

The name may be preceded by the library location path. By default, if there is no path, the libraries are searched in the folder MQL5/Libraries or in the folder next to the MQL program where the library is connected. Otherwise, different rules are applied to search for libraries depending on whether the type is DLL or EX5. These rules are covered in a [separate section](/en/book/advanced/libraries/libraries_path_lookup).

Here is an example of sequential import blocks from two libraries:

```
#import "user32.dll"
   int     MessageBoxW(int hWnd, string szText, string szCaption, int nType); 
   int     SendMessageW(int hWnd, int Msg, int wParam, int lParam); 
#import "lib.ex5" 
   double  round(double value); 
#import

```

With such directives, imported functions can be called from the source code in the same way as functions defined directly in the MQL program itself. All technical issues with loading libraries and redirecting calls to third-party modules are handled by the MQL program execution environment.

In order for the compiler to correctly issue the call to the imported function and organize the passing of parameters, a complete description is required: with the result type, with all parameters, modifiers, and default values, if they are present in the source.

Since the imported functions are outside of the compiled module, the compiler cannot check the correctness of the passed parameters and return values. Any discrepancy between the format of the expected and received data will result in an error during the execution of the program, and this may manifest itself as a critical program stop, or unexpected behavior.

If the library could not be loaded or the called imported function was not found, the MQL program terminates with a corresponding message in the log. The program will not be able to run until the problem is resolved, for example, by modifying and recompiling, placing the required library in one of the places along the search path, or allowing the use of the DLL (for DLLs only).

When sharing multiple libraries (doesn't matter if it's DLL or EX5), remember that they must have different names, regardless of their location directories. All imported functions get a scope that matches the name of the library file, that is, it is a kind of [namespace](/en/book/oop/classes_and_interfaces/classes_namespace_context), implicitly allocated for each included library.

Imported functions can have any names, including those that match the names of built-in functions (although this is not recommended). Moreover, it is possible to simultaneously import functions with the same names from different modules. In such cases, the operation [context permissions](/en/book/oop/classes_and_interfaces/classes_namespace_context) should be applied to determine which function should be called.

For example:

```
#import "kernel32.dll"
   int GetLastError();
#import "lib.ex5" 
   int GetLastError();
#import
  
class Foo
{
public: 
   int GetLastError() { return(12345); }
   void func() 
   { 
      Print(GetLastError());           // call a class method 
      Print(::GetLastError());         // calling the built-in (global) MQL5 function 
      Print(kernel32::GetLastError()); // function call from kernel32.d 
      Print(lib::GetLastError());      // function call from lib.ex5 
   }
};
   
void OnStart()
{
   Foo foo; 
   foo.func(); 
}

```

Let's see a simple example of the script LibRandTest.mq5, which uses functions from the EX5 library created in the previous section.

```
#include <MQL5Book/LibRand.mqh>

```

In the input parameters, you can select the number of elements in the array of numbers, the distribution parameters, as well as the step of the histogram, which we will calculate to make sure that the distribution approximately corresponds to the normal law.

```
input int N = 10000;
input double Mean = 0.0;
input double Sigma = 1.0;
input double HistogramStep = 0.5;
input int RandomSeed = 0;

```

Initialization of the random number generator built into MQL5 (uniform distribution) is performed by the value of the RandomSeed or, if 0 is left here, [GetTickCount](/en/book/common/timing/timing_count) is picked (new at each start).

To build a histogram, we use MapArray and QuickSortStructT (we have already worked with them in the sections on [multicurrency indicators](/en/book/applications/indicators_make/indicators_multisymbol) and about [array sorting](/en/book/common/arrays/arrays_compare_sort_search), respectively). The map will accumulate counters of hitting random numbers in the cells of the histogram with a HistogramStep step.

```
#include <MQL5Book/MapArray.mqh>
#include <MQL5Book/QuickSortStructT.mqh>

```

To display a histogram based on the map, you need to be able to sort the map in key-value order. To do this, we had to define a derived class.

```
#define COMMA ,
   
template<typename K,typename V>
class MyMapArray: public MapArray<K,V>
{
public:
   void sort()
   {
      SORT_STRUCT(Pair<K COMMA V>, array, key);
   }
};

```

Note that the COMMA macro becomes an alternate representation of the comma character ',' and is used when another SORT_STRUCT macro is called. If not for this substitution, the comma inside the Pair<K,V> would be interpreted by the preprocessor as a normal macro parameter separator, as a result of which 4 parameters would be received at the input of SORT_STRUCT instead of the expected 3 — this would cause a compilation error. The preprocessor knows nothing about the MQL5 syntax.

At the beginning of OnStart, after initialization of the generator, we check the receipt of a single random string and an array of strings of different lengths.

```
void OnStart()
{
   const uint seed = RandomSeed ? RandomSeed : GetTickCount();
   Print("Random seed: ", seed);
   MathSrand(seed);
   
   // call two library functions: StringPatternDigit and RandomString
   Print("Random HEX-string: ", RandomString(30, StringPatternDigit() + "ABCDEF"));
   Print("Random strings:");
   string text[];
   RandomStrings(text, 5, 10, 20);         // 5 lines from 10 to 20 characters long
   ArrayPrint(text);
   ...

```

Next, we test normally distributed random numbers.

```
   // call another library function: PseudoNormalArray
   double x[];
   PseudoNormalArray(x, N, Mean, Sigma);   // filled array x
   
   Print("Random pseudo-gaussian histogram: ");
   
   // take 'long' as key type, because 'int' has already been used for index access
   MyMapArray<long,int> map;
   
   for(int i = 0; i < N; ++i)
   {
 // value x[i] determines the cell of the histogram, where we increase the statistics
      map.inc((long)MathRound(x[i] / HistogramStep));
   }
   map.sort();                             // sort by key (i.e. by value)
   
   int max = 0;                            // searching for maximum for normalization
   for(int i = 0; i < map.getSize(); ++i)
   {
      max = fmax(max, map.getValue(i));
   }
   
   const double scale = fmax(max / 80, 1); // the histogram has a maximum of 80 symbols
   
   for(int i = 0; i < map.getSize(); ++i)  // print the histogram
   {
      const int p = (int)MathRound(map.getValue(i) / scale);
      string filler;
      StringInit(filler, p, '*');
      Print(StringFormat("%+.2f (%4d)",
         map.getKey(i) * HistogramStep, map.getValue(i)), " ", filler);
   }

```

Here is the result when run with default settings (timer randomization - each run will choose a new seed).

```
Random seed: 8859858
Random HEX-string: E58B125BCCDA67ABAB2F1C6D6EC677
Random strings:
"K4ZOpdIy5yxq4ble2" "NxTrVRl6q5j3Hr2FY" "6qxRdDzjp3WNA8xV"  "UlOPYinnGd36"      "6OCmde6rvErGB3wG" 
Random pseudo-gaussian histogram: 
-9.50 (   2) 
-8.50 (   1) 
-8.00 (   1) 
-7.00 (   1) 
-6.50 (   5) 
-6.00 (  10) *
-5.50 (  10) *
-5.00 (  24) *
-4.50 (  28) **
-4.00 (  50) ***
-3.50 ( 100) ******
-3.00 ( 195) ***********
-2.50 ( 272) ***************
-2.00 ( 510) ****************************
-1.50 ( 751) ******************************************
-1.00 (1029) *********************************************************
-0.50 (1288) ************************************************************************
+0.00 (1457) *********************************************************************************
+0.50 (1263) **********************************************************************
+1.00 (1060) ***********************************************************
+1.50 ( 772) *******************************************
+2.00 ( 480) ***************************
+2.50 ( 280) ****************
+3.00 ( 172) **********
+3.50 ( 112) ******
+4.00 (  52) ***
+4.50 (  43) **
+5.00 (  10) *
+5.50 (   8) 
+6.00 (   8) 
+6.50 (   2) 
+7.00 (   3) 
+7.50 (   1)

```

In this library, we have only exported and imported functions with built-in types. However, object interfaces with structures, classes, and templates are much more interesting and more in demand from a practical point of view. We will talk about the nuances of their use in libraries in a [separate section](/en/book/advanced/libraries/libraries_class_template).

When testing Expert Advisors and indicators in the tester, one should keep in mind an important point related to libraries. Libraries required for the main tested MQL program are determined automatically from the #import directives. However, if a custom indicator is called from the main program, to which some library is connected, then it is necessary to explicitly indicate in the program properties that it indirectly depends on a particular library. This is done with the directive:   

   

#property tester_library "path_library_name.extension"
