# Function templates

A function template consists of a header with template parameters (the syntax was described [earlier](/en/book/oop/templates/templates_header)) and a function definition in which the template parameters denote arbitrary types.

As a first example, consider the function Swap for swapping two array elements (TemplatesSorting.mq5). The template parameter T is used as the type of the input array variable, as well as the type of the local variable temp.

```
template<typename T>
void Swap(T &array[], const int i, const int j)
{
   const T temp = array[i];
   array[i] = array[j];
   array[j] = temp;
}

```

All statements and expressions in the body of the function must be applicable to real types, for which the template will then be instantiated. In this case, the assignment operator '=' is used. While it always exists for built-in types, it may need to be explicitly overloaded for user-defined types.

The compiler generates the implementation of the copy operator for classes and structures by default, but it can be removed implicitly or explicitly (see keyword [delete](/en/book/oop/classes_and_interfaces/classes_final_delete)). In particular, as we saw in the section [Object Type Casting](/en/book/oop/classes_and_interfaces/classes_dynamic_cast_void), having a constant field in a class causes the compiler to remove its implicit copy option. Then the above template function Swap cannot be used for objects of this class: the compiler will generate an error.

For classes/structures that the Swap function works with, it is desirable to have not only an assignment operator but also a copy constructor, because the declaration of the variable temp is actually a construction with an initialization, not an assignment. With a copy constructor, the first line of the function is executed in one go (temp is created based on array[i]), while without it, the default constructor will be called first, and then for temp the operator '=' will be executed.

Let's see how the template function Swap can be used in the quicksort algorithm: another template function QuickSort implements it.

```
template<typename T>
void QuickSort(T &array[], const int start = 0, int end = INT_MAX)
{
   if(end == INT_MAX)
   {
      end = start + ArraySize(array) - 1;
   }
   if(start < end)
   {
      int pivot = start;
      
      for(int i = start; i <= end; i++)
      {
         if(!(array[i] > array[end]))
         {
            Swap(array, i, pivot++);
         }
      }
      
      --pivot;
   
      QuickSort(array, start, pivot - 1);
      QuickSort(array, pivot + 1, end);
   }
}

```

Note that the T parameter of the QuickSort template specifies the type of the input parameter array, and this array is then passed to the Swap template. Thus, type inference T for the QuickSort template will automatically determine the type T for the Swap template.

The built-in function ArraySize (like many others) is able to work with arrays of arbitrary types: in a sense, it is also a template, although it is implemented directly in the terminal.

Sorting is done thanks to the '>' comparison operator in the if statement. As we noted earlier, this operator must be defined for any type T that is being sorted, because it applies to the elements of an array of type T.

Let's check how sorting works for arrays of built-in types.

```
void OnStart()
{
   double numbers[] = {34, 11, -7, 49, 15, -100, 11};
   QuickSort(numbers);
   ArrayPrint(numbers);
   // -100.00000 -7.00000 11.00000 11.00000 15.00000 34.00000 49.00000
   
   string messages[] = {"usd", "eur", "jpy", "gbp", "chf", "cad", "aud", "nzd"};
   QuickSort(messages);
   ArrayPrint(messages);
   // "aud" "cad" "chf" "eur" "gbp" "jpy" "nzd" "usd"
}

```

Two calls to the template function QuickSort automatically infer the type of T based on the types of the passed arrays. As a result, we will get two instances of QuickSort for types double and string.

To check the sorting of a custom type, let's create an ABC structure with an integer field x, and fill it with random numbers in the constructor. It is also important to overload the operator '>' in the structure.

```
struct ABC
{
   int x;
   ABC()
   {
      x = rand();
   }
   bool operator>(const ABC &other) const
   {
      return x > other.x;
   }
};
void OnStart()
{
   ...
   ABC abc[10];
   QuickSort(abc);
   ArrayPrint(abc);
  /* Sample output:
            [x]
      [0]  1210
      [1]  2458
      [2] 10816
      [3] 13148
      [4] 15393
      [5] 20788
      [6] 24225
      [7] 29919
      [8] 32309
      [9] 32589
   */
}

```

Since the structure values are randomly generated, we will get different results, but they will always be sorted in ascending order.

In this case, the type T is also automatically inferred. However, in some cases, explicit specification is the only way to pass a type to a function template. So, if a template function must return a value of a unique type (different from the types of its parameters) or if there are no parameters, then it can only be specified explicitly.

For example, the following template function createInstance requires the type to be explicitly specified in the calling instruction, since it is not possible to automatically "calculate" the type T from the return value. If this is not done, the compiler generates a "template mismatch" error.

```
class Base
{
   ...
};
   
template<typename T>
T *createInstance()
{
   T *object = new T(); //calling the constructor
   ...                  //object setting
   return object; 
}
   
void OnStart()
{
   Base *p1 = createInstance();       // error: template mismatch
   Base *p2 = createInstance<Base>(); // ok, explicit directive
   ...
}

```

If there are several template parameters, and the type of the return value is not bound to any of the input parameters of the function, then you also need to specify a specific type when calling:

```
template<typename T,typename U>
T MyCast(const U u)
{
   return (T)u;
}
   
void OnStart()
{
   double d = MyCast<double,string>("123.0");
   string f = MyCast<string,double>(123.0);
}

```

Note that if the types for the template are explicitly specified, then this is required for all parameters, even though the second parameter U could be inferred from the passed argument.

After the compiler has generated all instances of the template function, they participate in the standard procedure for choosing the best candidate from all [function overloads](/en/book/basis/functions/functions_overloading) with the same name and the appropriate number of parameters. Of all the overload options (including the created template instances), the closest one in terms of types (with the least number of conversions) is selected.

If a template function has some input parameters of specific types, then it is considered a candidate only if these types completely match the arguments: any need for conversion will cause the template to be "discarded" as unsuitable.

Non-template overloads take precedence over template overloads, more specialized ("narrowly focused") "win" from template overloads.

If the template argument (type) is specified explicitly, then the rules for [implicit type casting](/en/book/basis/conversion/conversion_implicit) are applied for the corresponding function argument (passed value), if necessary, if these types differ.

If several variants of a function match equally, we will get an "ambiguous call to an overloaded function with the same parameters" error.

For example, if in addition to the template MyCast, a function is defined to convert a string to a boolean type:

```
bool MyCast(const string u)
{
   return u == "true";
}

```

then calling MyCast<double,string>("123.0") will start throwing the indicated error, because the two functions differ only in the return value:

```
'MyCast<double,string>' - ambiguous call to overloaded function with the same parameters
could be one of 2 function(s)
   double MyCast<double,string>(const string)
   bool MyCast(const string)

```

When describing template functions, it is recommended to include all template parameters in the function parameters. Types can only be inferred from arguments, not from the return value.

If a function has a templated type parameter T with a default value, and the corresponding argument is omitted when called, then the compiler will also fail to infer the type of T and throw a "cannot apply template" error.

```
class Base
{
public:
   Base(const Base *source = NULL) { }
   static Base *type;
};
   
static Base* Base::type;
   
template<typename T>
T *createInstanceFrom(T *origin = NULL)
{
   T *object = new T(origin);
   return object; 
}
   
void OnStart()
{
   Base *p1 = createInstanceFrom();   // error: cannot to apply template
   Base *p2 = createInstanceFrom(Base::type); // ok, auto-detect from argument
   Base *p3 = createInstanceFrom<Base>();     // ok, explicit directive, an argument is omitted
}

```
