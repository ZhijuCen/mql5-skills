# Other operations

## Indexing ( [] )

When addressing the i-th element of the array, the expression value is the value of a variable with the serial number i.

Example:

```
array[i] = 3; // Assign the value of 3 to i-th element of the array.

```

Only an integer can be index of an array. Four-dimensional and below arrays are allowed. Each dimension is indexed from 0 to dimension size-1. In particular case, for a one-dimensional array consisting of 50 elements, the reference to the first element will look like array [0], that to the last element will be array [49].

When addressing beyond the array, the executing subsystem will generate a critical error, and the program will be stopped.

## Calling Function with x1, x2 ,..., xn Arguments

Each argument can represent a constant, variable, or expression of the corresponding type. The arguments passed are separated by commas and must be inside of parentheses, the opening parenthesis must follow the name of the called function.

The expression value is the value returned by the function. If the return value is of void type, such function call cannot be placed to the right in the assignment operation. Note that the expressions x1,..., xn are executed exactly in this order.

Example:

```
   int length=1000000;   
   string a="a",b="b",c;
//---Other Operations
   int start=GetTickCount(),stop;
   long i;
   for(i=0;i<length;i++)
     {
      c=a+b;
     }
   stop=GetTickCount();
   Print("time for 'c = a + b' = ",(stop-start)," milliseconds, i = ",i);

```

## Comma Operation ( , )

Expressions separated by commas are executed from left to right. All side effects of the left expression calculation can appear before the right expression is calculated. The result type and value coincide with those of the right expression. The list of parameters to be passed (see above) can be considered as an example.

Example:

```
for(i=0,j=99; i<100; i++,j--) Print(array[i][j]);

```

## Dot Operator ( . )  #

For the direct [access to the public members](/en/docs/basis/types/classes#dot_operation) of structures and classes the dot operation is used. Syntax:

```
Variable_name_of_structure_type.Member_name

```

Example:

```
   struct SessionTime
     {
      string sessionName;
      int    startHour;
      int    startMinutes;
      int    endHour;
      int    endMinutes;
     } st;
   st.sessionName="Asian";
   st.startHour=0;
   st.startMinutes=0;
   st.endHour=9;
   st.endMinutes=0;

```

## Scope Resolution Operation ( :: )  #

Each function in a mql5 program has its own execution scope. For example, the [Print()](/en/docs/common/print) system function is performed in a global scope. [Imported](/en/docs/basis/preprosessor/import) functions are called in the scope of the corresponding import. Method functions of [classes](/en/docs/basis/types/classes#class) have the scope of the corresponding class. The syntax of the scope resolution operation is as follows:

```
[Scope_name]::Function_name(parameters)

```

If there is no scope name, this is the explicit direction to use the global scope. If there is no scope resolution operation, the function is sought in the nearest scope. If there is no function in the local scope, the search is conducted in the global scope.

The scope resolution operation is also used to [define function](/en/docs/basis/function#function_definition)-class member.

```
type Class_name::Function_name(parameters_description)
   {
// function body
   }

```

Use of several functions of the same name from different execution contexts in a program may cause ambiguity. The priority order of function calls without explicit scope specification is the following:

1. Class methods. If no function with the specified name is set in the class, move to the next level.
2. MQL5 functions. If the language does not have such a function, move to the next level.
3. User defined global functions. If no function with the specified name is found, move to the next level.
4. Imported functions. If no function with the specified name is found, the compiler returns an error.

To avoid the ambiguity of function calls, always explicitly specify the function scope using the scope resolution operation.

Example:

```
#property script_show_inputs
#import "kernel32.dll"
   int GetLastError(void);
#import
 
class CCheckContext
  {
   int         m_id;
public:
               CCheckContext() { m_id=1234; }
protected:
   int         GetLastError() { return(m_id); }
  };
class CCheckContext2 : public CCheckContext
  {
   int         m_id2;
public:
               CCheckContext2() { m_id2=5678; }
   void        Print();
protected:
   int         GetLastError() { return(m_id2); }
  };
void CCheckContext2::Print()
  {
   ::Print("Terminal GetLastError",::GetLastError());
   ::Print("kernel32 GetLastError",kernel32::GetLastError());
   ::Print("parent GetLastError",CCheckContext::GetLastError());
   ::Print("our GetLastError",GetLastError());
  }  
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   CCheckContext2 test;
   test.Print();
  }
//+------------------------------------------------------------------+

```

## Operation of Obtaining Data Type Size or Size of Any Data Type Object ( sizeof )  #

Using the sizeof operation, the memory size corresponding to an identifier or type can be defined. The sizeof operation is of the following format:

Example:

```
sizeof(expression)

```

Any identifier, or type name enclosed in brackets can be used as an expression. Note that the void type name can't be used, and the identifier cannot belong to the field of bits, or be a function name.

If the expression is the name of a static array (i.e. the first dimension is given), then the result is the size of the whole array (i.e. the product of the number of elements and the length of the type). If the expression is the name of a dynamic array (the first dimension is not specified), the result will be the size of the object of the [dynamic array](/en/docs/basis/types/dynamic_array).

When sizeof is applied to the name of structure or class type, or to the identifier of the structure or class type, the result is the actual size of the structure or class.

Example:

```
   struct myStruct
     {
      char   h;
      int    b;
      double f;
     } str;
   Print("sizeof(str) = ",sizeof(str));
   Print("sizeof(myStruct) = ",sizeof(myStruct));   

```

The size is calculated at the compilation stage.

See also

[Precedence Rules](/en/docs/basis/operations/rules)
