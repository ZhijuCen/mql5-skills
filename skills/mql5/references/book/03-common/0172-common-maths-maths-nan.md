# Normality test for real numbers

Since calculations with real numbers can have abnormal situations, such as going beyond the scope of a function, obtaining mathematical infinity, lost order, and others, the result may not contain a number. Instead, it may contain a special value that actually describes the nature of the problem. All such special values have a generic name "not a number" (Not A Number, NaN).

We have already faced them in the previous sections of the book. In particular, when outputting to a journal (see section [Numbers to strings and vice versa](/en/book/common/conversions/conversions_numbers)) they are displayed as text labels (for example, nan(ind), +inf and others). Another feature is that a single NaN value among the operands of any expression is enough for the entire expression to stop evaluating correctly and begin to give the result NaN. The only exceptions are "non-numbers" representing the plus/minus of infinity: if you divide something by them, you get zero. However, there is an expected exception here: if we divide infinity by infinity, we again get NaN.

Therefore, it is important for programs to determine the moment when NaN appears in the calculations and handle the situation in a special way: signal an error, substitute some acceptable default value, or repeat the calculation with other parameters (for example, reduce the accuracy/step of the iterative algorithm).

There are 2 functions in MQL5 that allow you to analyze a real number for normality:MathIsValidNumber gives a simple answer: yes (true) or not (false), and MathClassify produces more detailed categorization.

At the physical level, all special values are encoded in a number with a special combination of bits that is not used to represent ordinary numbers. For types double and float these encodings are, of course, different. Let's take a look at double behind the scenes (as it is more in demand than float).

In the chapter [Nested templates](/en/book/oop/templates/templates_nested), we created a Converter class for switching views by combining two different types in a union. Let's use this class to study the NaN bit device.

For convenience, we will move the class to a separate header file ConverterT.mqh. Let's connect this mqh-file in the test script MathInvalid.mq5 and create an instance of a converter for a bunch of types double/ulong (the order is not important as the converter is able to work in both directions).

```
static Converter<ulong, double> NaNs;

```

The combination of bits in NaN is standardized, so let's take a few commonly used values represented by constants ulong, and see how the built-in functions react to them.

```
// basic NaNs
#define NAN_INF_PLUS  0x7FF0000000000000
#define NAN_INF_MINUS 0xFFF0000000000000
#define NAN_QUIET     0x7FF8000000000000
#define NAN_IND_MINUS 0xFFF8000000000000
   
// custom NaN examples
#define NAN_QUIET_1   0x7FF8000000000001
#define NAN_QUIET_2   0x7FF8000000000002
   
static double pinf = NaNs[NAN_INF_PLUS];  // +infinity
static double ninf = NaNs[NAN_INF_MINUS]; // -infinity
static double qnan = NaNs[NAN_QUIET];     // quiet NaN
static double nind = NaNs[NAN_IND_MINUS]; // -nan(ind)
   
void OnStart()
{
   PRT(MathIsValidNumber(pinf));               // false
   PRT(EnumToString(MathClassify(pinf)));      // FP_INFINITE
   PRT(MathIsValidNumber(nind));               // false
   PRT(EnumToString(MathClassify(nind)));      // FP_NAN
   ...
}

```

As expected, the results were the same.

Let's view the formal description of the MathIsValidNumber and MathClassify functions and then continue with the tests.

bool MathIsValidNumber(double value)

The function checks the correctness of a real number. The parameter can be of type double or float. The resulting true means the correct number, and false means "not a number" (one of the varieties of NaN).

ENUM_FP_CLASS MathClassify(double value)

The function returns the category of a real number (of type double or float) which is one of the enum ENUM_FP_CLASS values:

- FP_NORMAL is a normal number.
- FP_SUBNORMAL is a number less than the minimum number representable in a normalized form (for example, for the type double these are values less than DBL_MIN, 2.2250738585072014e-308); loss of order (accuracy).
- FP_ZERO is zero (positive or negative).
- FP_INFINITE is infinity (positive or negative).
- FP_NAN means all other types of "non-numbers" (subdivided into families of "silent" and "signal" NaN).

MQL5 does not provide alerting NaNs which are used in the exceptions mechanism and allows the interception and response to critical errors within the program. There is no such mechanism in MQL5, so, for example, in case of a zero division, the MQL program simply terminates its work (unloads from the chart).

There can be many "quiet" NaNs, and you can construct them using a converter to differentiate and handle non-standard states in your computational algorithms.

Let's perform some calculations in MathInvalid.mq5 to visualize how the numbers of different categories can be obtained.

```
 // calculations with double
   PRT(MathIsValidNumber(0));                      // true
   PRT(EnumToString(MathClassify(0)));             // FP_ZERO
   PRT(MathIsValidNumber(M_PI));                   // true
   PRT(EnumToString(MathClassify(M_PI)));          // FP_NORMAL
   PRT(DBL_MIN / 10);                              // 2.225073858507203e-309
   PRT(MathIsValidNumber(DBL_MIN / 10));           // true
   PRT(EnumToString(MathClassify(DBL_MIN / 10)));  // FP_SUBNORMAL
   PRT(MathSqrt(-1.0));                            // -nan(ind)
   PRT(MathIsValidNumber(MathSqrt(-1.0)));         // false
   PRT(EnumToString(MathClassify(MathSqrt(-1.0))));// FP_NAN
   PRT(MathLog(0));                                // -inf
   PRT(MathIsValidNumber(MathLog(0)));             // false
   PRT(EnumToString(MathClassify(MathLog(0))));    // FP_INFINITE
   
 // calculations with float
   PRT(1.0f / FLT_MIN / FLT_MIN);                             // inf
   PRT(MathIsValidNumber(1.0f / FLT_MIN / FLT_MIN));          // false
   PRT(EnumToString(MathClassify(1.0f / FLT_MIN / FLT_MIN))); // FP_INFINITE

```

We can use the converter in the opposite direction: to get its bit representation by value double, and thereby detect "non-numbers":

```
   PrintFormat("%I64X", NaNs[MathSqrt(-1.0)]);      // FFF8000000000000
   PRT(NaNs[MathSqrt(-1.0)] == NAN_IND_MINUS);      // true, nind

```

The PrintFormat function is similar to [StringFormat](/en/book/common/strings/strings_format); the only difference is that the result is immediately printed to the log, and not to a string.

Finally, let's make sure that "not numbers" are always not equal:

```
   // NaN != NaN always true
   PRT(MathSqrt(-1.0) != MathSqrt(-1.0)); // true
   PRT(MathSqrt(-1.0) == MathSqrt(-1.0)); // false

```

To get NaN or infinity in MQL5, there is a method based on casting the strings "nan" and "inf" to double.

```
double nan = (double)"nan";
double infinity = (double)"inf";

```
