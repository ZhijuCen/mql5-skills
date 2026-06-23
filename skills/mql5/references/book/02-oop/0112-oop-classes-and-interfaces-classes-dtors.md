# Destructors

In the chapter on structures, we learned about destructors (see the section about [Constructors and destructors](/en/book/oop/structs_and_unions/structs_ctor_dtor)). Let's briefly recap: a destructor is a method that is called when an object is destroyed. The destructor shares the same name as the class but is prefixed with a tilde character (~). Destructors do not return values and do not have any parameters. A class can only have one destructor.

Even if the class has no destructor or the destructor is empty, the compiler will implicitly perform "garbage collection" of the following types of fields: strings, dynamic arrays, and automatic objects.

Usually, the destructor is placed in the public section of the class, however, in some specific cases, the developer can move it to a group of private or protected members. A private or protected destructor will not allow you to declare an automatic variable of this class in the code. However, we will see [dynamic object creation](/en/book/oop/classes_and_interfaces/classes_new_delete_pointers) a little later, and for them, such a restriction might make sense.

In particular, some objects can be implemented in such a way that they must delete themselves when they are no longer needed (the concept of determining demand may be different). In other words, while objects are used by any part of the program, they exist, and as soon as the task is completed, they are self-destructed (a private destructor leaves the possibility to delete the object from class methods).

For experienced C++ programmers, it is worth noting that destructors are always virtual in MQL5 (more on virtual methods will be covered in the section about [Virtual methods (virtual and override)](/en/book/oop/classes_and_interfaces/classes_virtual_override)). This factor does not affect the syntax of the description.

In the example of the drawing program, technically, a destructor may not be necessary for shapes. However, for the purpose of tracing the sequence of calls to constructors and destructors, we will include one. Let's start with a simplified outline that "prints" the full name of the method:

```
class Shape
{
   ...
   ~Shape()
   {
      Print(__FUNCSIG__);
   }
};

```

We will soon add to this and other methods so that we can distinguish one instance of an object from another.

Consider the following example. A pair of objects Shape are described in two different contexts: global (outside functions) and local (inside OnStart). The global object constructor will be called after the script is loaded and before OnStart is called, and the destructor will be called before the script is unloaded. The local object's constructor will be called in the line with the variable definition, and the destructor will be called when the code block containing the variable definition exits, in this case the function OnStart.

```
// the global constructor and destructor are related to script loading and unloading
Shape global;
 
// object reference does not create a copy and does not affect lifetime
void ProcessShape(Shape &shape)
{
   // ...
}
 
void OnStart()
{
   // ...
   Shape local; // <- local constructor call
   // ...
   ProcessShape(local);
   // ...
} // <- local destructor call

```

Passing an object by reference to other functions does not create copies of it and does not call the constructor and destructor.
