# Type complex

The built-in type complex is a structure with two fields of type [double](/en/book/basis/builtin_types/float_numbers):

```
struct complex 
{ 
   double      real;   // real part 
   double      imag;   // imaginary part 
};

```

This structure is described in the type conversion section because it "converts" two double numbers into a new entity, in something similar to how [structures are turned into byte arrays, and vice versa](/en/book/common/conversions/conversions_structs). Moreover, it would be rather difficult to introduce this type without describing the structures first.

The complex structure does not have a constructor, so complex numbers must be created using an initialization list.

```
complex c = {re, im};

```

For complex numbers, only simple arithmetic and comparison operations are currently available: =, +, -, *, /, +=, -=, *=, /=, ==, !=. Support for [mathematical functions](/en/book/common/maths) will be added later.

Attention! Complex variables cannot be declared as inputs (using the keyword input) for an MQL program.

The suffix 'i' is used to describe complex (imaginary parts) constants, for example:

```
const complex x = 1 - 2i;
const complex y = 0.5i;

```

In the following example (script Complex.mq5) a complex number is created and squared.

```
input double r = 1;
input double i = 2;
   
complex c = {r, i};
   
complex mirror(const complex z)
{
   complex result = {z.imag, z.real}; // swap real and imaginary parts
   return result;
}
   
complex square(const complex z) 
{ 
   return (z * z);
}   
   
void OnStart()
{
   Print(c);
   Print(square(c));
   Print(square(mirror(c)));
}

```

With default parameters, the script will output the following:

```
c=(1,2) / ok
square(c)=(-3,4) / ok
square(mirror(c))=(3,4) / ok

```

Here, the pairs of numbers in parentheses are the string representation of the complex number.

Type complex can be passed by value as a parameter of MQL functions (unlike ordinary structures, which are passed only by reference). For functions imported from [DLL](/en/book/advanced/libraries/libraries_dll), the type complex should only be passed by reference.
