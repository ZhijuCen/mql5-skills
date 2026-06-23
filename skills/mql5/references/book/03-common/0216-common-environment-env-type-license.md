# Program type and license

The same source code can somehow be included in MQL programs of different types. In addition to the option of [including source codes](/en/book/basis/preprocessor/preprocessor_include) (preprocessor directive #include) into a common product at the compilation stage, it is also possible to assemble the [libraries](/en/book/advanced/libraries) — binary program modules connected to the main program at the execution stage.

However, some functions are only allowed to be used in certain types of programs. For example, the [OrderCalcMargin](/en/book/automation/experts/experts_ordercalcmargin) function cannot be used in [indicators](/en/book/applications/indicators_make). Although this limitation does not seem to be fundamentally justified, the developer of a universal algorithm for calculating collateral funds, which can be built into not only Expert Advisors but also indicators, should take this nuance into account and provide an alternative calculation method for indicators.

A complete list of restrictions on program types will be given in a suitable section of each chapter. In all such cases, it is important to know the type of the "parent" program.

To determine the program type, there is the MQL_PROGRAM_TYPE property in ENUM_MQL_INFO_INTEGER. Possible property values are described in the ENUM_PROGRAM_TYPE enumeration.

| Identifier | Value | Description |
| --- | --- | --- |
| PROGRAM_SCRIPT | 1 | Script |
| PROGRAM_EXPERT | 2 | Expert Advisor |
| PROGRAM_INDICATOR | 4 | Indicator |
| PROGRAM_SERVICE | 5 | Service |

In the log snippet in the previous section, we saw that the PROGRAM_SCRIPT property is set to 1 because our test is a script. To get a string description, you can use the function EnumToString.

```
ENUM_PROGRAM_TYPE type = (ENUM_PROGRAM_TYPE)MQLInfoInteger(MQL_PROGRAM_TYPE);
Print(EnumToString(type));

```

Another property of an MQL program that is convenient to analyze for enabling/disabling certain features is the type of license. As you know, MQL programs can be distributed freely or within the MQL5 Market. Moreover, the program in the store can be purchased or downloaded as a demo version. These factors are easy to check and, if desired, adapt the algorithms for them. For these purposes, there is the MQL_LICENSE_TYPE property in ENUM_MQL_INFO_INTEGER, which uses the ENUM_LICENSE_TYPE enumeration as a type.

| Identifier | Value | Description |
| --- | --- | --- |
| LICENSE_FREE | 0 | Free unlimited version |
| LICENSE_DEMO | 1 | Demo version of a paid product from the Market that works only in the strategy tester |
| LICENSE_FULL | 2 | Purchased licensed version, allows at least 5 activations (can be increased by the seller) |
| LICENSE_TIME | 3 | Time-limited version (not implemented yet) |

It is important to note here that the license refers to the binary ex5 module from which the request is made using MQLInfoInteger(MQL_LICENSE_TYPE). Within a library, this function will return the library's own license, not the main program that the library is linked to.

As an example to test both functions of this section, a simple service EnvType.mq5 is included with the book. It does not contain a work cycle and therefore will terminate immediately after executing the two instructions in OnStart.

```
#property service
   
void OnStart()
{
   Print(EnumToString((ENUM_PROGRAM_TYPE)MQLInfoInteger(MQL_PROGRAM_TYPE)));
   Print(EnumToString((ENUM_LICENSE_TYPE)MQLInfoInteger(MQL_LICENSE_TYPE)));
}

```

To simplify its launch, i.e., to eliminate the need to create an instance of the service and run it through the context menu of the Navigator in the terminal, it is proposed to use the debugger: just open the source code in MetaEditor and execute the command Debugging -> Start on real data (F5, or button in the toolbar).

We should get the following log entries:

```
EnvType (debug)        PROGRAM_SERVICE
EnvType (debug)        LICENSE_FREE

```

Here you can clearly see that the type of program is a service, and there is actually no license (free use).
