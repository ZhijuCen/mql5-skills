# Polymorphism

Polymorphism is an opportunity for different classes of objects, related through inheritance, to respond in various ways when calling the same function element. It helps to create a universal mechanism describing the behavior of not only the base class, but also descendant classes.

Let's continue to develop a base class CShape, and define a member function GetArea(), designed to calculate the area of a shape. In all the descendant classes, produced by inheritance from the base class, we redefine this function in accordance with rules of calculating the area of a particular shape.

For a square (class CSquare), the area is calculated through its sides, for a circle (class CCircle), area is expressed through its radius etc. We can create an array to store objects of CShape type, in which both objects of a base class and those of all descendant classes can be stored. Further we can call the same function for each element of the array.

Example:

```
//--- Base class
class CShape
  {
protected: 
   int            m_type;                // Shape type
   int            m_xpos;                // X - coordinate of the base point
   int            m_ypos;                // Y - coordinate of the base point
public:
   void           CShape(){m_type=0;};   // constructor, type=0
   int            GetType(){return(m_type);};// returns type of the shape
virtual
   double         GetArea(){return (0); }// returns area of the shape
  };

```

Now, all of the derived classes have a member function getArea(), which returns a zero value. The implementation of this function in each descendant will vary.

```
//--- The derived class Circle
class CCircle : public CShape            // After a colon we define the base class
  {                                      // from which inheritance is made
private:
   double         m_radius;              // circle radius
 
public:
   void           CCircle(){m_type=1;};  // constructor, type=1 
   void           SetRadius(double r){m_radius=r;};
   virtual double GetArea(){return (3.14*m_radius*m_radius);}// circle area
  };

```

For the class Square the declaration is the same:

```
//--- The derived class Square
class CSquare : public CShape            // After a colon we define the base class
  {                                      // from which inheritance is made
private:
   double          m_square_side;        // square side
 
public:
   void            CSquare(){m_type=2;}; // constructor, type=1
   void            SetSide(double s){m_square_side=s;};
   virtual double  GetArea(){return (m_square_side*m_square_side);}// square area
  };

```

For calculating the area of the square and circle, we need the corresponding values of m_radius and m_square_side, so we have added the functions SetRadius() and SetSide() in the declaration of the corresponding class.

It is assumed that object of different types (CCircle and CSquare) derived from one base type CShape are used in our program. Polymorphism allows creating an array of objects of the base CShape class, but when declaring this array, these objects are yet unknown and their type is undefined.

The decision on what type of object will be contained in each element of the array will be taken directly during program execution. This involves the [dynamic creation](/en/docs/basis/operators/newoperator) of objects of the appropriate classes, and hence the necessity to use [object pointers](/en/docs/basis/types/object_pointers) instead of objects.

The [new](/en/docs/basis/operators/newoperator) operator is used for dynamic creation of objects. Each such object must be individually and explicitly deleted using the [delete](/en/docs/basis/operators/deleteoperator) operator. Therefore we will declare an array of pointers of CShape type, and create an object of a proper type for each element (new Class_Name), as shown in the following script example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- Declare an array of object pointers of the base type 
   CShape *shapes[5];   // An array of pointers to CShape object
 
//--- Here fill in the array with derived objects
//--- Declare a pointer to the object of CCircle type
   CCircle *circle=new CCircle();
//--- Set object properties at the circle pointer
   circle.SetRadius(2.5);
//--- Place the pointer value in shapes[0]
   shapes[0]=circle;
 
//--- Create another CCircle object and write down its pointer in shapes[1]
   circle=new CCircle();
   shapes[1]=circle;
   circle.SetRadius(5);
 
//--- Here we intentionally "forget" to set a value for shapes[2]
//circle=new CCircle();
//circle.SetRadius(10);
//shapes[2]=circle;
 
//--- Set NULL for the element that is not used
   shapes[2]=NULL;
 
//--- Create a CSquare object and write down its pointer to shapes[3]
   CSquare *square=new CSquare();
   square.SetSide(5);
   shapes[3]=square;
 
//--- Create a CSquare object and write down its pointer to shapes[4]
   square=new CSquare();
   square.SetSide(10);
   shapes[4]=square;
 
//--- We have an array of pointers, get its size
   int total=ArraySize(shapes);
//--- Pass in a loop through all pointers in the array 
   for(int i=0; i<5;i++)
     {
      //--- If the pointer at the specified index is valid
      if(CheckPointer(shapes[i])!=POINTER_INVALID)
        {
         //--- Log the type and square of the shape
         PrintFormat("The object of type %d has the square %G",
               shapes[i].GetType(),
               shapes[i].GetArea());
        }
      //--- If the pointer has type POINTER_INVALID
      else
        {
         //--- Notify of an error
         PrintFormat("Object shapes[%d] has not been initialized! Its pointer is %s",
                     i,EnumToString(CheckPointer(shapes[i])));
        }
     }
 
//--- We must delete all created dynamic objects
   for(int i=0;i<total;i++)
     {
      //--- We can delete only the objects with pointers of POINTER_DYNAMIC type
      if(CheckPointer(shapes[i])==POINTER_DYNAMIC)
        {
         //--- Notify of deletion
         PrintFormat("Deleting shapes[%d]",i);
         //--- Delete an object by its pointer
         delete shapes[i];
        }
     }
  }

```

Please note that when deleting an object using the [delete](/en/docs/basis/operators/deleteoperator) operator, [the type of its pointer](/en/docs/constants/namedconstants/enum_pointer_type) must be checked. Only objects with the [POINTER_DYNAMIC](/en/docs/constants/namedconstants/enum_pointer_type) pointer can be deleted using delete. For pointers of other type, an error will be returned.

But besides the redefining of functions during inheritance, polymorphism also includes the implementation of one and the same functions with different sets of parameters within a class. This means that the class may have several functions with the same name but with a different type and/or set of parameters. In this case, polymorphism is implemented through the [function overload](/en/docs/basis/function/functionoverload).

See also

[Standard Library](/en/docs/standardlibrary)
