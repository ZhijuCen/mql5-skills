# Context, scope, and Lifetime of variables

MQL5 belongs to programming languages that use braces to group statements into code blocks.

Recall that a program consists of blocks with statements, and one block must exist definitely. In the script samples from Part 1, we saw the OnStart function. The body of this function (the brace-enclosed text following the function name) is exactly such a necessary code block.

Inside each block, the local context is formed, i.e., a region that limits the visibility and lifetime of variables described inside it. So far we have only encountered examples where braces define the body of functions. However, they can also be used to form [compound operators](/en/book/basis/statements/statements_compound), in the syntax of [the description of classes](/en/book/oop/classes_and_interfaces/classes_definition) and [namespaces](/en/book/oop/classes_and_interfaces/classes_namespace_context). All these methods also define visibility regions and will be considered in the relevant sections. At this stage, we only consider one type of local blocks, namely those inside of functions.

Along local regions, every program also has one global context, i.e., a region with the definitions of variables, functions, and other entities made beyond other blocks.

On the simple script side, in which the MQL Wizard has created the only void function OnStart, then there will only be 2 regions in it: A global one and a local one (inside the OnStart function body, although it is empty). The script below illustrates this with comments.

```
// GLOBAL SCOPE
void OnStart()
{
  // LOCAL SCOPE "OnStart"
}
// GLOBAL SCOPE

```

Please note that the global region stretches everywhere apart from function OnStart (both before and after it). Basically, it includes everything beyond any functions (if there were many), but there is nothing in this script, apart from OnStart.

We can describe variables, such as i, j, k, on the top of the file, and they will become global.

```
// GLOBAL SCOPE
int i, j, k;
void OnStart()
{
  // LOCAL SCOPE "OnStart"
}
// GLOBAL SCOPE

```

Global variables are created immediately upon starting an MQL program in the terminal and exist for the entire period of program execution.

The programmer can record and read the contents of global variables from any place in the program.

It is basically recommended to describe global variables just at the top, but it is necessary. If we move the declaration below the entire function OnStart, nothing will change basically. It will just be difficult for other programmers to immediately make sense of the code with variables, the definitions of which one has still to get to.

Interestingly, the OnStart function itself is declared in the global context, too. If we add another function, it will also be declared in the global context. Recall how we created the Greeting function in Part 1 and called it from the OnStart function. This is the effect of the function name and the method of referencing to it (how to execute it) being known throughout the source code. [Namespaces](/en/book/oop/classes_and_interfaces/classes_namespace_context) add some niceties to it; however, we will learn them later.

A local region inside each function only belongs to it: One local region is inside OnStart, and another is inside Greeting, which is its own and differs from both the local region of OnStart and the global one.

Variables described in the function body are called local. They are created according to their descriptions as of calling the relevant function during the program execution. Local variables can be only used inside the block that contains them. They are not visible or accessible from the outside. When leaving the function, local variables are destroyed.

Example of describing local variables x, y, z inside function OnStart:

```
// GLOBAL SCOPE
int i, j, k;
void OnStart()
{
  // LOCAL SCOPE "OnStart"
  int x, y, z;
}
// GLOBAL SCOPE

```

It should be noted that pairs of braces can be used in both describing the function and other statements and as themselves to form the internal code block. Unit nesting is unlimited.

Nested blocks are usually added to minimize the scope of variables used in a logically isolated small code location (if it is not set by a function for one reason or another). This allows the reduction of the probability of a false modification of the variable where it was not provided for or some undesired side effects due to the attempt to re-purpose the same variable for various needs (it is not a good practice).

Below is a sample function where unit nesting level is 2 (if we consider the block with the function body to be the first level), and 2 such blocks are created and will be executed consecutively.

```
void OnStart()
{
  // LOCAL SCOPE "OnStart"
  int x, y, z;
  
  { 
    // LOCAL SUBSCOPE 1
    int p;
    // ... use p for task 1
  }
  
  { 
    // LOCAL SUBSCOPE 2
    // y = p; // error: 'p' - undeclared identifier
    int p;    // from now 'p' is declared
    // ... use p for task 2
  }
  
  // p = x; // error: 'p' - undeclared identifier
}

```

Inside both blocks, variable p is described, which is used for various purposes in them. In fact, these are two different variables, although having the same name visible inside each block.

If the variable were taken out to the initial list of the local variables of the function, it could contain some remaining value upon exiting from the first block, thus breaking the operation of the second block. Moreover, the programmer could occasionally involve p in something else at the very beginning of the function, and then the side effects could take place in the first block.

Beyond either of the two nested blocks, variable p is unknown and therefore, an attempt to refer to it from the common block of the function leads to a compilation error ("undeclared identifier").

It should also be noted that a variable can be described not at the very beginning of the block, but in its middle or even closer to the end. Then it is defined not throughout the block, but only below its definition. Therefore, when referring to the variable above its description, the same error will occur.

Thus, the variable scope region may differ from the context (the entire block).

Both versions of the problem are illustrated in an example: Try to include any of the strings with statements p = x and y = p and compile the source code.

Memory is allocated for all the local variables of the function as soon as the control is passed inside the function. However, this is not the end of their creation. Then they are initialized (initial values are set), initialization being defined explicitly by the programmer or implicitly by the default values of the compiler. At the same time, context is of the essence, in which the variables are described.
