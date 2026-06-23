# Creation of ex5 libraries; export of functions

To describe a library, add the #property library directive to the source code of the main (compiled) module (usually, at the beginning of the file).

```
#property library

```

Specifying this directive in any other files included in the compilation process via #include has no effect.

The library property informs the compiler that the given ex5 file is a library: a mark about this is stored in the header of the ex5 file.

A separate folder MQL5/Libraries is reserved for libraries in MetaTrader 5. You can organize a hierarchy of nested folders in it, just like for other types of programs in MQL5.

Libraries do not directly participate in event handling, and therefore the compiler does not require the presence of any standard handlers in the code. However, you can call the exported functions of the library from the event handlers of the MQL program to which the library is connected.

To export a function from a library, just mark it with a special keyword export. This modifier must be placed at the very end of the function header.

```
result_type function_id ( [ parameter_type parameter_id
                          [ = default_value] ...] ) export
{
   ...
}

```

Parameters must be simple types or strings, structures with fields of such types, or their arrays. Pointers and references are allowed for MQL5 object types (for restrictions on importing DLLs, see the [relevant section](/en/book/advanced/libraries/libraries_dll)).

Let's see some examples. The parameter is a prime number:

```
double Algebraic2(const double x) export
{
   return x / sqrt(1 + x * x); 
}

```

The parameters are a pointer to an object and a reference to a pointer (allowing you to assign a pointer inside the function).

```
class X
{
public:
   X() { Print(__FUNCSIG__); }
};
void setObject(const X *obj) export { ... }
void getObject(X *&obj) export { obj = new X(); }

```

The parameter is a structure:

```
struct Data
{
   int value;
   double data[];
   Data(): value(0) { }
   Data(const int i): value(i) { ArrayResize(data, i); }
};
   
void getRefStruct(const int i, Data &data) export { ... }

```

You can only export functions but not entire classes or structures. Some of these limitations can be avoided with the help of pointers and references, which we will discuss in more detail later.

Function templates cannot be declared with the export keyword and in the #import directive.

The export modifier instructs the compiler to include the function in the table of exported functions within the given ex5 executable. Thanks to this, such functions become available ("visible") from other MQL programs, where they can be used after importing with a special directive [#import](/en/book/advanced/libraries/libraries_import).

All functions that are going to be exported must be marked with the export modifier. Although the main program is not required to import all of them as it can only import the necessary ones.

If you forget to export a function but include it in the import directive in the main MQL program, then when the latter is launched, an error will occur:

```
cannot find 'function' in 'library.ex5'
unresolved import function call

```

A similar problem will arise if there are discrepancies in the description of the exported function and its imported prototype. This can happen, for example, if you forget to recompile a library or main program after making changes to the programming interface, which is usually described in a separate header file.

Debugging libraries is not possible, so if necessary, you should have a helper script or another MQL program that is built from the source codes of the library in debugger mode and can be executed with breakpoints or step-by-step. Of course, this will require emulating calls to exported functions using some real or artificial data.

For DLLs, the description of exported functions is done differently, depending on the programming language in which they are created. Look for details in the documentation of your chosen development environments.

Consider an example of a simple library MQL5/Libraries/MQL5Book/LibRand.mq5, from which several functions are exported with different types of parameters and results. The library is designed to generate random data:

- of numerical data with a pseudo-normal distribution
- of strings with random characters from the given sets (may be useful for passwords)

In particular, you can get one random number using the PseudoNormalValue function, in which the expected value and variance are set as parameters.

```
double PseudoNormalValue(const double mean = 0.0, const double sigma = 1.0,
   const bool rooted = false) export
{
   // use ready-made sqrt for mass generation in a cycle in PseudoNormalArray
   const double s = !rooted ? sqrt(sigma) : sigma; 
   const double r = (rand() - 16383.5) / 16384.0; // [-1,+1] excluding borders
   const double x = -(log(1 / ((r + 1) / 2) - 1) * s) / M_PI * M_E + mean;
   return x;
}

```

The PseudoNormalArray function fills the array with random values in a given amount (n) and with the required distribution.

```
bool PseudoNormalArray(double &array[], const int n,
   const double mean = 0.0, const double sigma = 1.0) export
{
   bool success = true;
   const double s = sqrt(fabs(sigma)); // passing ready sqrt when calling PseudoNormalValue
   ArrayResize(array, n);
   for(int i = 0; i < n; ++i)
   {
      array[i] = PseudoNormalValue(mean, s, true);
      success = success && MathIsValidNumber(array[i]);
   }
   return success;
}

```

To generate one random string, we write the RandomString function, which "selects" from the supplied set of characters (pattern) a given quantity (length) of arbitrary characters. When the pattern parameter is blank (default), a full set of letters and numbers is assumed. Helper functions StringPatternAlpha and StringPatternDigit are used to get it; these functions are also exportable (not listed in the book, see the source code).

```
string RandomString(const int length, string pattern = NULL) export
{
   if(StringLen(pattern) == 0)
   {
      pattern = StringPatternAlpha() + StringPatternDigit();
   }
   const int size = StringLen(pattern);
   string result = "";
   for(int i = 0; i < length; ++i)
   {
      result += ShortToString(pattern[rand() % size]);
   }
   return result;
}

```

In general, to work with a library, it is necessary to publish a header file describing everything that should be available in it from outside (and the details of the internal implementation can and should be hidden). In our case, such a file is called MQL5Book/LibRand.mqh. In particular, it describes user-defined types (in our case, the STRING_PATTERN enumeration) and function prototypes.

Although the exact syntax of the #import block is not known to us yet, this should not affect the clarity of the declarations inside it: the headers of the exported functions are repeated here but without the keyword export.

```
enum STRING_PATTERN
{
   STRING_PATTERN_LOWERCASE = 1, // lowercase letters only
   STRING_PATTERN_UPPERCASE = 2, // capital letters only
   STRING_PATTERN_MIXEDCASE = 3  // both registers
};
   
#import "MQL5Book/LibRand.ex5"
string StringPatternAlpha(const STRING_PATTERN _case = STRING_PATTERN_MIXEDCASE);
string StringPatternDigit();
string RandomString(const int length, string pattern = NULL);
void RandomStrings(string &array[], const int n, const int minlength,
   const int maxlength, string pattern = NULL);
void PseudoNormalDefaultMean(const double mean = 0.0);
void PseudoNormalDefaultSigma(const double sigma = 1.0);
double PseudoNormalDefaultValue();
double PseudoNormalValue(const double mean = 0.0, const double sigma = 1.0,
   const bool rooted = false);
bool PseudoNormalArray(double &array[], const int n,
   const double mean = 0.0, const double sigma = 1.0);
#import

```

We will write a test script that uses this library in the next section, after studying the directive #import.
