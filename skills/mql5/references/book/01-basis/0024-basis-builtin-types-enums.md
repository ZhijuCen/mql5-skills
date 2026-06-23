# Enumerations

Enumerations are a group of types built in MQL5, each containing a set of named constants to describe related concepts or properties. These constants are also referred to as enumeration elements.

For example, enumeration ENUM_DAY_OF_WEEK contains constants for all days of the week:

| Identifier (ID) | Description | Value |
| --- | --- | --- |
| SUNDAY | Sunday | 0 |
| MONDAY | Monday | 1 |
| TUESDAY | Tuesday | 2 |
| WEDNESDAY | Wednesday | 3 |
| THURSDAY | Thursday | 4 |
| FRIDAY | Friday | 5 |
| SATURDAY | Saturday | 6 |

Enumeration ENUM_ORDER_TYPE describes all the order types supported in MetaTrader 5:

| Identifier (ID) | Description | Value |
| --- | --- | --- |
| ORDER_TYPE_BUY | Market buy order | 0 |
| ORDER_TYPE_SELL | Market sell order | 1 |
| ORDER_TYPE_BUY_LIMIT | Buy Limit pending order | 2 |
| ORDER_TYPE_SELL_LIMIT | Sell Limit pending order | 3 |
| ORDER_TYPE_BUY_STOP | Buy Stop pending order | 4 |
| ORDER_TYPE_SELL_STOP | Sell Stop pending order | 5 |
| ORDER_TYPE_BUY_STOP_LIMIT | Upon reaching the order price, Buy Limit pending order is placed at the StopLimit price | 6 |
| ORDER_TYPE_SELL_STOP_LIMIT | Upon reaching the order price, Sell Limit pending order is placed at the StopLimit price | 7 |
| ORDER_TYPE_CLOSE_BY | Order for closing a position by an opposite one | 8 |

There are a few dozens of various enumerations. Their names are prefixed with "ENUM_". We are going to learn them as we move through the relevant domain areas.

Each enumeration is an independent type. However, their internal representation is identical, i.e., four-byte integer (int). Each enumeration constant is coded with one number or another, but in most cases, the programmer does not need to remember these numbers, since the whole point of using enumeration is exactly to replace internal representations with evident identifiers.

The compiler ensures that the enumeration value is always one of the redefined constants. Otherwise, a warning or compilation error will occur (contextually, see the example).

This is how the ENUM_DAY_OF_WEEK enumeration appears "underneath" (script MQL5/Scripts/MQL5Book/p2/TypeEnum.mq5).

```
void OnStart()
{
  ENUM_DAY_OF_WEEK sun = SUNDAY;     // sun = 0
  ENUM_DAY_OF_WEEK mon = MONDAY;     // mon = 1
  ENUM_DAY_OF_WEEK tue = TUESDAY;    // tue = 2
  ENUM_DAY_OF_WEEK wed = WEDNESDAY;  // wed = 3
  ENUM_DAY_OF_WEEK thu = THURSDAY;   // thu = 4
  ENUM_DAY_OF_WEEK fri = FRIDAY;     // fri = 5
  ENUM_DAY_OF_WEEK sat = SATURDAY;   // sat = 6
  
  int i = 0;
  ENUM_DAY_OF_WEEK x = i; // warning: implicit enum conversion
  ENUM_DAY_OF_WEEK y = 1; // ok, equals to MONDAY
  ENUM_ORDER_TYPE buy = ORDER_TYPE_BUY;   // buy = 0
  ENUM_ORDER_TYPE sell = ORDER_TYPE_SELL; // sell = 1
  // ...
  
  // warning: implicit conversion
  //          from 'enum ENUM_DAY_OF_WEEK' to 'enum ENUM_ORDER_TYPE'
  //          'ENUM_ORDER_TYPE::ORDER_TYPE_SELL' will be used
  //          instead of 'ENUM_DAY_OF_WEEK::MONDAY'
  ENUM_ORDER_TYPE type = MONDAY;
  // compilation error: uncomment to reproduce
  // ENUM_DAY_OF_WEEK day = ORDER_TYPE_CLOSE_BY; // cannot convert enum
  // ENUM_DAY_OF_WEEK z = 10; // '10' - cannot convert enum
}

```

All constants of the days of the week are coded with numbers from 0 through 6, Sunday being the starting point. Basically, constants should not necessarily have consecutive numbers or start with 0. There are enumerations where this is not the case.

Please note that the same constants can mean different things in different enumeration types. For instance, for orders ORDER_TYPE_BUY and ORDER_TYPE_SELL in the ENUM_ORDER_TYPE enumeration, the same values (0 and 1) are used as for the days of week SUNDAY and MONDAY in ENUM_DAY_OF_WEEK.

When copying the value from a simple integer variable i into the enumeration variable x, the compiler gives a warning, since there can be a value other than the permitted constants in variable i at the program execution stage.

In variable y, we record number 1 which means MONDAY, and the compiler considers this to be a correct operation.

An attempt to write the constant of one enumeration into the variable of another enumeration (as MONDAY for variable type in the example above) may cause a warning about an implicit type conversion. This happens if the constant being written has the same value as one of the target enumeration elements. In other words, each of the two enumerations has its own element with the relevant value. Then the compiler performs an implicit conversion in the programmer's place automatically, but it uses a warning to "ask" the programmer to check whether everything is going as intended: The fact that MONDAY will be replaced with ORDER_TYPE_SELL is weird, indeed; however, we did that intentionally here for illustrative purposes.

If the element being copied does not match by its value with any element of another enumeration, a compilation error is generated, since an implicit conversion is impossible, such as when writing ORDER_TYPE_CLOSE_BY in variable day.

The commented string with variable z causes a compilation error, too, since the value 10 does not belong to ENUM_DAY_OF_WEEK. If the programmer is sure that, in an exotic case, there is still a need for recording a random value in the enumeration type variable, they can use explicit typecasting.

Explicit and implicit typecasting will be discussed in the section entitled [Typecasting](/en/book/basis/conversion).

MQL5 allows a programmer to declare their own applied enumerations using the keyword, enum. This feature is described in the next section, [Custom Enumerations](/en/book/basis/builtin_types/user_enums) (enum).
