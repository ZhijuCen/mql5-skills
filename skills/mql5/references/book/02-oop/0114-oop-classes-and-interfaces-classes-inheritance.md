# Inheritance

When defining a class, a developer can inherit it from another class, thereby embodying the [concept of inheritance](/en/book/oop/classes_and_interfaces/classes_oop_inheritance). To do this, the class name is followed by a colon sign, an optional access rights modifier (one of the keywords public, protected, private), and the name of the parent class. For example, here's how we can define a class Rectangle that derives from Shape:

```
class Rectangle : public Shape
{
};

```

Access modifiers in the class header control the "visibility" of the members of the parent class included in the child class:

- public — all inherited members retain their rights and limitations
- protected — changes the rights of inherited public members to protected
- private — makes all inherited members private (private)

The modifier public is used in the vast majority of definitions. The other two options make sense only in exceptional cases because they violate the basic principle of inheritance: objects of a derived class should be "is a" – full-fledged representatives of the parent family, and if we "truncate" their rights, they lose part of their characteristics. Structures can also be inherited from each other in a similar way. It is forbidden to inherit classes from structures or structures from classes.

Unlike C++, MQL5 does not support multiple inheritance. A class can have at most one parent.

A derived class object has a base class object built into it. Considering that the base class can, in turn, be inherited from some other parent class, the created object can be compared to matryoshka dolls nested one inside the other.

In the new class, we need a constructor that fills in the fields of the object in the same way as it was done in the base class.

```
class Rectangle : public Shape
{
public:
   Rectangle(int px, int py, color back) :
      Shape(px, py, back)
   {
      Print(__FUNCSIG__, " ", &this);
   }
};

```

In this case, the initialization list has become a single call to the Shape constructor. You cannot directly set base class variables in an initialization list, because the base constructor is responsible for initializing them. However, if necessary, we could change the protected fields of the base class from the body of the constructor Rectangle (the statements in the function body are executed after the base constructor has completed its call in the initialization list).

The rectangle has two dimensions, so let's add them as protected fields dx and dy. To set their values, you need to supplement the list of constructor parameters.

```
class Rectangle : public Shape
{
protected:
   int dx, dy; // dimensions (width, height)
   
public:
   Rectangle(int px, int py, int sx, int sy, color back) :
      Shape(px, py, back), dx(sx), dy(sy)
   {
   }
};

```

It is important to note that the Rectangle objects implicitly contain the toString function inherited from Shape (however, draw is also present there, but it is still empty). Therefore, the following code is correct:

```
void OnStart()
{
   Rectangle r(100, 200, 50, 75, clrBlue);
   Print(r.toString());
};

```

This demonstrates not only calling toString but also creating a rectangle object using our new constructor.

There is no default constructor (with no parameters) in the class Rectangle. This means that the user of the class cannot create rectangle objects in a simple way, without arguments:

```
   Rectangle r; // 'Rectangle' - wrong parameters count

```

The compiler will show an error "Invalid number of arguments".

Let's create another daughter class – Ellipse. For now, it will not differ from Rectangle in any way, except for the name. Later we will introduce the differences between them.

```
class Ellipse : public Shape
{
protected:
   int dx, dy; // dimensions (large and small radii)
public:
   Ellipse(int px, int py, int rx, int ry, color back) :
      Shape(px, py, back), dx(rx), dy(ry)
   {
      Print(__FUNCSIG__, " ", &this);
   }
};

```

As the number of classes increases, it would be great to display the class name in the toString method. In the [Special sizeof and typename operators](/en/book/basis/expressions/operators_sizeof_typename) section, we described the typename operator. Let's try using it.

Recall that typename expects one parameter, for which the type name is returned. For example, if we create a pair of objects s and r of classes Shape and Rectangle, respectively, we can find out their type in the following way:

```
void OnStart()
{
   Shape s;
   Rectangle r(100, 200, 75, 50, clrRed);
   Print(typename(s), " ", typename(r));      // Shape Rectangle
}

```

But we need to get this name inside the class somehow. For this purpose, let's add a string parameter to the parametric constructor Shape and store it in a new string field type (pay attention to the protected section and the modifier const: this field is hidden from the outside world and cannot be edited after the object has been created):

```
class Shape
{
protected:
   ...
   const string type;
   
public:
   Shape(int px, int py, color back, string t) :
      coordinates(px, py),
      backgroundColor(back),
      type(t)
   {
      Print(__FUNCSIG__, " ", &this);
   }
   ...
};

```

In the constructors of derived classes, we fill in this parameter of the base constructor using typename(this):

```
class Rectangle : public Shape
{
   ...
public:
   Rectangle(int px, int py, int sx, int sy, color back) :
      Shape(px, py, back, typename(this)), dx(sx), dy(sy)
   {
      Print(__FUNCSIG__, " ", &this);
   }
};

```

Now we can improve the method toString using the type field.

```
class Shape
{
   ...
public:
   string toString() const
   {
      return type + " " + (string)coordinates.x + " " + (string)coordinates.y;
   }
};

```

Let's make sure that our little class hierarchy spawns objects as intended and prints test log entries when constructors and destructors are called.

```
void OnStart()
{
   Shape s;
   //setting up an object by chaining calls via 'this'
   s.setColor(clrWhite).moveX(80).moveY(-50);
   Rectangle r(100, 200, 75, 50, clrBlue);
   Ellipse e(200, 300, 100, 150, clrRed);
   Print(s.toString());
   Print(r.toString());
   Print(e.toString());
}

```

As a result, we get approximately the following log entries (blank lines are added intentionally to separate the output from different objects):

```
Pair::Pair(int,int) 0 0
Shape::Shape() 1048576
   
Pair::Pair(int,int) 100 200
Shape::Shape(int,int,color,string) 2097152
Rectangle::Rectangle(int,int,int,int,color) 2097152
   
Pair::Pair(int,int) 200 300
Shape::Shape(int,int,color,string) 3145728
Ellipse::Ellipse(int,int,int,int,color) 3145728
   
Shape 80 -50
Rectangle 100 200
Ellipse 200 300
   
Ellipse::~Ellipse() 3145728
Shape::~Shape() 3145728
Pair::~Pair() 200 300
   
Rectangle::~Rectangle() 2097152
Shape::~Shape() 2097152
Pair::~Pair() 100 200
   
Shape::~Shape() 1048576
Pair::~Pair() 80 -50

```

The log makes it clear in what order the constructors and destructors are called.

For each object, firstly, the object fields described in it are created (if there are any), and then the base constructor and all constructors of derived classes along the inheritance chain are called. If there are own (added) fields of some object types in a derived class, the constructors for them will be called immediately before the constructor of this derived class. When there are several object fields, they are created in the order in which they are described in the class.

Destructors are called in exactly the reverse order.

In the derived classes copy constructors can be defined, which we learned about in [Constructors: Default, Parametric, Copy](/en/book/oop/classes_and_interfaces/classes_ctors). For specific shape types, such as a rectangle, their syntax is similar:

```
class Rectangle : public Shape
{
   ...
   Rectangle(const Rectangle &other) :
      Shape(other), dx(other.dx), dy(other.dy)
   {
   }
   ...
};

```

The scope is slightly expanding. A derived class object can be used to copy to a base class (because the derived class contains all the data for the base class). However, in this case, of course, the fields added in the derived class are ignored.

```
void OnStart()
{
   Rectangle r(100, 200, 75, 50, clrBlue);
   Shape s2(r);         // ok: copy derived to base
   
   Shape s;
   Rectangle r4(s);     // error: no one of the overloads can be applied 
                        // requires explicit constructor overloading
}

```

To copy in the opposite direction, you need to provide a constructor version with a reference to the derived class in the base class (which, in theory, contradicts the principles of OOP), otherwise the compilation error "no one of the overloads can be applied to the function call" will occur.

Now we can script a couple or more shape variables to then "ask" them to draw themselves using the method draw.

```
void OnStart()
{
   Rectangle r(100, 200, 50, 75, clrBlue);
   Ellispe e(100, 200, 50, 75, clrGreen);
   r.draw();
   e.draw();
};

```

However, such an entry means that the number of shapes, their types, and parameters are hardwired into the program, while the should be able to choose what and where to draw. Hence the need to create shapes in a dynamic way.
