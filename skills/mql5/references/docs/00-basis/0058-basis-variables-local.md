# Local Variables

A variable declared inside a [function](/en/docs/basis/function) is local. The scope of a local variable is limited to the function range inside which it is declared. Local variable can be [initialized](/en/docs/basis/variables/initialization) by outcome of any [expression](/en/docs/basis/operators/expression). Every call of the function initializes a local variable. Local variables are stored in memory area of the corresponding function.

Example:

```
int somefunc()
  {
   int ret_code=0;
   ...
   return(ret_code);
  }

```

[Scope](/en/docs/basis/variables/variable_scope) of a variable is a program part, in which a variable can be referred to. Variables declared inside a block (at the internal level), have the [block](/en/docs/basis/operators/compound) as their scope. The block scope start with the variable declaration and ends with the final right brace.

Local variables declared in the beginning of a function also have the scope of block, as well as [function parameters](/en/docs/basis/function/call#argument) that are local variables. Any block can contain variable declarations. If blocks are nested and the [identifier](/en/docs/basis/syntax/identifiers) in the external block has the same name as the identifier in the internal block, the external block identifier is hidden, until the operation of the internal block is over.

Example:

```
void OnStart()
  {
//---
   int i=5;      // local variable of the function
     {
      int i=10;  // function variable
      Print("Inside block i = ",i); // result is  i=10;
     }
   Print("Outside block i = ",i);  // result is  i=5;
  }

```

This means that while the internal block is running, it sees values of its own local identifiers, not the values of identifiers with identical names in the external block.

Example:

```
void OnStart()
  {
//---
   int i=5;      // local variable of the function
   for(int i=0;i<3;i++)
      Print("Inside for i = ",i);
   Print("Outside the block i = ",i);
  }
/* Execution result
Inside for i = 0
Inside for i = 1
Inside for i = 2
Outside block i = 5
*/

```

Local variables declared as [static](/en/docs/basis/variables/static) have the scope of the block, despite the fact that they exist since the program start.

## Stack  #

In every MQL5 program, a special memory area called stack is allocated for storing local function variables that are created automatically. One stack is allocated for all functions, its default size for indicators is equal to 1Mb. In Expert Advisors and scripts, stack size can be managed using the [#property stacksize](/en/docs/basis/preprosessor/compilation) compiler directive (which sets the stack size in bytes), a memory of 8Mb is allocated by default for the stack.

[Static](/en/docs/basis/variables/static) local variables are stored in the same place where other static and [global](/en/docs/basis/variables/global) variables are stored - in a special memory area, which exists separately from the stack. [Dynamically](/en/docs/basis/variables/object_live) created variables also use a memory area separate from the stack.

With each function call, a place on the stack is allocated for internal non-static variables. After exiting the function, the memory is available for use again.

If from the first function the second one is called, then the second function occupies the required size from the remaining stack memory for its variables. Thus, when using included functions, stack memory will be sequentially occupied for each function. This may lead to a shortage of memory during one of the function calls, such a situation is called stack overflow.

Therefore, for large local data you should better use dynamic memory - when entering a function, allocate the memory, which is required for local needs, in the system ([new](/en/docs/basis/operators/newoperator), [ArrayResize()](/en/docs/array/arrayresize)), and when exiting the function, release the memory ([delete](/en/docs/basis/operators/deleteoperator), [ArrayFree()](/en/docs/array/arrayfree)).

See also

[Data Types](/en/docs/basis/types), [Encapsulation and Extensibility of Types](/en/docs/basis/oop/incapsulation),[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
