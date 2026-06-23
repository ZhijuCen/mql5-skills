# If selection

The if statement has several forms. In its simplest case, it executes the dependent statement if the specified condition is true:

```
if ( condition )
  statement

```

If the condition is false, the statement is skipped and the execution immediately jumps to the rest of the algorithm (subsequent statements, if any).

The statement can be simple or compound. A condition is an expression of a boolean or castable type.

The second form allows you to specify two branches of actions: not only for the true condition (statement_A) but also for the false (statement_B):

```
if ( condition )
  statement_A
else
  statement_B

```

Whichever of the controlled statements is executed, the algorithm will then continue following the statements below the if/else statement.

For example, a script can follow a different strategy depending on the timeframe of the chart it is placed on. For this purpose, it is enough to analyze the value returned by the [Period](/en/book/applications/charts/charts_main_properties) built-in function. The value is of the [ENUM_TIMEFRAMES](/en/book/applications/timeseries/timeseries_symbol_period) enum type. If it is less than PERIOD_D1, it means short-term trading, otherwise, long-term trading (StmtSelectionIf.mq5).

```
if(Period() < PERIOD_D1)
{
   Print("Intraday");
}
else
{
   Print("Interday");
}

```

As a statement in the else branch, it is allowed to specify the following operator if, and thus arrange them into a chain of successive checks. For example, the following fragment counts the number of capital letters and punctuation symbols (more precisely, non-Latin letters) in a string.

```
string s = "Hello, " + Symbol();
int capital = 0, punctuation = 0;
for(int i = 0; i < StringLen(s); ++i)
{
   if(s[i] >= 'A' && s[i] <= 'Z')
      ++capital;
   else if(!(s[i] >= 'a' && s[i] <= 'z'))
      ++punctuation;
      
}
Print(capital, " ", punctuation);

```

The loop is organized through all the characters of the string (numbering starts from 0) and the [StringLen](/en/book/common/strings/strings_init) function returns the length of the string. The first if checks each character to see if it belongs to the range 'A' to 'Z' and, if successful, increments the capital counter by 1. If the character does not fall into this range, the second if is run, in which the condition for belonging to the range of lowercase letters (s[i] >= 'a' && s[i] <= 'z') is inverted with '!'. In other words, the condition means that the character is not in the given range. Given two consecutive checks, if the character is not an uppercase letter (else) and not a lowercase letter (the second if), we can conclude that the character is not a letter of the Latin alphabet. In this case, we increment the punctuation counter.

The same checks could be written in a more detailed form, with '{...}' blocks for clarity.

```
int capital = 0, small = 0, punctuation = 0;
for(int i = 0; i < StringLen(s); ++i)
{
   if(s[i] >= 'A' && s[i] <= 'Z')
   {
      ++capital;
   }
   else
   {
      if(s[i] >= 'a' && s[i] <= 'z')
      {
         ++small;
      }
      else
      {
         ++punctuation;
      }
   }
}

```

The use of curly brackets helps to avoid logical errors associated which can occur when the programmer is only guided by indentation in the code. In particular, the most common problem is called the "hanging" else.

When if statements are nested, sometimes there are fewer else branches than if. Here is one example:

```
factor = 0.0;
if(mode > 10)
   if(mode > 20)
      factor = +1.0;
else
   factor = -1.0;

```

The indentation indicates what kind of logic the programmer meant: factor should become +1 when mode is greater than 20, remain equal to 0 when mode is between 10 and 20, and change to -1 otherwise (mode <= 10). But will the code work that way?

In MQL5, each else is assumed to refer to the nearest previous if (which does not have a else). As a result, the compiler will treat the statements as follows:

```
factor = 0.0;
if(mode > 10)
   if(mode > 20)
      factor = +1.0;
   else
      factor = -1.0;

```

So the factor will be -1 in the mode range from 10 to 20, and 0 for mode <= 10. The most interesting thing is that the program does not produce any formal errors, neither during compilation nor during execution. And yet it doesn't work correctly.

To eliminate such subtle logical problems allows the placement of curly brackets.

```
if(mode > 10)
{
   if(mode > 20)
      factor = +1.0;
}
else
   factor = -1.0;

```

To keep the design consistent, it is desirable to use blocks in all branches of the statement if at least one block has already been required in it.

When using the loop to check equality, take into account the possibility of a typo when one '=' is written instead of two characters '=='. This turns the comparison into an assignment, and the assigned value is analyzed as a logical condition. For example,

```
// should have been x == y + 1, which would give false and skip the if
if(x = y + 1) // warning: expression not boolean
{
   // assigned x = 5 and treated x as true, so if is executed
}

```

The compiler will produce a warning "expression not boolean".
