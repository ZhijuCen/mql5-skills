# Functions

Every task can be divided into subtasks, each of which can either be directly represented in the form of a code, or divided into smaller sub-tasks. This method is called stepwise refinement. Functions are used for writing the code of sub-tasks to be solved. The code that describes what a function does is called function definition:

```
function_header
  {
   instructions
  }

```

All that is before the first brace is the header of the function definition, and what is between braces is the body of the function definition. The function header includes a description of the return value type, name ([identifier](/en/docs/basis/syntax/identifiers)) and [formal parameters](/en/docs/basis/variables/formal).  The number of parameters passed to the function is limited and cannot exceed 64.

The function can be called from other parts of the program as many times as necessary. In fact, the return type, function identifier and parameter types constitute the function prototype.

Function prototype is the function declaration, but not its definition. Due to the explicit declaration of the return type and a list of argument types, the strict type checking and implicit typecasting are possible during function calls. Very often function declarations are used in classes to improve the code readability.

The function definition must exactly match its declaration. Each declared function must be defined.

Example:

```
double                       // return value type
linfunc (double a, double b) // function name and parameter list
  {
                             // composite operator
   return (a + b);           // return value
  }

```

The [return](/en/docs/basis/operators/return) operator can return the value of an expression located in this operator. If necessary, the expression value is converted to the function result type. What can be returned: [simple types](/en/docs/basis/types#base_types), [simple structures](/en/docs/basis/types/classes#simple_structure), [object pointers](/en/docs/basis/types/object_pointers). With the return operator you can't return any arrays, class objects, variables of compound structure type.

A function that returns no value should be described as that of [void](/en/docs/basis/types/void) type.

Example:

```
void errmesg(string s)
  {
   Print("error: "+s);
  }

```

Parameters passed to the function can have default values, which are defined by constants of that type.

Example:

```
int somefunc(double a,
             double d=0.0001,
             int n=5,
             bool b=true,
             string s="passed string")
  {
   Print("Required parameter a = ",a);
   Print("Pass the following parameters: d = ",d," n = ",n," b = ",b," s = ",s);
   return(0);
  }

```

If any of parameters has a default value, all subsequent parameters must also have default values.

Example of incorrect declaration:

```
int somefunc(double a,
             double d=0.0001,    // default value 0.0001 declared
             int n,              // default value is not specified !
             bool b,             // default value is not specified !
             string s="passed string")
  {                                          
  }           

```

See also

[Overload](/en/docs/basis/oop/overload), [Virtual Functions](/en/docs/basis/oop/virtual), [Polymorphism](/en/docs/basis/oop/polymorphism)
