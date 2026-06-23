# Continue jump

The continue statement breaks the current iteration of the innermost loop containing continue and initiates the next iteration. The statement can only be used inside for, while and do loops. Execution of continue inside for results in the next calculation of the expression in the loop header (increment/decrement of the loop variable), after which the loop continuation condition is checked. Executing continue inside while or do immediately results in checking the condition in the loop header.

The statement consists of the keyword continue and a semicolon:

```
continue ;

```

It is usually placed in one of the branches of the [if/else](/en/book/basis/statements/statements_if) or [switch](/en/book/basis/statements/statements_switch) conditional statement.

For example, we can generate a times table with gaps: when the product of two indexes is odd, the corresponding array element will remain zero (StmtJumpContinue.mq5).

```
int a[10][10] = {0};
for(int i = 0; i < 10; ++i)
{
   for(int j = 0; j < 10; ++j)
   {
      if((j * i) % 2 == 1)
         continue;
      a[i][j] = (i + 1) * (j + 1);
   }
}
ArrayPrint(a);

```

And here's how you can calculate the sum of the positive elements of an array.

```
int b[10] = {1, -2, 3, 4, -5, -6, 7, 8, -9, 10};
int sum = 0;
for(int i = 0; i < 10; ++i)
{
   if(b[i] < 0) continue;
   sum += b[i];
}
Print(sum); // 33

```

Note that the same loop can be rewritten without continue but with a greater nesting of code blocks:

```
for(int i = 0; i < 10; ++i)
{
   if(b[i] >= 0)
   {
      sum += b[i];
   }
}

```

Thus, operator continue is often used to simplify code formatting (especially if there are several conditions to pass). However, which of the two approaches to choose is a matter of personal preference.
