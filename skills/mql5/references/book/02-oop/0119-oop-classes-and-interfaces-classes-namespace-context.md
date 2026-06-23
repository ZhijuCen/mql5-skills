# Nested types, namespaces, and the context operator '::'

Classes, structures, and unions can be described not only in the global context but also within another class or structure. And even more: the definition can be done inside the function. This allows you to describe all the entities necessary for the operation of any class or structure within the appropriate context and thereby avoid potential name conflicts.

In particular, in the drawing program, the structure for storing coordinates Pair has been defined globally so far. As the program grows, it is quite possible that another entity called Pair will be needed (especially given the rather generic name). Therefore, it is desirable to move the description of the structure inside the class Shape (Shapes6.mq5).

```
class Shape
{
public:
   struct Pair
   {
      int x, y;
      Pair(int a, int b): x(a), y(b) { }
   };
   ...
};

```

The nested descriptions have access permissions in accordance with the specified section modifiers. In this case, we have made the name Pair publicly available. Inside the class Shape, the handling of the Pair structure type does not change in any way due to the transfer. However, in external code, you must specify a fully qualified name that includes the name of the external class (context), the context selection operator '::' and the internal entity identifier itself. For example, to describe a variable with a pair of coordinates, you would write:

```
Shape::Pair coordinates(0, 0);

```

The level of nesting when describing entities is not limited, so a fully qualified name can contain identifiers of multiple levels (contexts) separated by '::'. For example, we could wrap all drawing classes inside the outer class Drawing, in the public section.

```
class Drawing
{
public:
   class Shape
   {
   public:
      struct Pair
      {
         ...
      };
   };
   class Rectangle : public Shape
   {
      ...
   };
   ...
};

```

Then fully qualified type names (e.g. for use in OnStart or other external functions) would be lengthened:

```
Drawing::Shape::Rect coordinates(0, 0);
Drawing::Rectangle rect(200, 100, 70, 50, clrBlue);

```

On the one hand, this is inconvenient, but on the other hand, it is sometimes a necessity in large projects with a large number of classes. In our small project, this approach is used only to demonstrate the technical feasibility.

To combine logically related classes and structures into named groups, MQL5 provides an easier way than including them in an "empty" wrapper class.

A namespace is declared using the keyword namespace followed by the name and a block of curly braces that includes all the necessary definitions. Here's what the same paint program looks like using namespace:

```
namespace Drawing
{
   class Shape
   {
   public:
      struct Pair
      {
         ...
      };
   };
   class Rectangle : public Shape
   {
      ...
   };
   ...
}

```

There are two main differences: the internal contents of the space are always available publicly (access modifiers are not applicable in it) and there is no semicolon after the closing curly brace.

Let's add the method move to the class Shape, which takes the structure Pair as a parameter:

```
class Shape
{
public:
   ...
   Shape *move(const Pair &pair)
   {
      coordinates.x += pair.x;
      coordinates.y += pair.y;
      return &this;
   }
};

```

Then, in the function OnStart, you can organize the shift of all shapes by a given value by calling this function:

```
void OnStart()
{
   //draw a random set of shapes
   for(int i = 0; i < 10; ++i)
   {
      Drawing::Shape *shape = addRandomShape();
      // move all shapes
      shape.move(Drawing::Shape::Pair(100, 100));
      shape.draw();
      delete shape;
   }
}

```

Note that the types Shape and Pair have to be described with full names: Drawing::Shape and Drawing::Shape::Pair respectively.

There may be several blocks with the same space name: all their contents will fall into one logically unified context with the specified name.

Identifiers defined in the global context, in particular all built-in functions of the MQL5 API, are also available through the context selection operator not preceded by any notation. For example, here's what a call to the function Print might look like:

```
::Print("Done!");

```

When the call is made from any function defined in the global context, there is no need for such an entry.

Necessity can manifest itself inside any class or structure if an element of the same name (function, variable or constant) is defined in them. For example, let's add the method Print to the class Shape:

```
   static void Print(string x)
   {
      // empty
      // (likely will output it to a separate log file later)
   }

```

Since the test implementations of the draw method in derived classes call Print, they are now redirected to this Print method: from several identical identifiers, the compiler chooses the one that is defined in a closer context. In this case, the definition in the base class is closer to the shapes than the global context. As a result, logging output from shape classes will be suppressed.

However, calling Print from the function OnStart still works (because it is outside the context of the class Shape).

```
void OnStart()
{
   ...
   Print("Done!");
}

```

To "fix" debug printing in classes, you need to precede all Print calls with a global context selection operator:

```
class Rectangle : public Shape
{
   ...
   void draw() override
   {
      ::Print("Drawing rectangle"); // reprint via global Print(...)
   }
};

```
