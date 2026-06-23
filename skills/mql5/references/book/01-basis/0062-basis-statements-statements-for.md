# For loop

This loop is implemented by a statement with the for keyword, hence the name. In a generalized form, it can be described as follows:

```
for ( [initialization] ; [condition] ; [expression] )
  loop body

```

In the title, after the word 'for', the following is indicated in parentheses:

- Initialization: a statement for one-time initialization before the start of the loop;
- Condition: a boolean condition that is checked at the beginning of each iteration, and the loop runs as long as it is true;
- Expression: formula of calculations performed at the end of each iteration, when all statements in the loop body have been passed.

The loop body is a simple or compound statement.

All three header components are optional and may be omitted in any combination, including their absence.

Initialization may include the declaration of variables (along with setting initial values) or the assignment of values to already existing variables. Such variables are called loop variables. If they are declared in the header, then their scope and lifetime are limited to the loop.

The loop starts executing if, after initialization, the condition is true, and continues executing for as long as it is true at the beginning of each subsequent iteration. If during the next check, the condition is violated, the loop exits, i.e., control is transferred to the statement written after the loop and its body. If the condition is false before the start of the loop (after initialization), it will never be executed.

The condition and expression usually include loop variables.

Executing a loop means executing its body.

The most common form of the for loop has a single loop variable that controls the number of iterations. In the following example, we calculate the squares of the numbers in the a array.

```
int a[] = {1, 2, 3, 4, 5, 6, 7};
const int n = ArraySize(a);
for(int i = 0; i < n; ++i)
   a[i] = a[i] * a[i];
ArrayPrint(a);    // 1  4  9 16 25 36 49
// Print(i);      // error: 'i' - undeclared identifier

```

This loop is executed in the following steps:

1. A variable i with an initial value of 0 is created.
2. The condition is checked of whether the variable i is less than the size of the loop n. As long as it is true, the loop continues. If it is false, we jump to the statement calling the ArrayPrint function.
3. If the condition is true, the statements of the loop body are executed. In this case, the i-th element of the array gets the product of the initial value of this element by itself, i.e. the value of each element is replaced by its square.
4. The variable i is incremented by 1.

Then everything repeats, starting from step 2. After exiting the loop, its variable i is destroyed, and an attempt to access it will cause an error.

The expression for step 4 can be of arbitrary complexity, not just an increment of the loop variable. For example, to iterate over even or odd elements, one could write i += 2.

Regardless of how many statements make up the body of the loop, it is recommended to write it on a separate line (lines) from the header. This makes the step-by-step debugging process easier.

Initialization may include multiple variable declarations, but they must be of the same type because they are one statement. For example, to rearrange elements in reverse order, you can write such a loop (this is just a demonstration of the loop, there is a built-in function ArrayReverse to reverse the order in an array, see [Copying and editing arrays](/en/book/common/arrays/arrays_edit)):

```
for(int i = 0, j = n - 1; i < n / 2; ++i, --j)
{
   int temp = a[i];
   a[i] = a[j];
   a[j] = temp;
}
ArrayPrint(a);    // 49 36 25 16  9  4  1

```

The auxiliary variable temp is created and deleted on each pass of the loop, but the compiler allocates memory for it only once, as for all local variables, when entering the function. This optimization works well for built-in types. However, if [a custom class object](/en/book/oop) is described in the loop, then its constructor and destructor will be called at each iteration.

It is acceptable to change the loop variable in the loop body, but this technique is only used in very exotic cases. It is not recommended to do this, as this may cause errors (in particular, processed elements can be skipped or execution can get into an infinite loop).

To demonstrate the ability to omit header components, let's imagine the following problem: We need to find the number of elements of the same array the sum of which is less than 100. To do this, we need a counter variable k defined before the loop because it must continue to exist after its completion. We will also create the sum variable to calculate the sum on a cumulative basis.

```
int k = 0, sum = 0;
for( ; sum < 100; )
{
  sum += a[k++];
}
 
Print(k - 1, " ", sum - a[k - 1]); // 2 85

```

Thus, there is no need to do initialization in the header. In addition, the k counter is incremented using a postfix increment directly in the expression that calculates the sum (when accessing an array element). Therefore, we do not need an expression in the title.

At the end of the loop, we print out k and the sum minus the last added element, because it was the one that exceeded our limit of 100.

Note that we are using a compound block even though there is only one statement in the loop body. This is useful because when the program grows, everything is already done for adding additional statements inside the brackets. In addition, this approach guarantees a uniform style for all loops. But the choice, in any case, is up to the programmer.

In the explicit, maximally abbreviated version, the cycle header might look like this:

```
for( ; ; )
{
   // ...       // periodic actions
   Sleep(1000); // pause the program for 1 second
}

```

If there are no statements in the body of such a loop that would interrupt the loop due to some conditions, it will be executed indefinitely. We'll learn how to break and test conditions in [Break ](/en/book/basis/statements/statements_break)[jump](/en/book/basis/statements/statements_break) and [If ](/en/book/basis/statements/statements_if)[selection](/en/book/basis/statements/statements_if) respectively.

Such looping algorithms are usually used in services (they are designed for constant background work) to monitor the state of the terminal or external network resources. They usually contain statements that pause the program at a specified interval, for example, using the built-in function [Sleep](/en/book/common/timing/timing_sleep). Without this precaution, an infinite loop will load 100% of one processor core.

Script StmtLoopsFor.mq5 contains an infinite loop at the end, but it is for demonstration purposes only.

```
for( ; ; )
{
   Comment(GetTickCount());
   Sleep(1000); // 1000 ms
  
   // the loop can be exited only by deleting the script at the user's command
   // after 3 seconds of waiting we will get the message 'Abnormal termination'
}
Comment("");  // this line will never be executed

```

In the loop, once per second, the computer's internal timer ([GetTickCount](/en/book/common/timing/timing_count)) is displayed using the [Comment](/en/book/common/output/output_comment) function: the value is displayed in the upper left corner of the chart. Only the user can interrupt the loop by deleting the entire script from the chart (the "Delete" button in the Experts dialog). This code does not check for such user requests to stop inside the loop, although there is a built-in function [IsStopped](/en/book/common/environment/env_stop) for this purpose. It returns true if the user has given the command to stop. In the program, especially if there are loops and long-term calculations, it is desirable to provide for checking the value of this function and voluntarily terminate the loop and the entire program upon receipt of true. Otherwise, the terminal will forcibly terminate the script after 3 seconds of waiting (with output to the "Abnormal termination" log), which will happen in this example.

A better version of this loop should be:

```
for( ; !IsStopped(); ) // continue until user interrupt
{
   Comment(GetTickCount());
   Sleep(1000); // 1000 ms
}
Comment("");    // will clear the comment

```

However, this loop would be better implemented using another repeat statement [while](/en/book/basis/statements/statements_while). As a rule of thumb, a for loop should only be used when there is an obvious loop variable and/or a predetermined number of iterations. In this case, these conditions are not met.

Loop variables are usually integers, although other types are allowed, such as double. This is due to the fact that the very logic of the loop operation implies the numbering of iterations. In addition, it is always possible to calculate the necessary real numbers from an integer index, and with greater accuracy. For example, the following loop iterates over values from 0.0 to 1.0 in increments of 0.01:

```
for(double x = 0.0; x < 1.0; x += 0.01) { ... }

```

It can be replaced by a similar loop with an integer variable:

```
for(int i = 0; i < 100; ++i) { double x = i * 0.01; ... }

```

In the first case, when adding x += 0.01, the error of floating-point calculations gradually accumulates. In the second case, each value x is obtained in one operation i * 0.01, with the maximum available precision.

It is customary to give loop variables the following single-letter names, for example, i, j, k, m, p, q. Multiple names are required when loops are nested or both forward (increasing) and backward (decreasing) indexes are calculated within the same loop.

By the way, here is an example of a nested loop. The following code calculates and stores the multiplication table in a two-dimensional array.

```
int table[10][10] = {0};
for(int i = 1; i <= 10; ++i)
{
   for(int j = 1; j <= 10; ++j)
   {
      table[i - 1][j - 1] = i * j;
   }
}
ArrayPrint(table);

```
