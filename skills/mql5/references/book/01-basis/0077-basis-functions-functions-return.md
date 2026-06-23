# Return values

Functions can return the values of built-in types, [structures](/en/book/oop/structs_and_unions) with fields of built-in types, as well as [pointers to functions](/en/book/basis/functions/functions_typedef) and pointers to [class](/en/book/oop/classes_and_interfaces) objects. The type name is written in the function definition before the name. If the function does not return anything, it should be assigned the void type.

To return from an array function, you must use parameters passed by reference (see [Value parameters and reference parameters](/en/book/basis/functions/functions_ref_value)).

A value is returned using the [return](/en/book/basis/statements/statements_return) statement, in which an expression is specified after the return keyword. Any of the two forms may be used:

```
return expression ;

```

or:

```
return ( expression ) ;

```

If the function is of type void, then the return statement is simplified:

```
return ;

```

The return statement cannot contain any expression inside the void-function: the compiler will generate an error "'return' - 'void' function returns a value".

For such functions, theoretically, it is not necessary to use return at the end of the block with the function body. We saw this in the example of the OnStart function.

If the function has a type other than void, then the return statement must be mandatory. If it is not present, a compilation error "not all control paths return a value" will occur.

```
int func(void)
{
   if(IsStopped()) return; // error: function must return a value
                           // error: not all control paths return a value  
}

```

It is important to note that a function body can have multiple return statements. In particular, in case of early exits by condition. Any return statement breaks the execution of the function at the place where it is located.

If a function must return a value (because it is not of type void), and it is not specified in the return operator, the compiler will generate an error "function must return a value". The compiler-correct version of the func function is given below (FuncReturn.mq5).

```
int func(void)
{
   if(IsStopped()) return 0;
   return 1;
}

```

If the return value differs from the specified function type, the compiler will attempt an [implicit conversion](/en/book/basis/conversion/conversion_implicit). In case the types require explicit conversion, an error will be generated.

To return a value, a temporary variable is implicitly created and made available to the calling code.

After we learn about object types (see the chapter on [Classes](/en/book/oop/classes_and_interfaces)) and the ability to return pointers to objects from functions, we'll get back to considering how to pass them safely. Unlike C++, functions in MQL5 are not capable of returning references. Attempting to declare a function with an ampersand in the result type results in a "'&' - reference cannot used" error.
