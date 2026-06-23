# Getting a general list of terminal and program properties

The available built-in functions for obtaining environment properties use a generic approach: the properties of each specific type are combined into a separate function with a single argument that specifies the requested property. There are enumerations defined to identify properties: each element describes one property.

As we will see below, this approach is often used in the MQL5 API and in other areas, including application areas. In particular, similar sets of functions are used to get the properties of [trading accounts](/en/book/automation/account) and [financial instruments](/en/book/automation/symbols).

Properties of three simple types, int, double, and string, are sufficient to describe the environment. However, not only integer properties are presented using values of type int, but also logical flags (in particular, permissions/prohibitions, presence of a network connection, etc.), as well as other built-in enumerations (for example, types of MQL programs and types of licenses).

Given the conditional division into terminal properties and properties of a particular MQL program, there are the following functions that describe the environment.

int MQLInfoInteger(ENUM_MQL_INFO_INTEGER p)

int TerminalInfoInteger(ENUM_TERMINAL_INFO_INTEGER p)

double TerminalInfoDouble(ENUM_TERMINAL_INFO_DOUBLE p)

string MQLInfoString(ENUM_MQL_INFO_STRING p)

string TerminalInfoString(ENUM_TERMINAL_INFO_STRING p)

These prototypes map value types to enum types. For example, terminal properties of type int are summarized in ENUM_TERMINAL_INFO_INTEGER, and its properties of type double are listed in ENUM_TERMINAL_INFO_DOUBLE, etc. The list of available enums and their elements can be found in the documentation, in the sections on [Terminal properties](https://www.mql5.com/en/docs/constants/environment_state/terminalstatus) and [MQL programs](https://www.mql5.com/en/docs/constants/environment_state/mql5_programm_info).

In the following sections, we'll take a look at all the properties, grouped based on their purpose. But here we turn to the problem of obtaining a general list of all existing properties and their values. This is often necessary to identify "bottlenecks" or features of the operation of MQL programs on specific instances of the terminal. A rather common situation is when an MQL program works on one computer, but does not work at all, or works exhibits some problems on another.

The list of properties is constantly updated as the platform develops, so it is advisable to make their request not on the basis of a list hardwired into the source code, but automatically.

In the [Enumerations](/en/book/common/conversions/conversions_enums) section, we have created a template function EnumToArray to get a complete list of enumeration elements (file EnumToArray.mqh). Also in that section, we introduced the script ConversionEnum.mq5, which uses the specified header file. In the script, a helper function process was implemented, which received an array with enumeration element codes and output them to the log. We will take these developments as a starting point for further improvement.

We need to modify the process function in such a way, that we not only get a list of the elements of a particular enumeration but also query the corresponding properties using one of the built-in property functions.

Let's give the new version of the script a name, Environment.mq5.

Since the properties of the environment are scattered across several different functions (in this case, five), you need to learn how to pass to the new version of the function process a pointer to the required built-in function (see section [Function pointers (typedef)](/en/book/basis/functions/functions_typedef)). However, MQL5 does not allow assigning the address of a built-in function to a function pointer. This can only be done with an application function implemented in MQL5. Therefore, we will create wrapper functions. For example:

```
int _MQLInfoInteger(const ENUM_MQL_INFO_INTEGER p)
{
   return MQLInfoInteger(p);
}
// example of pointer type description  
typedef int (*IntFuncPtr)(const ENUM_MQL_INFO_INTEGER property);
// initialization of pointer variables
IntFuncPtr ptr1 = _MQLInfoInteger;  // ok
IntFuncPtr ptr2 = MQLInfoInteger;   // compilation error

```

A "double" for MQLInfoInteger is shown above (obviously, it should have a different, but preferably similar, name). Other functions are "packed" in a similar way. There will be five in total.

If in the old version of process there was only one template parameter specifying an enumeration, in the new one we also need to pass the type of the return value (since MQL5 does not "understand" the words in the name of enumerations): even though the ending "INTEGER" is present in the name ENUM_MQL_INFO_INTEGER, the compiler is not able to associate it with the type int).

However, in addition to linking the types of the return value and the enumeration, we need to somehow pass to the function process a pointer to the appropriate wrapper function (one of the five we defined earlier). After all, the compiler itself cannot determine by an argument, for example, of ENUM_MQL_INFO_INTEGER type, that MQLInfoInteger needs to be called.

To solve this problem, a special template structure was created that combines all three factors together.

```
template<typename E, typename R>
struct Binding
{
public:
   typedef R (*FuncPtr)(const E property);
   const FuncPtr f;
   Binding(FuncPtr p): f(p) { }
};

```

The two template parameters allow you to specify the type of the function pointer (FuncPtr) with the desired combination of result and input parameters. The structure instance has the f field for a pointer to that newly defined type.

Now a new version of the process function can be described as follows.

```
template<typename E, typename R>
void process(Binding<E, R> &b)
{
   E e = (E)0; // turn off the warning about the lack of initialization
   int array[];
   // get a list of enum elements into an array
   int n = EnumToArray(e, array, 0, USHORT_MAX);
   Print(typename(E), " Count=", n);
   ResetLastError();
   // display the name and value for each element,
   // obtained by calling a pointer in the Binding structure
   for(int i = 0; i < n; ++i)
   {
      e = (E)array[i];
      R r = b.f(e); // call the function, then parse _LastError
      const int snapshot = _LastError;
      PrintFormat("% 3d %s=%s", i, EnumToString(e), (string)r +
         (snapshot != 0 ? E2S(snapshot) + " (" + (string)snapshot + ")" : ""));
      ResetLastError();
   }
}

```

The input argument is the Binding structure. It contains a pointer to a specific function for obtaining properties (this field will be filled in by the calling code).

This version of the algorithm logs the sequence number, the property identifier, and its value. Again, note that the first number in each entry will contain the element's ordinal in the enumeration, not the value (values can be assigned to elements with gaps). Optionally you can add an output of a variable e "in its pure form" inside the instructions print format.

In addition, you can modify the process so that it collects into an array (or other container, such as a map) the resulting property values and returns them "outside".

It would be a potential error to refer to the function pointer directly in the instruction print format along with the _LastError error code analysis. The point is that the sequence of evaluation of function arguments (see section [Parameters and Arguments](/en/book/basis/functions/functions_parameters)) and operands in an expression (see section [Basic concepts](/en/book/basis/expressions/expressions_overview)) is not defined in this case. Therefore, when a pointer is called on the same line where _LastError is read, the compiler may decide to execute the second before the first. As a result, we will see an irrelevant error code (for example, from a previous function call).

But that's not all. Built-in variable _LastError can change its value almost anywhere in the evaluation of an expression if any operation fails. In particular, the function EnumToString can potentially raise an error code if a value is passed as an argument that is not in the enumeration. In this snippet, we are immune to this problem because our function EnumToArray returns an array with only checked (valid) enumeration elements. However, in general cases, in any "compound" instruction, there may be many places where _LastError will be changed. In this regard, it is desirable to fix the error code immediately after the action which we are interested in (here it is a function call by a pointer), saving it to an intermediate variable snapshot.

But let's go back to the main issue. We can finally organize a call of the new function process to obtain various properties of the software environment.

```
void OnStart()
{
   process(Binding<ENUM_MQL_INFO_INTEGER, int>(_MQLInfoInteger));
   process(Binding<ENUM_TERMINAL_INFO_INTEGER, int>(_TerminalInfoInteger));
   process(Binding<ENUM_TERMINAL_INFO_DOUBLE, double>(_TerminalInfoDouble));
   process(Binding<ENUM_MQL_INFO_STRING, string>(_MQLInfoString));
   process(Binding<ENUM_TERMINAL_INFO_STRING, string>(_TerminalInfoString));
}

```

Below is a snippet of the generated log entries.

```
ENUM_MQL_INFO_INTEGER Count=15
  0 MQL_PROGRAM_TYPE=1
  1 MQL_DLLS_ALLOWED=0
  2 MQL_TRADE_ALLOWED=0
  3 MQL_DEBUG=1
...
  7 MQL_LICENSE_TYPE=0
...
ENUM_TERMINAL_INFO_INTEGER Count=50
  0 TERMINAL_BUILD=2988
  1 TERMINAL_CONNECTED=1
  2 TERMINAL_DLLS_ALLOWED=0
  3 TERMINAL_TRADE_ALLOWED=0
...
  6 TERMINAL_MAXBARS=100000
  7 TERMINAL_CODEPAGE=1251
  8 TERMINAL_MEMORY_PHYSICAL=4095
  9 TERMINAL_MEMORY_TOTAL=8190
 10 TERMINAL_MEMORY_AVAILABLE=7813
 11 TERMINAL_MEMORY_USED=377
 12 TERMINAL_X64=1
...
ENUM_TERMINAL_INFO_DOUBLE Count=2
  0 TERMINAL_COMMUNITY_BALANCE=0.0 (MQL5_WRONG_PROPERTY,4512)
  1 TERMINAL_RETRANSMISSION=0.0
ENUM_MQL_INFO_STRING Count=2
  0 MQL_PROGRAM_NAME=Environment
  1 MQL_PROGRAM_PATH=C:\Program Files\MT5East\MQL5\Scripts\MQL5Book\p4\Environment.ex5
ENUM_TERMINAL_INFO_STRING Count=6
  0 TERMINAL_COMPANY=MetaQuotes Software Corp.
  1 TERMINAL_NAME=MetaTrader 5
  2 TERMINAL_PATH=C:\Program Files\MT5East
  3 TERMINAL_DATA_PATH=C:\Program Files\MT5East
  4 TERMINAL_COMMONDATA_PATH=C:\Users\User\AppData\Roaming\MetaQuotes\Terminal\Common
  5 TERMINAL_LANGUAGE=Russian
 

```

These and other properties will be described in the following sections.

It is worth noting that some properties are inherited from previous stages of platform development and are left only for compatibility. In particular, the TERMINAL_X64 property in TerminalInfoInteger returns an indication of whether the terminal is 64-bit. Today, the development of 32-bit versions has been discontinued, and therefore this property is always equal to 1 (true).
