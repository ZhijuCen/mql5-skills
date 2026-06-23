# Declaration and definition of variables

A variable is a named memory cell for storing the data of a specific type. For the program to be able to operate a variable, the programmer must declare and/or define it in the source code. In the general case, the terms declaration and definition mean different things regarding the program elements, while they practically always coincide for variables. These intricacies will be covered when we get to know about functions, classes, and special (external) variables. Here we are going to use both terms interchangeably, along with the 'description' as a generalizing one.

It would be safe to assume that a declaration contains a description of a program element with all its attributes necessary for being used in the program. Definition, however, contains the specific implementation of this element, corresponding with the declaration.

Declarations allow the compiler to interconnect all the elements of the program. Based on definitions, the compiler generates an executable code.

In the case of variables, their declaration practically always acts as their definition, since it ensures allocating memory and interpreting their contents in accordance with their types (this is exactly an implementation of a variable). The only exception is the declaration of variables with the word 'extern' (for more details, see section [External Variables](/en/book/basis/variables/variables_extern)).

Only upon the description of a variable, you can use special statements to enter values into it, read them, and refer to the variable name to move it from one part of the program into another.

In the simplest case, a statement describing a variable appears as follows:

```
type name;

```

Here, name must meet the requirements of constructing [identifiers](/en/book/basis/identifiers). As a type, you can specify any of the [embedded types](/en/book/basis/builtin_types) that we have considered in the preceding section or some other custom types – we will learn a bit later how to create them. For example, integer variable i is declared as follows:

```
int i;

```

If necessary, you can describe several variables of the same type simultaneously. In this case, their names are specified in the statement, separated by commas.

```
int i, j, k;

```

An important factor is the place in the program, where the statement is located, which contains the variable description. This affects the lifetime of the variable and its accessibility from various parts of the program.
