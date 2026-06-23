# Pointers

As we said in the [Class Definition](/en/book/oop/classes_and_interfaces/classes_definition) section, pointers in MQL5 are some descriptors (unique numbers) of objects, and not addresses in memory, as in C++. For an automatic object, we obtained a pointer by putting an ampersand in front of its name (in this context, the ampersand character is the "get address" operator). So, in the following example, the variable p points to the automatic object s.

```
Shape s;        // automatic object
Shape *p = &s;  // a pointer to the same object
s.draw();       // calling an object method
p.draw();       // doing the same

```

In the previous sections, we learned how to get a pointer to an object as a result of creating it dynamically with new. At this time, an ampersand is not needed to get a descriptor: the value of the pointer is the descriptor.

The MQL5 API provides the function GetPointer which performs the same action as the ampersand operator '&', i.e. returns a pointer to an object:

```
void *GetPointer(Class object);

```

Which of the two options to use is a matter of preference.

Pointers are often used to link objects together. Let's illustrate the idea of ​​creating subordinate objects that receive a pointer to this of its object-creator (ThisCallback.mq5). We mentioned this trick in the section on the keyword [this](/en/book/oop/classes_and_interfaces/classes_this).

Let's try using it to implement a scheme for notifying the "creator" from time to time about the percentage of calculations performed in the subordinate object: we made its analog using the [function pointer](/en/book/basis/functions/functions_typedef). The class Manager controls calculations, and the calculations themselves (most probably, using different formulas) are performed in separate classes - in this example, one of them, the class Element is shown.

```
class Manager; // preliminary announcement
   
class Element
{
   Manager *owner; // pointer
   
public:
   Element(Manager &t): owner(&t) { }
   
   void doMath()
   {
      const int N = 1000000;
      for(int i = 0; i < N; ++i)
      {
         if(i % (N / 20) == 0)
         {
            // we pass ourselves to the method of the control class
            owner.progressNotify(&this, i * 100.0f / N);
         }
         // ... massive calculations
      }
   }
   
   string getMyName() const
   {
      return typename(this);
   }
};
   
class Manager
{
   Element *elements[1]; // array of pointers (1 for demo)
   
public:
   Element *addElement()
   {
      // looking for an empty slot in the array
      // ...
      // passing to the constructor of the subclass
      elements[0] = new Element(this); // dynamic creation of an object
      return elements[0];
   }
   
   void progressNotify(Element *e, const float percent)
   {
      // Manager chooses how to notify the user:
      // display, print, send to the Internet
      Print(e.getMyName(), "=", percent);
   }
};

```

A subordinate object can use the received link to notify the "boss" about the work progress. Reaching the end of the calculation sends a signal to the control object that it is possible to delete the calculator object, or let another one work. Of course, the fixed one-element array in the class Manager doesn't look very impressive, but as a demonstration, it gets the point across. The manager not only manages the distribution of computing tasks, but also provides an abstract layer for notifying the user: instead of outputting to a log, it can write messages to a separate file, display them on the screen, or send them to the Internet.

By the way, pay attention to the preliminary declaration of the class Manager before the class definition Element. It is needed to describe in the class Element a pointer to the class Manager, which is defined below in the code. If the forward declaration is omitted, we get the error "'Manager' - unexpected token, probably type is missing?".

The need for forward declaration arises when two classes refer to each other through their members: in this case, in whatever order we arrange the classes, it is impossible to fully define either of them. A forward declaration allows you to reserve a type name without a full definition.

A fundamental property of pointers is that a pointer to a base class can be used to point to an object of any derived class. This is one of the manifestations of [polymorphism](/en/book/oop/classes_and_interfaces/classes_polymorphism). This behavior is possible because derived objects contain built-in "sub-objects" of parent classes like nesting dolls matryoshkas.

In particular, for our task with shapes, it is easy to describe a dynamic array of pointers Shape and add objects of different types to it at the request of the user.

The number of classes will be expanded to five (Shapes2.mq5). In addition to Rectangle and Ellipse, let's add Triangle, and also make a class derived from Rectangle for a square (Square), and a class derived from Ellipse for a circle (Circle). Obviously, a square is a rectangle with equal sides, and a circle is an ellipse with the equal large and small radii.

To pass a string class name along the inheritance chain, let's add in the protected sections of the classes Rectangle and Ellipse special constructors with an additional string parameter t:

```
class Rectangle : public Shape
{
protected:
   Rectangle(int px, int py, int sx, int sy, color back, string t) :
      Shape(px, py, back, t), dx(sx), dy(sy)
   {
   }
   ...
};

```

Then, when creating a square, we set not only equal sizes of the sides but also pass typename(this) from the class Square:

```
class Square : public Rectangle
{
public:
   Square(int px, int py, int sx, color back) :
      Rectangle(px, py, sx, sx, back, typename(this))
   {
   }
};

```

In addition, we will move constructors in the class Shape to the protected section: this will prohibit the creation of the object Shape by itself - it can only act as a base for their descendant classes.

Let's assign the function addRandomShape to generate shapes, which returns a pointer to a newly created object. For demonstration purposes, it will now implement a random generation of shapes: their types, positions, sizes and colors.

Supported shape types are summarized in the SHAPES enumeration: they correspond to five implemented classes.

Random numbers in a given range are returned by the function random (it uses the built-in function [rand](/en/book/common/maths/maths_rand), which returns a random integer in the range from 0 to 32767 each time it is called. The centers of the shapes are generated in the range from 0 to 500 pixels, the sizes of the shapes are in the range of up to 200. The color is formed from three RGB components (see [Color](/en/book/basis/builtin_types/colors) section), each ranging from 0 to 255.

```
int random(int range)
{
   return (int)(rand() / 32767.0 * range);
}
   
Shape *addRandomShape()
{
   enum SHAPES
   {
      RECTANGLE,
      ELLIPSE,
      TRIANGLE,
      SQUARE,
      CIRCLE,
      NUMBER_OF_SHAPES
   };
   
   SHAPES type = (SHAPES)random(NUMBER_OF_SHAPES);
   int cx = random(500), cy = random(500), dx = random(200), dy = random(200);
   color clr = (color)((random(256) << 16) | (random(256) << 8) | random(256));
   switch(type)
   {
      case RECTANGLE:
         return new Rectangle(cx, cy, dx, dy, clr);
      case ELLIPSE:
         return new Ellipse(cx, cy, dx, dy, clr);
      case TRIANGLE:
         return new Triangle(cx, cy, dx, clr);
      case SQUARE:
         return new Square(cx, cy, dx, clr);
      case CIRCLE:
         return new Circle(cx, cy, dx, clr);
   }
   return NULL;
}
   
void OnStart()
{
   Shape *shapes[];
   
   // simulate the creation of arbitrary shapes by the user
   ArrayResize(shapes, 10);
   for(int i = 0; i < 10; ++i)
   {
      shapes[i] = addRandomShape();
   }
   
   // processing shapes: for now, just output to the log 
   for(int i = 0; i < 10; ++i)
   {
      Print(i, ": ", shapes[i].toString());
      delete shapes[i];
   }
}

```

We generate 10 shapes and output them to the log (the result may differ due to the randomness of the choice of types and properties). Don't forget to delete the objects with delete because they were created dynamically (here this is done in the same loop because the shapes are not used further; in a real program, the array of shapes will most likely be stored somehow to a file for later loading and continuing to work with an image).

```
0: Ellipse 241 38
1: Rectangle 10 420
2: Circle 186 38
3: Triangle 27 225
4: Circle 271 193
5: Circle 293 57
6: Rectangle 71 424
7: Square 477 46
8: Square 366 27
9: Ellipse 489 105

```

The shapes are successfully created and inform about their properties.

We are now ready to access the API of our classes, i.e. the draw method.
