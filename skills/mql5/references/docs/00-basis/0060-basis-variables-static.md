# Static Variables

The storage class of static defines a static variable. The static modifier is indicated before the data type.

Example:

```
int somefunc()
  {
   static int flag=10;
   ...
   return(flag);
  }

```

A static variable can be [initialized](/en/docs/basis/variables/initialization) by a constant or constant expression corresponding to its type, unlike a simple local variable, which can be initialized by any expression.

Static variables exist from the moment of program execution and are initialized only once before the specialized functions [OnInit()](/en/docs/event_handlers/oninit) is called. If the initial values are not specified, variables of the static storage class are taking zero initial values.

[Local variables](/en/docs/basis/variables/local) declared with the static keyword retain their values throughout the function [lifetime](/en/docs/basis/variables/variable_scope). With each next function call, such local variables contain the values that they had during the previous call.

Any variables in a block, except [formal parameters](/en/docs/basis/variables/formal) of a function, can be defined as static. If a variable declared on a local level is not a static one, memory for such a variable is allocated automatically at a program stack.

Example:

```
int Counter()
  {
   static int count;
   count++;
   if(count%100==0) Print("Function Counter has been called ",count," times");
   return count;
  }
void OnStart()
  {
//---
   int c=345;
   for(int i=0;i<1000;i++)
     {
      int c=Counter();
     }
   Print("c =",c);
  }

```

See also

[Data Types](/en/docs/basis/types), [Encapsulation and Extensibility of Types](/en/docs/basis/oop/incapsulation), [Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live), [Static Class Members](/en/docs/basis/oop/staticmembers)
