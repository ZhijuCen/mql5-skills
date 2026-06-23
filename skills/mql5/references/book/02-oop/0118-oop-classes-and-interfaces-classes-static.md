# Static members

So far, we have considered the fields and methods of a class that describe the state and behavior of objects of a given class. However, in programs, it may be necessary to store certain attributes or perform operations on the entire class, rather than on its objects. Such class properties are called static and are described using the static keyword added before the type. They are also supported in structures and unions.

For example, we can count the number of shapes created by the user in a drawing program. To do this, in the class Shape, we will describe the static variable count(Shapes5.mq5).

```
class Shape
{
private:
   static int count;
   
protected:
   ...
   Shape(int px, int py, color back, string t) :
      coordinates(px, py),
      backgroundColor(back),
      type(t)
   {
      ++count;
   }
   
public:
   ...
   static int getCount()
   {
      return count;
   }
};

```

It is defined in the private section and therefore not accessible from the outside.

To read the current counter value, a public static method getCount() is provided. In theory, since static members are defined in the context of a class, they receive visibility restrictions according to the modifier of the section in which they are located.

We will increase the counter by 1 in the parametric constructor Shape, and remove the default constructor. Thus, each instance of a shape of any derived type will be taken into account.

Note that a static variable must be explicitly defined (and optionally initialized) outside the class block:

```
static int Shape::count = 0;

```

Static class variables are similar to global variables and static variables inside functions (see section [Static variables](/en/book/basis/variables/static_variables)) in the sense that they are created when the program starts and are deleted before it is unloaded. Therefore, unlike object variables, they must exist from the beginning as a single instance.

In this case, zero-initialization can be omitted because, as we know, global and static variables are set to zero by default. Arrays can also be static.

In the definition of a static variable, we see the use of the special context selection operator ['::'](/en/book/oop/classes_and_interfaces/classes_namespace_context). With it, a fully qualified variable name is formed. To the left of '::' is the name of the class to which the variable belongs, and to the right is its identifier. Obviously, the fully qualified name is necessary, because within different classes static variables with the same identifier can be declared, and a way to uniquely refer to each of them is needed.

The same '::' operator is used to access not only public static class variables but also methods. In particular, in order to call the method getCount in the OnStart function, we use the syntax Shape::getCount():

```
void OnStart()
{
   for(int i = 0; i < 10; ++i)
   {
      Shape *shape = addRandomShape();
      shape.draw();
      delete shape;
   }
   
   Print(Shape::getCount()); // 10
}

```

Since the specified number of shapes (10) is now being generated, we can verify that the counter is working correctly.

If you have a class object, you can refer to a static method or property through the usual dereference (for example, shape.getCount()), but such a notation can be misleading (because it hides the fact that the object is actually not accessed).

Note that the creation of derived classes does not affect static variables and methods in any way: they are always assigned to the class in which they were defined. Our counter is the same for all classes of shapes derived from Shape.

You can't use this inside static methods because they are executed without being tied to a specific object. Also, from a static method, you cannot directly, without dereferencing any object type variable, call a regular class method or access its field. For example, if you call draw from getCount, you get an "access to non-static member or function" error:

```
   static int getCount()
   {
      draw(); // error: 'draw' - access to non-static member or function
      return count;
   }

```

For the same reason, static methods cannot be virtual.

Is it possible, using static variables, to calculate not the total number of shapes, but their statistics by type? Yes, it is possible. This task is left for independent study. Those interested can find one of the implementation examples in the script Shapes5stats.mq5.
