# Function overloading

MQL5 allows the definition of functions with the same name but with different numbers or types of parameters in the same source code. This approach is called function overloading. It is usually applied when the same action can be triggered by different inputs. Differences in signatures allow the compiler to automatically determine which function to call based on the arguments passed. But there are some specifics.

Functions cannot differ only in their return type. In this case. the overload mechanism is not triggered and the "function already defined and has different type" error is returned.

If functions of the same name have different numbers of parameters and the "extra" parameters are declared optional, then the compiler will not be able to determine which one to call. This will generate the error "ambiguous call to overloaded function with the same parameters".

When an overloaded function is called, the compiler matches the arguments and parameters in the available overloads. If no exact match is found, the compiler tries to add/remove the const modifier and to perform numeric type expansion and [arithmetic conversion](/en/book/basis/conversion/conversion_arithmetic). In the case of [object pointers](/en/book/oop/classes_and_interfaces/classes_pointers), class inheritance rules are used.

With a different number of parameters or unrelated parameter types in the same position (such as a number and a string), the choice is usually clear. However, if the parameter types are to be implicitly converted from one to another, ambiguity may arise.

For example, we have two summation functions:

```
double sum(double v1, double v2)
{
   return v1 + v2;
}
 
int sum(int v1, int v2)
{
   return v1 + v2;
}

```

Then the following call will result in an error:

```
sum(1, 3.14); // overloaded function call is ambiguous

```

Here, the compiler is equally uncomfortable with each of the overloads: for the function double sum(double v1, double v2) it is necessary to implicitly convert the first argument to double, and for int sum(int v1, int v2) the second argument in int needs to be converted.

The term 'overload' should be interpreted in the sense that a reused name is "loaded" with "duties" several times heavier than a regular name used only for one function.

Let's try to overload the function for matrix transposition. We already had an example for a 2x2 array (see [Value parameters and reference parameters](/en/book/basis/functions/functions_ref_value)). Let's implement the same operation for a 3x3 array. The size of a multidimensional array parameter in higher dimensions (non-zero) changes the type, i.e. double [][2] is different from double [][3]. Thus, we will overload the old version of the function:

```
void Transpose(double &m[][2]);

```

by adding a new one (FuncOverload.mq5):

```
void Transpose(double &m[][3]);

```

In the implementation of the new version, it is convenient to use the helper function Swap to exchange two matrix elements at given indices.

```
void Transpose(double &m[][3])
{
   Swap(m, 0, 1);
   Swap(m, 0, 2);
   Swap(m, 1, 2);
}
 
void Swap(double &m[][3], const int i, const int j)
{
   static double temp;
   
   temp = m[i][j];
   m[i][j] = m[j][i];
   m[j][i] = temp;
}

```

Now we can call both functions from OnStart using the same notation for arrays of different sizes. The compiler itself will generate a call to the correct versions.

```
double a[2][2] = {{1, 2}, {3, 4}};
Transpose(a);
...
double b[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
Transpose(b);

```

It is important to note that the const modifier on the parameter, although it changes the prototype of the function, is not always a sufficient difference for overloading. Two functions of the same name, which differ only in the presence and absence of const for some parameter, can be considered the same. This will result in a "function already defined and has body" error. This behavior occurs because, for value parameters, the const modifier is discarded when the argument is assigned (because a value parameter, by definition, cannot change the argument in the calling code), and this does not allow one of several overlapped functions to be selected based on it.

To demonstrate this, it is enough to add a function in the script:

```
void Swap(double &m[][3], int i, int j);

```

It is an unsuccessful overload for the existing one:

```
void Swap(double &m[][3], const int i, const int j);

```

The only difference between the two functions is the const modifiers for the i and j parameters. Therefore, they are both suitable for calling with arguments of type int and passing by value.

When parameters are passed by reference, overloading with a difference of only const/non-const attributes succeeds because, for references, the const modifier is important (it changes the type and eliminates the possibility of implicit conversion). This is demonstrated in the script with a couple of functions:

```
void SwapByReference(double &m[][3], int &i, int &j)
{
   Print(__FUNCSIG__);
}
 
void SwapByReference(double &m[][3], const int &i, const int &j)
{
   Print(__FUNCSIG__);
}
 
void OnStart()
{
   // ...
   {
      int i = 0, j = 1;
      SwapByReference(b, i, j);
   }
   {
      const int i = 0, j = 1;
      SwapByReference(b, i, j);
   }
}

```

They are left as almost empty stubs, in which the signature of each function is printed using the Print(__FUNCSI__)call. This makes it possible to ensure that the appropriate version of the function is called depending on the const attribute of the arguments.
