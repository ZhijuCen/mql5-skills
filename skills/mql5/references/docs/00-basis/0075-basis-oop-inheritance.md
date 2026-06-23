# Inheritance

The characteristic feature of OOP is the encouragement of code reuse through inheritance. A new class is made from the existing, which is called the base class. The derived class uses the members of the base class, but can also modify and supplement them.

Many types are variations of the existing types. It is often tedious to develop a new code for each of them. In addition, the new code implies new errors. The derived class inherits the description of the base class, thus any re-development and re-testing of code is unnecessary. The inheritance relationships are hierarchical.

Hierarchy is a method that allows to copy the elements in all their diversity and complexity. It introduces the objects classification. For example, the periodic table of elements has gases. They possess to properties inherent to all periodic elements.

Inert gases constitute the next important subclass. The hierarchy is that the inert gas, such as argon is a gas, and gas, in its turn, is part of the system. Such a hierarchy allows to interpret behaviour of inert gases easily. We know that their atoms contain protons and electrons, that is true for all other elements.

We know that they are in a gaseous state at room temperature, like all the gases. We know that no gas from inert gas subclass enters usual chemical reaction with other elements, and it is a property of all inert gases.

Consider an example of the inheritance of geometric shapes. To describe the whole variety of simple shapes (circle, triangle, rectangle, square etc.), the best way is to create a base class ([ADT](/en/docs/basis/oop#atd)), which is the ancestor of all the derived classes.

Let's create a base class CShape, which contains just the most common members describing the shape. These members describe properties that are characteristic of any shape - the type of the shape and main anchor point coordinates.

Example:

```
//--- The base class Shape
class CShape
  {
protected:
   int       m_type;                   // Shape type
   int       m_xpos;                   // X - coordinate of the base point
   int       m_ypos;                   // Y - coordinate of the base point
public:
             CShape(){m_type=0; m_xpos=0; m_ypos=0;} // constructor
   void      SetXPos(int x){m_xpos=x;} // set X
   void      SetYPos(int y){m_ypos=y;} // set Y
  };

```

Next, create new classes derived from the base class, in which we will add necessary fields, each specifying a certain class. For the Circle shape it is necessary to add a member that contains the radius value. The Square shape is characterized by the side value. Therefore, derived classes, inherited from the base class CShape will be declared as follows:

```
//--- The derived class circle
class CCircle : public CShape        // After a colon we define the base class
  {                                    // from which inheritance is made
private:
   int             m_radius;           // circle radius
 
public:
                   CCircle(){m_type=1;}// constructor, type 1 
  };

```

For the Square shape class declaration is similar:

```
//--- the derived class Square
class CSquare : public CShape        // After a colon we define the base class
  {                                    // from which inheritance is made
private:
   int            m_square_side;       // square side
 
public:
                  CSquare(){m_type=2;} // constructor, type 2 
  };

```

It should be noted that while object is created the base class constructor is called first, and then the [constructor](/en/docs/basis/types/classes#constructor) of the derived class is called. When an object is destroyed first the [destructor](/en/docs/basis/types/classes#destructor) of the derived class is called, and then a base class destructor is called.

Thus, by declaring the most general members in the base class, we can add an additional members in derived classes, which specify a particular class. Inheritance allows creating powerful code libraries that can be reused many times.

The syntax for creating a derived class from an already existing one is as follows:

```
class class_name : 
          (public | protected | private) opt  base_class_name
  {                                    
    class members declaration
  };

```

One of aspects of the derived class is the visibility (openness) of its members successors (heirs). The  public, protected and private keywords are used to indicate the extent, to which members of the base class will be available for the derived one. The public keyword after a colon in the header of a derived class indicates that the protected and public members of the base class CShape should be inherited as protected and public members of the derived class CCircle.

The private class members of the base class are not available for the derived class. The public inheritance also means that derived classes (CCircle and CSquare) are CShapes. That is, the Square (CSquare) is a shape (CShape), but the shape does not necessarily have to be a square.

The derived class is a modification of the base class, it inherits the protected and public members of the base class. The constructors and destructors of the base class cannot be inherited. In addition to members of the base class, new members are added in a derivative class.

The derived class may include the implementation of member functions, different from the base class. It has nothing common with an [overload](/en/docs/basis/oop/overload), when the meaning of the same function name may be different for different signatures.

In protected inheritance, public and protected members of base class become protected members of derived class. In private inheritance, the public and protected members of base class become private members of the derived class.

In protected and private inheritance, the relation that "the object of a derivative class is object of a base class" is not true. The protected and private inheritance types are rare, and each of them needs to be used carefully.

It should be understood that the type of inheritance (public, protected or private) does not affect the ways of accessing the members of base classes in the hierarchy of inheritance from a derived class. With any type of inheritance, only base class members declared with public and protected access specifiers will be available out of the derived classes. Let's consider it in the following example:

```
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Example class with a few access types                            |
//+------------------------------------------------------------------+
class CBaseClass
  {
private:             //--- The private member is not available from derived classes
   int               m_member;
protected:           //--- The protected method is available from the base class and its derived classes
   int               Member(){return(m_member);}
public:              //--- Class constructor is available to all members of classes
                     CBaseClass(){m_member=5;return;};
private:             //--- A private method for assigning a value to m_member
   void              Member(int value) { m_member=value;};
 
  };
//+------------------------------------------------------------------+
//| Derived class with errors                                        |
//+------------------------------------------------------------------+
class CDerived: public CBaseClass // specification of public inheritance can be omitted, since it is default
  {
public:
   void Func() // In the derived class, define a function with calls to base class members
     {
      //--- An attempt to modify a private member of the base class
      m_member=0;        // Error, the private member of the base class is not available
      Member(0);         // Error, the private method of the base class is not available in derived classes
      //--- Reading the member of the base class
      Print(m_member);   // Error, the private member of the base class is not available
      Print(Member());   // No error, protected method is available from the base class and its derived classes
     }
  };

```

In the above example, CBaseClass has only a public method – the constructor. Constructors are called automatically when creating a class object. Therefore, the private member m_member and the protected methods Member() cannot be called from the outside. But in case of public inheritance, the Member() method of the base class will be available from the derived classes.

In case of protected inheritance, all the members of the base class with public and protected access become protected. It means that if public data members and methods of the base class were accessible from the outside, with protected inheritance they are available only from the classes of the derived class and its further derivatives.

```
//+------------------------------------------------------------------+
//| Example class with a few access types                            |
//+------------------------------------------------------------------+
class CBaseMathClass
  {
private:             //--- The private member is not available from derived classes
   double            m_Pi;
public:              //--- Getting and setting a value for m_Pi
   void              SetPI(double v){m_Pi=v;return;};
   double            GetPI(){return m_Pi;};
public:              // The class constructor is available to all members
                     CBaseMathClass() {SetPI(3.14);  PrintFormat("%s",__FUNCTION__);};
  };
//+------------------------------------------------------------------+
//| Derived class, in which m_Pi cannot be modified                  |
//+------------------------------------------------------------------+
class CProtectedChildClass: protected CBaseMathClass // Protected inheritance
  {
private:
   double            m_radius;
public:              //--- Public methods in the derived class
   void              SetRadius(double r){m_radius=r; return;};
   double            GetCircleLength(){return GetPI()*m_radius;};
  };
//+------------------------------------------------------------------+
//| Script starting function                                         |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- When creating a derived class, the constructor of the base class will be called automatically
   CProtectedChildClass pt;
//--- Specify radius
   pt.SetRadius(10);
   PrintFormat("Length=%G",pt.GetCircleLength());
//--- If we uncomment the line below, we will get an error at the stage of compilation, since SetPI() is now protected
// pt.SetPI(3); 
 
//--- Now declare a variable of the base class and try to set the Pi constant equal to 10
   CBaseMathClass bc;
   bc.SetPI(10);
//--- Here is the result
   PrintFormat("bc.GetPI()=%G",bc.GetPI());
  }

```

The example shows that methods SetPI() and GetPi() in the base class CBaseMathClass are open and available for calling from any place of the program. But at the same time, for CProtectedChildClass which is derived from it these methods can be called only from the methods of the CProtectedChildClass class or its derived classes.

In case of private inheritance, all the members of the basic class with the public and protected access become private, and calling them becomes impossible in further inheritance.

MQL5 has no multiple inheritance.

### Method hiding

If a derived class defines a method with the same name as in the base class, the parent methods are hidden (in earlier versions of the MQL compiler, the descendant method was overloaded with the methods of the same name in the base class, and all of them remained available in the parent).

To call a hidden base class method, you must explicitly specify its scope when calling it:

```
class Base
  {
public:
   void Print(int x)    { ::Print("Base int: ", x); }
   void Print(double y) { ::Print("Base double: ", y); }
  };
class Derived : public Base
  {
public:
   void Print(string s) { ::Print("Derived string: ", s); }
  };
void OnStart()
  {
   Derived d;
   d.Print("text");   // call Derived::Print(string)
   d.Print(10);       // Base::Print hidden, cannot be called
   d.Base::Print(10); // explicit call of parent hidden method
  }

```

### 

### Recovering overloads with 'using'

using operator is used to return hidden overloads of the parent to the descendant scope:

```
class Base
  {
protected:
   void Print(int x)   { ::Print("Base int: ", x); }
   void Print(double y){ ::Print("Base double: ", y); }
  };
class Derived : public Base
  {
public:
   void Print(string s){ ::Print("Derived string: ", s); }
   using Base::Print;  // return all Print overloads from Base
  };
void OnStart()
  {
   Derived d;
   d.Print("text");   // Derived::Print(string)
   d.Print(42);       // Base::Print(int)
   d.Print(3.14);     // Base::Print(double)
  }

```

If using Base::Print; is removed, the d.Print(42) and d.Print(3.14) calls will be unavailable; only Derived::Print(string) will remain

Additionally, in this example, you can see that protected methods from the base class become accessible in the derived class ([protected](/en/docs/basis/oop/inheritance#protected_inheritance) is replaced with [public](/en/docs/basis/oop/inheritance#public_inheritance)).

### Accessibility and scope

[using](/en/docs/basis/oop/inheritance#using) operator not only returns base class methods to the scope of the derived class, but can also change their access level. Base class methods with the [protected](/en/docs/basis/oop/inheritance#protected_inheritance) modifier are accessible only from within the derived class methods. However, the using operator allows us to make them accessible to an external code as well — if using declaration is located in the [public](/en/docs/basis/oop/inheritance#public_inheritance) section of the derived class.

```
class Base
  {
protected:
    void Hidden() { ::Print("Base::Hidden"); }
  };
class Derived : public Base
  {
public:
    using Base::Hidden; // method becomes 'public'
  };
void OnStart()
  {
    Derived d;
    d.Hidden(); // now available
  }

```

See also

[Structures and Classes](/en/docs/basis/types/classes)
