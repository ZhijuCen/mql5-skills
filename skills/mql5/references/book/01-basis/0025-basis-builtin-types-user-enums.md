# Custom enumerations

Custom enumerations are structurally based on the int type, and the principles of using them completely coincide with what has been discussed above in the preceding section dealing with embedded enumerations. Therefore, we are describing custom enumerations here, although, strictly speaking, they are not embedded.

To describe your own enumeration in the MQL5 code, you will use the keyword enum. The simplest description form is as follows:

```
enum name
{
  element1,
  element2,
  element3
};

```

This description registers in the program an enumeration type named name with brace-enclosed comma-separated elements (their amount is only limited by the highest int value, which can be considered as no limitations in terms of practical tasks). Identifiers element1, element2, and element3 can be then used in the program within the context, in which they have been defined: Globally (i.e., outside of all functions) or inside of a function (see section [Context, visibility, and lifetime of variables](/en/book/basis/variables/scope_and_lifetime)).

Please consider the semicolon following the closing brace. It is needed since the enumeration description is a separate statement, and semicolons must be placed after any MQL5 statement.

By default, identifiers take constant values, starting with 0, each subsequent being 1 greater than the preceding one. If necessary, the programmer may define a specific value for each element, after '=' to the right of the identifier. For instance, the entry above is equivalent to this one:

```
enum name
{
  element1 = 0,
  element2 = 1,
  element3 = 2
};

```

It is permitted to specify as value only constants or expressions the compiler can compute at the compilation stage (for more details, please see the example below).

If the values are not defined for all elements, the skipped values are computed automatically based on the nearest known (preceding) ones by adding 1. For example,

```
enum name
{
  element1 = 1,
  element2,
  element3 = 10,
  element4,
  element5
};

```

Here, the first two elements take values 1 and 2 (computed), while those starting with the third one take 10 (specified explicitly), 11, and 12 (the last two ones are computed based on 10).

In script TypeUserEnum.mq5, there are some examples of describing custom enumerations.

```
const int zero = 0; // runtime value is not known at compile time
 
enum
{
  MILLION = 1000000
};
 
enum RISK
{
  // OFF      = zero, // error: constant expression required
  LOW      = -1,
  MODERATE = -2,
  HIGH     = -3,
};
 
enum INCOME
{
  LOW      = 1,
  MODERATE = 2,
  HIGH     = 3,
  ENORMOUS = MILLION,
};
 
void OnStart()
{
  enum INTERNAL
  {
    ON,
    OFF,
  };
 
  // int x = LOW; // ambiguous access, can be one of
  int x = RISK::LOW;
  int y = INCOME::LOW;
}

```

Enumeration INTERNAL shows the possibility of describing it inside of the function and, in doing so, limits the visibility/availability region of this type, which is useful in terms of name collisions.

Enumeration RISK shows that elements may be assigned with negative values. Commented element OFF cannot be described due to the attempt to initialize it with a non-constant expression: In this case, variable zero is specified there, the value of which cannot be computed by the compiler.

In enumeration INCOME, element ENORMOUS is initialized successfully by the value from the MILLION element of the other enumeration defined above. Enumerations are created at the moment of compiling and therefore, they are available in initialization expressions.

Enumeration with MILLION has no name, such enumerations are called anonymous. Their basic application is to declare constants. However, named enumerations are used more often for constants, since they allow grouping elements by their meanings.

Since there 2 enumerations defined in the example, both having elements with identical names, specifying the LOW identifier when declaring variable x leads to the "ambiguous access" compilation error, because it is not clear the element of which enumeration is meant. Please note that identifiers may have (and they do, in this case) different values.

To solve this issue, there is a special context operator: Two colons, "::". They help form the complete identifier of the language element, i.e., the enumeration element, in our case: First, the enumeration name is specified, then operator "::", and after that the element identifier. Example: RISK::LOW and INCOME::LOW. We will get to know about all operators in the relevant section.
