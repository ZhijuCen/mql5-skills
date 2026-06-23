# Switch selection

The switch operator provides the ability to choose one of several algorithm options. As a rule, the number of options is significantly higher than two, because otherwise, it is easier to use the if/else statement. In theory, the chain of if/else statements allows having an equivalent of switch in many cases (but not all). An important feature of switch is that all options are selected (identified) based on the integer expression value, usually a variable.

In general case, the switch statement looks as follows:

```
switch ( expression )
{
   case constant-expression : statements [break; ]
   ...
   [ default : statements ] 
}

```

The statement header starts with the keyword switch. It must be followed by an expression in parentheses. The block with curly brackets is also required.

Integer values that can be obtained by evaluating an expression should be specified as constants after the case keyword. A constant is a literal of any [integer types](/en/book/basis/builtin_types/integer_numbers), for example, int (10, 123), ushort (characters 'A', 's', '*' etc.), or [enum](/en/book/basis/builtin_types/enums) elements. Real numbers, variables, or expressions are not allowed here.

There may be many such case options, or may not be at all, which is indicated by semicircular brackets with index opt(n). All variants must have unique constants (no repetitions).

For each alternative declared with case, a statement must be written after the colon, which will be executed if the value of the expression is equal to the corresponding constant. Again, a statement can be simple or compound. In addition, it is permissible to write several simple statements without enclosing them in curly brackets: they will still be executed as a group (a compound statement).

One or more of these statements can be followed by the [break](/en/book/basis/statements/statements_break) jump statement.

If there is a break, after executing the previous statements from the case branch, the switch statement exits, i.e., control is transferred to the statements below switch.

In the absence of break, the statements of the next branch or several branches case continue to be executed, that is, until the first encountered break or the end of the block switch. This is called "fall-through".

Thus, the switch statement not only allows splitting the algorithm execution flow into several alternatives but also combining them, which is not available for the if operator. On the other hand, in the switch statement, unlike if, you cannot select a range of values as a condition for activating alternatives.

The default keyword allows you to set the default algorithm variant, that is, for any other expression values except for constants from all cases. The default option may not be present, or there must be only one.

The sequence in which case constants and default are listed can be arbitrary.

Even if there is no algorithm for the default branch yet, it is recommended to make it explicitly empty, i.e. containing break. An empty default will remind you and other programmers that other options exist but are considered unimportant because otherwise, the default branch would have to signal an error.

Several case variants with different constants can be listed one below the other (or left to right) without statements, but the last one must have a statement. Such combined cases are indicated on the diagram by the index (i).

Here is the simplest and most useless switch:

```
switch(0)
{
}

```

Let's consider a more complex example with different modes (StmtSelectionSwitch.mq5). In it, the switch operator is placed inside the loop to show how its work depends on the values of the control variable i.

```
for(int i = 0; i < 7; i++)
{
   double factor = 1.0;
   
   switch(i)
   {
      case -1:
         Print("-1: Never hit");
         break;
      case 1:
         Print("Case 1");
         factor = 1.5;
         break;
      case 2: // fall-through, no break (!)
         Print("Case 2");
         factor *= 2;
      case 3: // same statements for 3 and 4
      case 4:
         Print("Case 3 & 4");
         {
            double local_var = i * i;
            factor *= local_var;
         }
         break;
      case 5:
         Print("Case 5");
         factor = 100;
         break;
      default:
         Print("Default: ", i);
   }
   
   Print(factor);
}

```

The -1 option will fail because the loop changes the variable i from 0 to 6 (inclusive). When i is 0, the default branch will trigger. It will also take control when i is equal to 6. All other possible i values are distributed according to the corresponding case directives. At the same time, there is no break statement after case 2, and therefore the code for options 3 and 4 will be executed in addition to 2 (in such cases, it is always recommended to leave a comment that this was done intentionally).

Cases 3 and 4 have a common statement block. But it is also important to note here that if you want to declare a local variable inside one of the case options, you need to enclose the statements in a nested compound block ('{...}'). Here, the variable local_varis defined this way.

It is worth advising that in the default case, there is no break statement. It's redundant because default is written last in this case. However, many programmers advise inserting break at the end of any option, even the last one, because it can cease to be the last in the process of subsequent modifications of the code, and then it is easy to forget to add break, which will probably lead to an error in the program logic.

If in switch there is no default, and the header expression does not match any of the case constants, the entire switch is skipped.

As a result of the script execution, we will receive the following messages in the log:

```
Default: 0
1.0
Case 1
1.5
Case 2
Case 3 & 4
8.0
Case 3 & 4
9.0
Case 3 & 4
16.0
Case 5
100.0
Default: 6
1.0

```
