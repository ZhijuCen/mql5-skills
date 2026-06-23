# Dynamic creation of objects: new and delete

So far we have only tried to create automatic objects, i.e. local variables inside OnStart. An object declared in the global context (outside OnStart or some other function) would also be automatically created (when the script is loaded) and deleted (when the script is unloaded).

In addition to these two modes, we have touched on the ability to describe a field of an object type (in our example, this is the structure Pair used for the field coordinates inside the object Shape). All such objects are also automatic: they are created for us by a compiler in a constructor of a "host" object and deleted in its destructor.

However, it is quite often impossible to get by with only automatic objects in programs. In the case of a drawing program, we will need to create shapes at the user's request. Moreover, shapes will need to be stored in an array, and for this automatic objects would have to have a default constructor (which is not the case in our case.

For such situations, MQL5 offers the opportunity to dynamically create and delete objects. Creation is implemented with the operator new and deletion with the operator delete.

Operator new

The keyword new is followed by the name of the required class and, in parentheses, a list of arguments to call any of the existing constructors. Execution of the operator new leads to the creation of an instance of the class.

The operator new returns a value of a special type — a pointer to an object. To describe a variable of this type, add an asterisk character '*' after the class name. For example:

```
Rectangle *pr = new Rectangle(100, 200, 50, 75, clrBlue);

```

Here the variable pr has a type of pointer to an object of the class Rectangle. Pointers will be discussed in more detail in a separate [section](/en/book/oop/classes_and_interfaces/classes_pointers).

It is important to note that the declaration of a variable of an object pointer type itself does not allocate memory for an object and does not call its constructor. Of course, a pointer takes up space - 8 bytes, but in fact, it is an unsigned integer ulong, which the system interprets in a special way.

You can work with a pointer in the same way as with an object, i.e., you can call available methods through the dereference operator and access fields.

```
Print(pr.toString());

```

A pointer variable that has not yet been assigned a dynamic object descriptor (for example, if the operator new is called not at the time of initialization of a new variable, but is moved to some later lines of the source code), contains a special null pointer, which is denoted as NULL (to distinguish it from numbers) but is actually equal to 0.

Operator delete

Pointers received via new should be freed at the end of an algorithm using the operator delete. For example:

```
delete pr;

```

If this is not done, the instance allocated by the operator new will remain in memory. If more and more new objects are created in this way, and then not deleted when they are no longer needed, this will lead to unnecessary memory consumption. The remaining unreleased dynamic objects cause warnings to be printed when the program terminates. For example, if you don't delete the pointer pr, you'll get something like this in the log after the script is unloaded:

```
1 undeleted object left
1 object of type Rectangle left
168 bytes of leaked memory

```

The terminal reports how many objects and what class were forgotten by the programmer, as well as how much memory they occupied.

Once the operator delete is called for a pointer, the pointer is invalidated because the object no longer exists. A subsequent attempt to access its properties causes a run-time error "Invalid pointer accessed":

```
Critical error while running script 'shapes (EURUSD,H1)'.
Invalid pointer access.

```

The MQL program is then interrupted.

This, however, does not mean that the same pointer variable can no longer be used. It is enough to assign a pointer to another newly created instance of the object.

MQL5 has a built-in function that allows you to check the validity of a pointer in a variable — CheckPointer:

```
ENUM_POINTER_TYPE CheckPointer(object *pointer);

```

It takes one parameter of a pointer to a type class and returns a value from the ENUM_POINTER_TYPE enumeration:

- POINTER_INVALID — incorrect pointer;
- POINTER_DYNAMIC — valid pointer to a dynamic object;
- POINTER_AUTOMATIC — valid pointer to an automatic object.

Execution of the statement delete only makes sense for a pointer for which the function returned POINTER_DYNAMIC. For an automatic object, it will have no effect (such objects are deleted automatically when control returns from the block of code in which the variable is defined).

The following macro simplifies and ensures the correct cleanup for a pointer:

```
#define FREE(P) if(CheckPointer(P) == POINTER_DYNAMIC) delete (P)

```

The necessity to explicitly "clean up" is an inevitable price to pay for the flexibility provided by dynamic objects and pointers.
