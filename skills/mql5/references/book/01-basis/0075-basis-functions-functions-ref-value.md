# Value parameters and reference parameters

Arguments can be passed to a function in two ways: by value and by reference.

All the cases we've looked at so far are passing by value. This option means that the value of the argument prepared by the calling code snippet is copied into a new variable, the corresponding input variable of the function. Otherwise, the argument and input variable are unrelated. All subsequent manipulations with the variable inside the function do not affect the argument in any way.

To describe a reference parameter, add an ampersand sign '&' on the right of the type. Many programmers prefer to append an ampersand to a parameter name, thus emphasizing that the parameter is a reference to the given type. For example, the following entries are equivalent:

```
void func(int &parameter);
void func(int & parameter); 
void func(int& parameter);

```

When a function is called, a corresponding local variable is not created for a reference parameter. Instead, the argument specified for this parameter becomes available inside the function under the name (alias) of the input parameter. Thus, the value is not copied, but used at the same address in memory. Therefore, modifications to a parameter within a function are reflected in the state of its associated argument. An important feature follows from this.

You can only specify a variable (LValue, see [Assignment operator](/en/book/basis/expressions/operator_assignment)) as an argument for a reference parameter. Otherwise, we'll get the "parameter passed as reference, variable expected" error.

Passing by reference is used in several cases:

- to improve the efficiency of the program by eliminating the copying of the value;
- to pass modified data from a function to the calling code when returning a single value with return is not enough;

The first point is especially relevant for potentially large variables such as strings or arrays.

To distinguish between the first and second purposes of a reference parameter, the authors of the function are encouraged to add the const modifier when the parameter inside the function is not expected to change. This will remind you and make it clear to other developers that passing a variable inside a function will not lead to side effects.

Not applying the const modifier to reference parameters where possible can lead to problems throughout the entire function call hierarchy. The fact is that calling such functions will require non-constant arguments. Otherwise, the error "constant variable cannot be passed as reference" will occur. As a result, it may gradually turn out that all parameters in all functions should be stripped of the const modifier for the sake of the code compilability. In fact, this actually expands the scope for potential bugs with unintentional corruption of variables. The situation should be corrected in the opposite way: put const wherever return and modification of values are not required.

To compare the ways of passing parameters in the FuncDeclaration.mq5 script, several functions are implemented: FuncByValue – passing by value, FuncByReference – passing by reference,  FuncByConstReference – passing by constant reference.

```
void FuncByValue(int v)
{
   ++v;
   // we are doing something else with v
}
 
void FuncByReference(int &v)
{
   ++v;
}
 
void FuncByConstReference(const int &v)
{
   // error
   // ++v; // 'v' - constant cannot be modified
   Print(v); 
}

```

In the OnStart function, we call all these functions and observe their effect on i variable used as an argument. Note that passing a parameter by reference does not change the function call syntax.

```
void OnStart()
{
   int i = 0;
   FuncByValue(i);          // i cannot change
   Print(i);                // 0
   FuncByReference(i);      // i is changing
   Print(i);                // 1
   FuncByConstReference(i); // i cannot change, 1
   const int j = 1;
   // error
   // 'j' - constant variable cannot be passed as a reference
   // FuncByReference(j);
   
   FuncByValue(10);         // ok
   // error: '10' - parameter passed as reference, variable expected
   // FuncByReference(10);
}

```

The literal can only be passed to FuncByValue function, since other functions require a reference, i.e. a variable, as an argument.

Function FuncByReference cannot be called with the variable j, since the latter is declared as a constant, and this function declares the ability (or intention) to change its parameter since it is not equipped with the const modifier. This generates the "constant variable cannot be passed as reference" error.

The script also describes the Transpose function: it transposes a 2x2 matrix passed as a two-dimensional array by reference.

```
void Transpose(double &m[][2])
{
   double temp = m[1][0];
   m[1][0] = m[0][1];
   m[0][1] = temp;
}

```

Its call from OnStart demonstrates the expected change in the contents of the local array a.

```
double a[2][2] = {{-1, 2}, {3, 0}};
Transpose(a);
ArrayPrint(a);

```

In MQL5, array parameters are always passed as an internal structure of a dynamic array (see the [Characteristics of arrays](/en/book/basis/arrays/arrays_overview) section). As a consequence, the description of such a parameter must necessarily have an open size in the first dimension, that is, it is empty inside the first pair of square brackets.

This does not prevent, if necessary, passing to the function the actual argument, which is an array with a fixed size (as in our example). However, functions like [ArrayResize](/en/book/common/arrays/arrays_dynamic) will not be able to resize or otherwise reorganize such a masked fixed array.

The sizes of the array in all dimensions except the first must match for both, the parameter and argument. Otherwise, we will get a "parameter conversion not allowed" error. In particular, the TransposeVectorfunction is defined in the example:

```
void TransposeVector(double &v[])
{
}

```

An attempt to call it on a two-dimensional array a is commented out in OnStart because it generates the above error: array dimensions do not match.

In addition to passing parameters by value or by reference, there is another option: passing a pointer. Unlike C++, MQL5 only supports [pointers](/en/book/oop/classes_and_interfaces/classes_pointers) for object types ([classes](/en/book/oop/classes_and_interfaces)). We will look at this feature in the third Part.
