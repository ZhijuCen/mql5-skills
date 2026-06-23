# Simple statements (expressions)

Simple statements contain [expressions](/en/book/basis/expressions), such as assigning new values or calculation results to variables, as well as function calls.

Formally, the syntax looks like this:

```
expression ;

```

The semicolon at the end is important here. Since MQL5 source codes support free formatting, the ';' is the only delimiter that tells the compiler where the previous statement ended and the next one began. As a rule, statements are written on separate lines, for example, like this:

```
int i = 0, j = 1, k;   // declaration statement
++i;                   // simple statement
j += i;                // simple statement
k = (i + 1) * (j + 1); // simple statement
Print(i, " ", j);      // simple statement

```

However, the rules do not prohibit shorthand code writing:

```
int i=0,j=1;++i;j+=i;k=(i+1)*(j+1);Print(i," ",j);

```

If it weren't for the ';', adjacent expressions could silently "stick together" and lead to unintended results. For example, the expression x = y - 10 * z could well be two: x = y; and -10 * z; (-10 with a unary minus). How is this possible?

The fact is that it is syntactically permissible to write a statement that actually works in vain, i.e., does not save the result. Here is another example:

```
i + j; // warning: expression has no effect

```

The compiler issues an "expression has no effect" warning. The possibility to construct such expressions is necessary because the object types, which we will learn in [Part 3](/en/book/oop), allow for the [operator overloading](/en/book/oop/classes_and_interfaces/classes_operator_overloading), i.e., we can replace the usual meaning of operator symbols with some specific actions. Then, if the type of i and j is not int, but some class with an overridden addition operation, such a notation will have an effect, and the compiler will not issue a warning.

Simple statements can only be written inside compound statements. For example, calling the Print function outside of a function will not work:

```
Print("Hello ", Symbol());
void OnStart()
{
}

```

We will get a cascade of errors::

```
'Print' - unexpected token, probably type is missing?
'Hello, ' - declaration without type
'Hello, ' - comma expected
'Symbol' - declaration without type
'(' - comma expected
')' - semicolon expected
')' - expressions are not allowed on a global scope

```

The most relevant, in this case, is the last one: "expressions are not allowed in the global context."
