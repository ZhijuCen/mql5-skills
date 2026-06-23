# While loop

This loop is described using the while keyword. It repeats the execution of controlled statements as long as the logical expression in its header is true.

```
while ( condition )
  loop body

```

The condition is an arbitrary expression of a boolean type. The presence of the condition is mandatory. If the condition is false before the start of the loop, the loop will never execute.

Unlike C++, MQL5 does not support defining variables in the while loop header.

Variables included in the condition must be defined before the loop.

The loop body is a simple or compound statement.

The while loop is usually used when the number of iterations is not defined. So, an example with the loop that outputs a computer timer counter every second can be written using a while loop and checking the stop flag (by calling the IsStopped function) as follows (StmtLoopsWhile.mq5):

```
while(!IsStopped())
{
   Comment(GetTickCount());
   Sleep(1000);
}
Comment("");

```

Also, the while loop is convenient when the loop termination condition can be combined with the modification of variables in one expression. The next loop is executed until the variable i reaches zero (0 is treated as false).

```
int i = 5;
while(--i) // warning: expression not boolean
{
   Print(i);
}

```

However, in this case, the header expression is not boolean (and is implicitly converted to false or true). The compiler generates the relevant warning. It is desirable to always compose expressions taking into account the expected (according to the rules) characteristics. Below is the correct loop version:

```
int i = 5;
while(--i > 0)
{
   Print(i);
}

```

The loop can also be used with a simple statement (no block):

```
while(i < 10)
   Print(++i);

```

Note that a simple statement ends with a semicolon. It also demonstrates that changing the variable being checked in the header is done inside the loop.

When working with loops, be careful when using unsigned integers. For example, the next loop will never end, because its condition is always true (in theory, the compiler could issue warnings in such places, but it does not). After zero, the counter will "turn" into a large positive number (UINT_MAX) and the loop will continue.

```
uint i = 5;
while(--i >= 0)
{
   Print(i);
}

```

From the user's point of view, the MQL program will freeze (stop responding to commands), although it will still consume resources (processor and memory).

while loops can be nested like other kinds of repetition statements.
