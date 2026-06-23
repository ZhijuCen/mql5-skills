# Return jump

The return operator is designed to return control from [functions](/en/book/basis/functions). Given that all executable statements are inside a particular function, it can be indirectly used to interrupt containing it loops for, while, and do of any nesting level. It should be taken into account that unlike continue and, especially, break, all statements following interrupted loops inside the function will also be ignored.

The syntax for the return operator:

```
return ([expression]) ;

```

The need to specify an expression is determined by the function signature (more on this will be discussed in the [relevant section](/en/book/basis/functions/functions_return)). For a general understanding of how return works in the context of control statements, let's view an example with the main script function OnStart. Since it is of type void, i.e. it does not return anything, the operator takes the following form:

```
return ;

```

In the section on [break](/en/book/basis/statements/statements_break), we implemented an algorithm for finding duplicate characters in a string. To break two nested loops, we not only use break but also modify the condition of the outer loop.

With the return operator, this can be done in a simpler way (StmtJumpReturn.mq5).

```
void OnStart()
{
   string s = "Hello, " + Symbol();
   const int n = StringLen(s);
   for(int i = 0; i < n; ++i)
   {
      for(int j = i + 1; j < n; ++j)
      {
         if(s[i] == s[j])
         {
            PrintFormat("Duplicate: %c", s[i]);
            return;
         }
      }
   }
   
   Print("No duplicates");
}

```

If equality is found in the if operator, we display the symbol and exit the function. If this algorithm was in a custom function other than OnStart, we could define a return type for it (for example, ushort instead of void) and pass the found character using the full form return to the calling code.

Since the double letter 'l' is known to exist in the test string, the statement after the loops (Print) will not be executed.
