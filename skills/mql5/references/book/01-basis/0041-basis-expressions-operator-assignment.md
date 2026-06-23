# Assignment operation

Expression calculation results must usually be stored somewhere. The assignment operator denoted by '=' is intended for this purpose in the language. The name of a variable or an array element is placed to the left of it, in which the result must be stored, while the expression (in fact, the formula for computation) is to the right.

We have already used this operator for the initialization of variables, which is executed only once, during creating them. However, assignment allows changing the values of variables in the course of the algorithm for an arbitrary number of times. For example:

```
int z;
int x = 1, y = 2;
z = x;
x = y;
y = z;

```

Variables x and y were initialized by values 1 and 2, whereupon the auxiliary third variable z and three assignments were used to exchange values x and y.

The assignment operator, like all operators, returns its result into the expression. This enables writing the assignments in a sequence.

```
int x, y, z;
x = y = z = 1;

```

Here, 1 will first be assigned to variable z, then to variable y, and finally to variable x. Obviously, this operator is right-associative, because the value being assigned drifts from right to left in the expression.

We can use the assignment as a part of an expression. But, since its priority is lower than those of all other operators (except for the "comma" one, see [Priorities of Operations](/en/book/basis/expressions/operators_precedence)), it must be enclosed in parentheses (for more details, please see the section on [Grouping with parentheses](/en/book/basis/expressions/operators_parentheses)). This aspect enables situations where mistypes, such as '=' instead of '==', in expressions lead to not executing the statements as intended. See the example of such behavior in the section dealing with [statement ](/en/book/basis/statements/statements_if)[if](/en/book/basis/statements/statements_if).

The assignment operator imposes certain limitations on what can be to the left of '=' and what to the right of it. In programming, these entities aiming to simplify storing are entitled precisely: LValue and RValue (based on Left and Right).

LValue and RValue  

   

 LValue represents an entity, for which memory is allocated and, therefore, a value can be written in it. Variable and array elements are the known examples of LValue. Upon having studied OOP, we will get to know another representative of this category: Object, in which the assignment operator can be reloaded. A mandatory element of LValue is the presence of an identifier.  

   

It should be considered that variables and arrays may be described with the keyword const, and then they cannot act as LValue, because the modification of constants is prohibited.  

   

RValue is a temporary value used in an expression, such as a literal or value returned due to a function call or due to computing a fragment of the expression.  

   

Category LValue is of expansive nature, i.e., falling within it allows placing the relevant object to the left of '=' but does not prohibit using it, on par with RValue, to the right of '='.  

   

Category RValue, over again, is of a limiting nature, i.e., any RValue may only be to the right of '='.  

   

As a certain LValue element is used to the right of '=', its identifier, in fact, denotes its current contents placed into the expression formula.  

   

However, if an element of LValue is used to the left of '=', its identifier indicates a memory address (cell) where the new value (expression computation result) should be written.  

   

Different operators have different limitations regarding whether they can be used for the operands of LValue or RValue. For example, increment '++' and decrement '--' operators (see [Increment and Decrement](/en/book/basis/expressions/increment_decrement)) may only be used with LValue.

Here are some examples of what is and is not allowed to do with assignment operators (script ExprAssign.mq5):

```
// description of variables
const double cx = 123.0;
int x, y, a[5] = {1};
string s;
// assignment
a[2] = 21;       // ok
x = a[0] + a[1] + a[2]; // ok
s = Symbol();    // ok
cx = 0;          // const variable may not be changed
                 // error: 'cx' - constant cannot be modified
5 = y;           // 5 – this number (literal)
                 // error: '5' - l-value required
x + y = 3;       // to the left of RValue (expression computation result)
                 // error: l-value required
Symbol() = "GBPUSD"; // to the left of RValue with the function call result  
                     // error: l-value required

```

The compiler returns an error of breaking the operator use rules.
