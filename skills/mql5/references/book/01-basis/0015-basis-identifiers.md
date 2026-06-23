# Identifiers

As we are going to see soon, programs are built of multiple elements that must be referred to by unique names to avoid confusion. These names are exactly what is called identifiers.

Identifier is a word composed by certain rules: Only Latin characters, underscore characters ('_'), and digits may be used in it, and the first character may not be a digit. Letters can be small (lower-case) and capital (upper-letter).

The maximum identifier length is 63 characters. The identifier may not coincide with any service words of MQL5, such as type names. You can find the full list of service words in the Help. Violating any of the identifier forming rules will cause a compilation error.

Here are some correct identifiers:

```
i             // single character
abc           // lower-case letters
ABC           // upper-case letters
Abc           // mixed-case letters
_abc          // underscore at the beginning
_a_b_c_       // underscore anywhere
step1         // digit
_1step        // underscore and digit

```

We have already seen in the script HelloChart how identifiers are used as names of variables and functions.

It is recommended to provide identifiers with meaningful names, from which the purpose or content of the relevant element becomes clear. In some cases, single-character identifiers are used, which we will discuss in the section dealing with [loops](/en/book/basis/statements/statements_for).

There are some common practices for composing identifiers. For instance, if we choose a name for a variable that stores the value of profit factor, the following options will be good:

```
ProfitFactor   // "camel" style, all words start with a capital letter
profitFactor   // "camel" style, all words but the first one start with a capital letter
profit_factor  // "snake" style, the underscore is put between all words

```

In many programming languages, different styles are used to name different entities. For example, a practice may be followed, in which variable names only start with a lower-case letter, while class names (see [Part 3](/en/book/oop)) with upper-case letters. This helps the programmer analyze the source code when working in a team or if they return to their own code fragment after a long break.

Along the above ones, there are other styles, some of which are used in special cases:

```
profitfactor   // "smooth" style, all letters are lower-case
PROFITFACTOR   // "smooth" style, all letters are upper-case
PROFIT_FACTOR  // "macro" style, all letters are upper-case with underscores between the words

```

All capitals are sometimes used in the names of [constants](/en/book/basis/variables/const_variables).

"Macro" style is conventionally used in the names of [preprocessor](/en/book/basis/preprocessor/preprocessor_define_overview) macro descriptions.
