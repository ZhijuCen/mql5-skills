# Break jump

The break operator is intended for early termination of the for, while, do loops, as well as exit from the switch selection statement. The operator can only be applied within the specified statements and only affects the one immediately containing break if there are multiple nested ones. After processing the break statement, program execution continues to the statement following the interrupted loop or switch.

The syntax is very simple: the keyword break and a semicolon:

```
break ;

```

When used inside loops, break is usually implemented in one of the branches of the [if/else](/en/book/basis/statements/statements_if) conditional operator.

Consider a script that prints the current system time counter once per second, but no more than 100 times. It provides for handling the interruption of the process by the user: for this, the function IsStopped is polled in the conditional operator if and its dependent statement contains break (StmtJumpBreak.mq5).

```
int count = 0;
while(++count < 100)
{
   Comment(GetTickCount());
   Sleep(1000);
   if(IsStopped())
   {
      Print("Terminated by user");
      break;
   }
}

```

In the following example, a diagonal matrix is filled in with a times table (the top right corner will remain filled with zeros).

```
int a[10][10] = {0};
for(int i = 0; i < 10; ++i)
{
   for(int j = 0; j < 10; ++j)
   {
      if(j > i)
         break;
      a[i][j] = (i + 1) * (j + 1);
   }
}
ArrayPrint(a);

```

When the inner loop variable j is greater than the outer loop variable i, the break statement breaks the inner loop. Of course, this is not the best way to fill the matrix diagonally: it would be easier to loop over j from 0 to i without any break, but here it demonstrates the presence of equivalent constructions with break and without break.

Although things may not be so obvious in production projects, it is recommended to avoid the break operator whenever possible and replace it with additional variables (for example, a boolean variable with a "telling" name needAbreak), which should be used in terminal expressions in loop headers to break them in the standard way.

Imagine that two nested loops are used to find duplicate characters in a string. The first loop sequentially makes each character of the string current and the second runs through the remaining (to the right) characters.

```
string s = "Hello, " + Symbol();
ushort d = 0;
const int n = StringLen(s);
for(int i = 0; i < n; ++i)
{
   for(int j = i + 1; j < n; ++j)
   {
      if(s[i] == s[j])
      {
         d = s[i];
         break;
      }
   }
}

```

If the characters at positions i and j match, remember the duplicate character and exit the loop via break.

It could be assumed that the variable d should contain the letter 'l' after the execution of this fragment. However, if you place the script on the most popular instrument "EURUSD", the answer will be 'U'. The thing is that break breaks only the inner loop, and after finding the first duplicate ('ll' in the word "Hello"), the loop continues on i. Therefore, to exit from several nested loops at once, additional measures must be taken.

The most popular way is to include in the condition of the outer loop (or all outer loops) a variable that is filled in the inner loop. In our case, there is already such a variable: d.

```
for(int i = 0; i < n && d == 0; ++i)
{
   for(int j = i + 1; j < n; ++j)
   {
      if(s[i] == s[j])
      {
         d = s[i];
         break;
      }
   }
}

```

Checking d for being equal to 0 will now stop the outer loop after finding the first duplicate. But the same check can be added to the inner loop, which eliminates the need to use break.

```
for(int i = 0; i < n && d == 0; ++i)
{
   for(int j = i + 1; j < n && d == 0; ++j)
   {
      if(s[i] == s[j])
      {
         d = s[i];
      }
   }
}

```
