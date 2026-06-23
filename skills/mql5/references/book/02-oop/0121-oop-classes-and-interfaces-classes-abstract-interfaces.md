# Abstract classes and interfaces

To explore abstract classes and interfaces, let's go back to our end-to-end drawing program example. Its API for simplicity consists of a single virtual method draw. Until now, it has been empty, but at the same time, even such an empty implementation is a concrete implementation. However, objects of the class Shape cannot be drawn - their shape is not defined. Therefore, it makes sense to make the method draw abstract or, as it is otherwise called, purely virtual.

To do this, the block with an empty implementation should be removed, and "= 0" should be added to the method header:

```
class Shape
{
public:
   virtual void draw() = 0;
   ...

```

A class that has at least one abstract method also becomes abstract, because its object cannot be created: there is no implementation. In particular, our constructor Shape was available to derived classes (thanks to the protected modifier), and their developers could, hypothetically, create an object Shape. But it was like that before, and after the declaration of the abstract method, we stopped this behavior, as it was forbidden by us, the authors of the drawing interface. The compiler will throw an error:

```
'Shape' -cannot instantiate abstract class
      'void Shape::draw()' is abstract

```

The best approach to describe an interface is to create an abstract class for it, containing only abstract methods. In our case, the method draw should be moved to the new class Drawable, and the class Shape should be inherited from it (Shapes.mq5).

```
class Drawable
{
public:
   virtual void draw() = 0;
};
 
class Shape : public Drawable
{
public:
   ...
   // virtual void draw() = 0; // moved to base class
   ...
};

```

Of course, interface methods must be in the section public.

MQL5 provides another convenient way to describe interfaces by using the keyword interface. All methods in an interface are declared without implementation and are considered public and virtual. The description of the Drawable interface which is equivalent to the above class looks like this:

```
interface Drawable
{
   void draw();
};

```

In this case, nothing needs to be changed in the descendant classes if there were no fields in the abstract class (which would be a violation of the abstraction principle).

Now it's time to expand the interface and make the trio of methods setColor, moveX, moveY also part of it.

```
interface Drawable
{
   void draw();
   Drawable *setColor(const color c);
   Drawable *moveX(const int x);
   Drawable *moveY(const int y);
};

```

Note that the methods return a Drawable object because I don't know anything about Shape. In the Shape class, we already have implementations that are suitable for overriding these methods, because Shape inherits from Drawable (Shape "are sort of" Drawable objects).

Now third-party developers can add other families of Drawable classes to the drawing program, in particular, not only shapes, but also text, bitmaps, and also, amazingly, collections of other Drawables, which allows you to nest objects in each other and make complex compositions. It is enough to inherit from the interface and implement its methods.

```
class Text : public Drawable
{
public:
   Text(const string label)
   {
      ...
   }
   
   void draw()
   {
      ...
   }
   
   Text *setColor(const color c)
   {
      ...
      return &this;
   }
   ...
};

```

If the shape classes were distributed as a binary ex5 library (without source codes), we would supply a header file for it containing only the description of the interface, and no hints about the internal data structures.

Since virtual functions are dynamically (later) bound to an object during program execution, it is possible to get a "Pure virtual function call" fatal error: the program terminates. This happens if the programmer inadvertently "forgot" to provide an implementation. The compiler is not always able to detect such omissions at compile time.
