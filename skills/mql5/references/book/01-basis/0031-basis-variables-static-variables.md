# Static variables

It is sometimes necessary to describe a variable inside a function, ensuring its existence for the entire duration of the program execution. For example, we want to count how many times this function has been called.

Such a variable cannot be local, because then it will lose its "long memory," since it will be created every time at calling the function and removed at exiting it. Technically, it could be described globally; however, if the variable is only used in this function, this approach is wrong in terms of program design.

First, a global variable can accidentally be changed from any place in the program.

Second, imagine what "zoo" of variables would be made in the global region of the program if we declare a global variable at the slightest pretext. Instead, it is recommended to declare variables in the smallest block (if there are several nested ones), in which they are used.

Therefore, the counter of function executions should be described inside the function. This is where the new attribute of variables helps, their static nature.

A special keyword (modifier), static, placed before the variable type in its declaration allows prolonging its lifetime up to the entire duration of program execution, that is, makes it similar to global ones. As a rule, a static variable is only defined locally, in one of the functions. Therefore, its visibility is limited by the relevant code block, as in a normal local variable.

Static variables can also be described at a global level, but do not differ from the normal global ones in any way (at least, as of writing this book). It varies from their behavior in C++: There, their visibility is limited by the file they are described in. In MQL5, a program is assembled based on one main mq5 file and, perhaps, some header files (see [directive ](/en/book/basis/preprocessor/preprocessor_include)[#include](/en/book/basis/preprocessor/preprocessor_include)); therefore, both static and normal global variables are available from all source files of the program.

A local static variable is created only once — at the moment when the program first steps into the function where this variable is described. Such a variable will only be removed at unloading the program. If a function has never been called, the local static variables described in it, if any, will never be created.

As an example, let's modify the Greeting function from Part 1 so that it gives different greetings at each call. Let's name the new script GoodTimes.mq5.

We will remove the input of the script GreetingHour and the parameter of the Greeting function. Inside the Greeting function, we will describe a new static variable, counter, of integer type, with the initial value of 0. It should be reminded that it is exactly initialization, and it will be executed only once because the variable is static.

```
string Greeting() 
{
  static int counter = 0;
  static string messages[3] =
  {
    "Good morning", "Good day", "Good evening"
  };
  return messages[counter++ % 3];
}

```

Since we know modifier static now, it is reasonable to also use it for array messages. The matter is that it was declared as local before, and it would be re-created every time at multiple calls of function Greeting (and removed at exit). This is not efficient.

It should be reminded that an array is a named set of several values of the same type, available by index specified in square brackets after the name. Much of what has been said about variables applies directly to arrays. Further nuances of working with arrays will be covered in section [Arrays](/en/book/basis/arrays).

But let's get back to our current problem. An option is chosen from the array based on the value of the counter variable in the return statement and so far appears quite cabbalistically:

```
  return messages[counter++ % 3];

```

We have already mentioned casually the modulus operation performed using character '%' in Part 1. With it, we guarantee that the element index will not be able to exceed the array size: Whatever be counter, its division modulo by 3 will either be 0 or 1, or 2.

The same applies to structure counter++, it means adding 1 to the variable value (single increment).

It is important to note that, in this notation, incrementation will take place upon having computed the entire expression, in this case, upon division counter % 3. This means that counting will start from zero, i.e., initial value. There is a possibility to make an increment before computing the expression, having written: ++counter % 3. Then counting would start from 1. We will consider the operations of this type in section [Increment and Decrement](/en/book/basis/expressions/increment_decrement).

Let's call the Greeting function from OnStart 3 consecutive times.

```
void OnStart()
{
  Print(Greeting(), ", ", Symbol());
  Print(Greeting(), ", ", Symbol());
  Print(Greeting(), ", ", Symbol());
  // Print(counter); // error: 'counter' - undeclared identifier
}

```

As a result, we will see the anticipated three strings with all greetings one after another in the log.

```
GoodTimes (EURUSD,H1)        Good morning, EURUSD
GoodTimes (EURUSD,H1)        Good afternoon, EURUSD
GoodTimes (EURUSD,H1)        Good evening, EURUSD

```

If we continue calling the function, the counter will increase, and the messages will rotate.

An attempt to refer to the counter variable at the end of OnStart (commented) will not allow the code to be compiled, since the static variable, although it continues to exist, is only available inside function Greeting.

Please note that braces are used for both forming the code blocks and initializing arrays. You should distinguish among their applications. Arrays will be considered in detail in the relevant section. However, these are not all applications of braces: Using them, we will later learn how to define custom types, structures, and classes. Static variables can also be defined inside structures and classes.
