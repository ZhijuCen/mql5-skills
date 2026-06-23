# Do loop

This loop is similar to the while loop, but its condition is checked after the loop body. Due to this, controlled statements must be executed at least once.

Two keywords, do and while, are used to describe the loop:

```
do
  loop body
while ( condition ) ;

```

Thus, the loop header is separated, and after the logical condition in brackets, there should be a semicolon. The condition cannot be omitted. When it becomes false, the loop exits.

Variables included in the condition must be defined before the loop.

The loop body is a simple or compound statement.

The following example calculates a sequence of numbers starting from 1, in which each next number is obtained by multiplying the previous one by the square root of two, the predefined constant M_SQRT2 (StmtLoopsDo.mq5).

```
double d = 1.0;
do
{
   Print(d);
   d *= M_SQRT2;
}
while(d < 100.0);

```

The process terminates when the number exceeds 100.
