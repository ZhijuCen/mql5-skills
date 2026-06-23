# Functions

A function is a named block with statements. Almost the entire application algorithm of the program is contained in functions. Outside of functions, only auxiliary operations are performed, such as creating and deleting global variables.

The execution of statements within a function occurs when we call that function. Some functions, the main ones, are called automatically by the terminal when various events occur. They are also referred to as the MQL program entry points or event handlers. In particular, we already know that when we run a script on a chart, the terminal calls its main function OnStart. In other types of programs, there are other functions called by the terminal, which we will discuss in detail in the [fifth](/en/book/applications) and [sixth](/en/book/automation) chapters covering the trading architecture of the MQL5 API.

In this chapter, we will learn how to define and declare a function, how to describe and pass parameters to it, and how to return the result of its work from the function.

We will also talk about function overloading, i.e., the ability to provide multiple functions with the same name, and how this can be useful.

Finally, we will get acquainted with a new type: a pointer to a function.
