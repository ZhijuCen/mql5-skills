# Constructors: default, parametric, and copying

We have already encountered constructors in the chapter on structures (see section [Constructors and destructors](/en/book/oop/structs_and_unions/structs_ctor_dtor)). For classes, they work in much the same way. Let's get back to the main points and consider further features.

A constructor is a method having the same name as the class and is of type void, meaning it does not return a value. Usually, the keyword void is omitted before the constructor name. A class can have several constructors: they must differ in the number or type of parameters. When a new object is created, the program calls the constructor so that it can set the initial values for the fields.

One of the ways to create an object that we used is the description in the code of the variable of the corresponding class. The constructor will be called on this string. It happens automatically.

Depending on the presence and types of parameters, constructors are divided into:

- default constructor: no parameters;
- copy constructor: with a single parameter which is the type of a reference to an object of the same class;
- parametric constructor: with an arbitrary set of parameters, except for a single reference for copying shown above.

Default constructor

The simplest constructor, without parameters, is called the default constructor. Unlike C++, MQL5 does not consider a default constructor to be a constructor that has parameters and all of them have default values ​​(that is, all parameters are optional, see section [Optional parameters](/en/book/basis/functions/functions_parameters_default)).

Let's define a default constructor for the class Shape.

```
class Shape
{
   ...
public:
   Shape()
   {
      ...
   }
};

```

Of course, it should be done in the public section of the class.

Constructors are sometimes deliberately made protected or private to control how objects are created, for example, through factory methods. But in this case, we are considering the standard version of class composition.

To set initial values for object variables, we could use the usual assignment statements:

```
public:
   Shape()
   {
      x = 0;
      y = 0;
      ...
   }

```

However, the constructor syntax provides another option. It is called the initialization list and is written after the function header, separated by a colon. The list itself is a comma-separated sequence of field names, with the desired initial value in parentheses to the right of each name.

For example, for the constructor Shape it can be written as follows:

```
public:
   Shape() :
      x(0), y(0),
      backgroundColor(clrNONE)
   {
   }

```

This syntax is preferred over assigning variables in the body of a constructor for several reasons.

First, the assignment in the function body is made after the corresponding variable has been created. Depending on the type of the variable, this may mean that the default constructor was first called for it and then the new value was overwritten (and this means extra expenses). In the case of an initialization list, the variable is immediately created with the desired value. It is likely that the compiler will be able to optimize the assignment in the absence of an initialization list, but in the general case, this is not guaranteed.

Secondly, some class fields can be declared with the const modifier. Then they can only be set in the initialization list.

Thirdly, field variables of user-defined types may not have a default constructor (that is, all available constructors in their class have parameters). This means that when you create a variable, you need to pass actual parameters to it, and the initialization list allows you to do this: the argument values are specified inside parentheses, as if in an explicit constructor call. An initialization list can be used in constructor definitions, but not in other methods.

Parametric constructor

A parametric constructor, by definition, has multiple parameters (one or more).

For example, imagine that for coordinates x and y a special structure with a parametric constructor is described:

```
struct Pair
{
   int x, y;
   Pair(int a, int b): x(a), y(b) { }
};

```

Then we can use the coordinates field of the new type Pair instead of the two integer fields x and y in the Shape class. This construction of objects is called inclusion or compositional aggregation. The Pair object is an integral part of the object Shape. A coordinate pair is automatically created and destroyed along with the "host" object.

Because Pair does not have a parameterless constructor, the coordinates field must be specified in the initialization list of the Shape constructor, with two parameters (int, int):

```
class Shape
{
protected:
   // int x, y;
   Pair coordinates;  // center coordinates (object inclusion)
   ...
public:
   Shape() :
      // x(0), y(0),
      coordinates(0, 0), //object initialization
      backgroundColor(clrNONE) 
   {
   }
};

```

Without an initialization list, such automatic objects cannot be created.

Given the change in how coordinates are stored in the object, we need to update the toStringmethod:

```
   string toString() const
   {
      return (string)coordinates.x + " " + (string)coordinates.y;
   }

```

But this is not the final version: we will make some more changes soon.

Recall that automatic variables were described in the [Declaration/Definition Instructions](/en/book/basis/statements/statements_declaration) section. They are called automatic because the compiler creates them (allocates memory) automatically, and also automatically deletes them when program execution leaves the context (block of code) in which the variable was created.  

   

In the case of object variables, automatic creation means not only memory allocation but also a constructor call. The automatic deletion of an object is accompanied by a call to its destructor (see below section [Destructors](/en/book/oop/classes_and_interfaces/classes_dtors)). Moreover, if the object is part of another object, then its lifetime coincides with the lifetime of its "owner", as in the case of the field coordinates – an instance of Pair in the object Shape.  

   

Static (including global) objects are also managed automatically by the compiler.  

   

An alternative to automatic allocation is [dynamic object creation and manipulation via pointers](/en/book/oop/classes_and_interfaces/classes_new_delete_pointers).

In the [inheritance](/en/book/oop/classes_and_interfaces/classes_inheritance) section, we will learn how one class can be inherited from another. In this case, the initialization list is the only way to call the parametric constructor of the base class (the compiler is not able to automatically generate a constructor call with parameters, as it does implicitly for the default constructor).

Let's add another constructor to the class Shape that allows you to set specific values ​​to variables. It will just be a parametric constructor (you can create as many of them as you like: for different purposes and with a different set of parameters).

```
   Shape(int px, int py, color back) :
      coordinates(px, py),
      backgroundColor(back)
   {
   }

```

The initialization list ensures that when the body of the constructor is executed, all internal fields (including nested objects, if any) have already been created and initialized.

The order of initialization of class members does not correspond to the initialization list but to the sequence of their declaration in the class.

If a constructor with parameters is declared in a class, and it is required to allow the creation of objects without arguments, the programmer must explicitly implement the default constructor

In the event that there are no constructors at all in the class, the compiler implicitly provides a default constructor in the form of a stub, which is responsible for initializing fields of the following types: strings, dynamic arrays, and automatic objects with a default constructor. If there are no such fields, the implicit default constructor does nothing. Fields of other types are not affected by the implicit constructor, so they will contain random "garbage". To avoid this, the programmer must explicitly declare the constructor and set the initial values.

Copy constructor

The copy constructor allows you to create an object based on another object passed by reference as the only parameter.

For example, for the class Shape, the copy constructor might look like this:

```
class Shape
{
   ...
   Shape(const Shape &source) :
      coordinates(source.coordinates.x, source.coordinates.y),
      backgroundColor(source.backgroundColor)
   {
   }
   ...
};

```

Note that protected and private members of another object are available in the current object because permissions work at the class level. In other words, two objects of the same class can access each other's data when given a reference (or [pointer](/en/book/oop/classes_and_interfaces/classes_new_delete_pointers)).

If there is such a constructor, you can create objects using one of two syntax types:

```
void OnStart()
{
   Shape s;
   ...
   Shape s2(s);   // ok: syntax 1 - copying
   Shape s3 = s;  // ok: syntax 2 - copying via initialization
                  //                   (if there is copy constructor)
                  //                 - or assignment
                  //                   (if there is no copy constructor,
                  //                    but there is default constructor)
   
   Shape s4;      // definition
   s4 = s;        // assignment, not copy constructor!
}

```

It is necessary to distinguish between initialization of an object during creation and assignment.

The second option (marked with the "syntax 2" comment) will work even if there is no copy constructor, but there is a default constructor. In this case, the compiler will generate less efficient code: first, using the default constructor, it will create an empty instance of the receiving variable (s3, in this case), and then copy the fields of the sample (s, in this case) element by element. In fact, the same case will turn out as with the variable s4, for which the definition and assignment are performed by separate statements.

If there is no copy constructor, then attempting to use the first syntax will result in a "parameter conversion not allowed" error, as the compiler will try to take some other constructor available with a different set of parameters.

Keep in mind that if the class has fields with the modifier const, assigning such objects is prohibited for obvious reasons: a constant field cannot be changed, it can only be set once when creating an object. Therefore, the copy constructor becomes the only way to duplicate an object.

In particular, in the following sections, we will complete our Shape1.mq5 example, and the following field will appear in the Shape class (with a description string type). Then the assignment operator will generate errors (in particular, for such lines as with the variable s4):

```
attempting to reference deleted function
   'void Shape::operator=(const Shape&)'
function 'void Shape::operator=(const Shape&)' was implicitly deleted
   because member 'type' has 'const' modifier

```

Thanks to the detailed wording of the compiler, you can understand the essence and reasons for what is happening: first, the assignment operator ('=') is mentioned, and not the copy constructor; second, it is reported that the assignment operator was implicitly removed due to the presence of the modifier const. Here we encounter concepts that are yet unknown, which we will study later: [operator overloading in classes](/en/book/oop/classes_and_interfaces/classes_operator_overloading), [object type conversion](/en/book/oop/classes_and_interfaces/classes_dynamic_cast_void), and the ability to mark methods as [deleted](/en/book/oop/classes_and_interfaces/classes_final_delete).

In the section [Inheritance](/en/book/oop/classes_and_interfaces/classes_inheritance), after we learn how to describe derived classes, we need to make some clarifications about copy constructors in class hierarchies.
