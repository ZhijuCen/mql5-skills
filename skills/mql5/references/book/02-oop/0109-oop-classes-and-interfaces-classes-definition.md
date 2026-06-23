# Class definition

The class definition statement has many optional components that affect its characteristics. In a generalized form, it can be represented as follows:

```
class class_name [: modifier_access name_parent_class ...]
{
  [ modifier_access:]
     [description_member...]
  ...
};

```

To make the presentation easier, we will start with the minimum sufficient syntax and will expand it as we move through the material.

As a starting ground, we use a task with a conditional drawing program that supports several types of shapes.

To define a new class, use the class keyword, followed by the class identifier and a block of code in curly brackets. Like all statements, such a definition must end with a semicolon.

The code block can be empty. For example, a compilable template of class Shape for a drawing program looks like this:

```
class Shape
{
};

```

From the previous chapters of the book, we know that curly brackets denote the context or scope of variables. When such blocks occur in a function definition, they define its local context. In addition to it, there is a global context in which the functions themselves are defined, as well as global variables.

This time, the parentheses in the class definition define a new kind of context, the class context. It is a container for both variables and functions declared inside the class.

The description of variables for storing class properties is done by the usual statements inside the block (Shapes1.mq5).

```
class Shape
{
   int x, y;              // center coordinates
   color backgroundColor; // fill color
};

```

Here we have declared some of the fields discussed in the theoretical sections: the coordinates of the shape center and the fill color.

After such a description, the user-defined type Shape becomes available in the program along with the built-in types. In particular, we can create a variable of this type, and it will contain the specified fields inside. However, we cannot yet do anything with them and even make sure that they are there.

```
void OnStart()
{
   Shape s;
   // errors: cannot access private member declared in class 'Shape'
   Print(s.x, " ", s.y);
}

```

Class members are private by default, and therefore cannot be accessed from other parts of the code external to the class. This is the principle of encapsulation in action.

If we try to output a shape to the log, the result will disappoint us for several reasons.

The most straightforward approach will cause the "objects are only passed by reference" error (we've seen this with structures too):

```
Print(s); // 's' - objects are passed by reference only

```

Objects may consist of many fields, and because of their large size, it is inefficient to pass them by value. Therefore, the compiler requires object type parameters to be passed by reference, while Print takes values.

From the section about function parameters (see section [Value parameters and reference parameters](/en/book/basis/functions/functions_ref_value)), we know that the symbol '&' is used to describe references. It would be logical to assume that in order to obtain a reference to a variable (in this case, an object s of type Shape) it is necessary to put the same sign before its name.

```
Print(&s);

```

This statement compiles and runs without problem but does not quite do what was expected.

The program outputs some integer number during execution, for example, 1 or 2097152 (it will most likely be different). An ampersand sign in front of a variable name means getting a pointer to this variable, not a reference (as opposed to a function parameter description).

[Pointers](/en/book/oop/classes_and_interfaces/classes_pointers) will be discussed in detail in a separate section. However, note that MQL5 does not provide direct access to memory, and the pointer to an object is a descriptor, or in a simple way, a unique object number (it is assigned by the terminal itself). But even if the pointer pointed to an address in memory (as it does in C++), that would not provide a legal way to read the object's contents.

To output the contents of Shape objects to the log or whatever, a class member function is required. Let's call it toString: it should return a string with some description of the object. We can decide later what to display in it. Let's also reserve the draw method for drawing the shape. For now, it will act as a declaration of the future object programming interface.

```
class Shape
{
   int x, y;              // center coordinates
   color backgroundColor; // fill color
   
   string toString()
   {
      ...
   }
   
   void draw() { /* future drawing interface stub */ }
};

```

The definition of method functions is done in the usual way, with the only difference being that they are located inside the block of code that forms the class.

In the future, we will learn how to separate the declaration of a function inside the class block and its [definition outside the block](/en/book/oop/classes_and_interfaces/classes_declaration_definition). This approach is often used to put declarations in a header file and "hide" definitions in an mq5 file. This makes the code more understandable (due to the fact that the programming interface is presented separately, in a compact form, without implementation). It also allows [software libraries](/en/book/advanced/libraries) to be distributed as ex5 files if needed (without the main source code but providing a header file that is sufficient to call the external interface methods).

Because the method toString is part of the class, it has access to variables and can convert them to a string. For example,

```
string toString()
{
  return (string)x + " " + (string)y;
}

```

However, now toString and draw are private, as are the rest of the fields. We need to make them available from outside the class.
