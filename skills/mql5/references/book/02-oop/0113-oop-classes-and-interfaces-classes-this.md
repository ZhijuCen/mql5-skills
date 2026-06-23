# Self-reference: this

In the context of each class, in its methods code, there is a special reference to the current object: this. Basically, it is an implicitly defined variable. All the methods of working with object variables are applicable to it. In particular, it can be dereferenced to refer to an object field or to call a method. For example, the following statements in a method of the Shape class are identical (we use the draw method for demonstration purposes only):

```
class Shape
{
   ...
   void draw()
   {
      backgroundColor = clrBlue;
      this.backgroundColor = clrBlue;
   }
};

```

It might be necessary to use the long form if there are other variables/parameters with the same name in the same context. This practice is generally not welcomed, but if necessary, the keyword this allows you to refer to the overridden members of an object.

The compiler issues a warning if the name of any local variable or method parameter overlaps the name of a class member variable.

In the following hypothetical example, we have implemented the draw method, which takes an optional string parameter backgroundColor with the color name. Because the parameter name is the same as the class member Shape, the compiler issues the first warning "the definition of 'backgroundColor' hides the field".

The consequence of the overlap is that the subsequent erroneous assignment of the clrBlue value works on the parameter and not on the class member, and because the value and parameter types do not match, the compiler will issue a second warning, "implicit number to string conversion" (the number here is a constant clrBlue). But the line this.backgroundColor = clrBlue writes the value to the field of the object.

```
   void draw(string backgroundColor = NULL) //warning 1:
                // declaration of 'backgroundColor' hides member
   {
      ...
      backgroundColor = clrBlue; // warning 2:
        // implicit conversion from 'number' to 'string'
      this.backgroundColor = clrBlue; // ok
      
      {
         bool backgroundColor = false; // warning 3:
             // declaration of 'backgroundColor' hides local variable
         ...
         this.backgroundColor = clrRed; // ok
      }
      ...
   }

```

The subsequent definition of the local boolean variable backgroundColor (in the nested block of curly brackets) overrides the previous definitions of that name once again (which is why we get the third warning). However, by dereferencing this, the statement this.backgroundColor = clrRed also refers to an object field.

Without this specified, the compiler always chooses the closest (by context) name definition.

There is also a need for this of another kind: to pass the current object as a parameter to another function. In particular, an approach is taken in which objects of the same class are responsible for creating/deleting objects of another class, and the subordinate object must know its "boss". Then the dependent objects are created in the "boss" class using the constructor, and this of the "boss" object is passed into it. This technique typically uses dynamic object allocation and pointers, and due to this a relevant example will be shown in the section [pointers](/en/book/oop/classes_and_interfaces/classes_pointers).

Another common use of this is to return a pointer to the current object from a member function. This allows you to arrange member function calls in a chain. As we have yet to study pointers in detail, it will be enough to know that a pointer to an object of some class is described by adding the character '*' to the class name, and you can work with an object through a pointer in the same way as you would do directly.

For example, we can provide the user with several methods to set the properties of a shape individually: change color, move horizontally or vertically. Each of them will return a pointer to the current object.

```
   Shape *setColor(const color c)
   {
      backgroundColor = c;
      return &this;
   }
   
   Shape *moveX(const int x)
   {
      coordinates.x += x;
      return &this;
   }
 
   Shape *moveY(const int y)
   {
      coordinates.y += y;
      return &this;
   }

```

Then it is possible to conveniently arrange calls to these methods in a chain.

```
   Shape s;
   s.setColor(clrWhite).moveX(80).moveY(-50);

```

When there are many properties in a class, this approach allows you to compactly and selectively configure an object.

In the section [Class definition](/en/book/oop/classes_and_interfaces/classes_definition), we tried to log an object variable but discovered that we could use its name with only an ampersand (in a Print call) to get a pointer, or, in fact, a unique number (handle). In an object context, the same handle is available via &this.

For debugging purposes, you can identify objects by their descriptor. We're going to explore class inheritance, and when there is more than one of those, identification will come in handy. Because of it, in all constructors and destructors, we add (and will add in the future in derived classes) the following Print call:

```
   ~Shape()
   {
      Print(__FUNCSIG__, " ", &this);
   }

```

Now all creation and deletion steps will be marked in the log with the class name and object number.

We implement similar constructors and destructors in the Pair structure, however in structures, unfortunately, pointers are not supported, i.e. writing &this is impossible. Therefore, we can identify them only by their content (in this case, by their coordinates):

```
struct Pair
{
   int x, y;
   Pair(int a, int b): x(a), y(b)
   {
      Print(__FUNCSIG__, " ", x, " ", y);
   }
   ...
};

```
