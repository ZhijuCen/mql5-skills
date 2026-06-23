# Logic (Boolean) Type

Logic type is intended for storing features that only have 2 possible states: "enabled"/"disabled". Their interface analogs are options in setup dialogs of many programs, including MetaTrader 5: Each flag may be either enabled or disabled. Checking the states of such features allows branching the logic of the program execution, thus the type name.

Logic type is defined in MQL5 under the bool keyword and consumes 1 byte of memory. For this type, two constants are reserved: true and false. Moreover, situations are permissible (and programmers often make use of it), in which bool is the result of computations with integers and real numbers, value 0 being interpreted as false, and any others as true.

Back-interpretation of the bool type value as a number is supported, as well: true is considered as 1 and false as 0.

Examples of logic type variables are given in file MQL5/Scripts/MQL5Book/p2/TypeBool.mq5.

```
void OnStart()
{
  bool t = true;          // true
  bool f = false;         // false
  bool x = 100;           // x = true
  bool y = 0;             // y = false
  int i = true;           // i = 1
  int j = false;          // j = 0
}

```

For logic type, a set of special logic operations is provided (see [Logical (Boolean) Operations](/en/book/basis/expressions/operators_logical) and [Comparison Operations](/en/book/basis/expressions/operators_relational)).
