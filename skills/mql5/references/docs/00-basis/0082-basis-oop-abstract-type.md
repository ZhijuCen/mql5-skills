# Abstract Classes and Pure Virtual Functions

Abstract classes are used for creating generic entities, that you expect to use for creating more specific derived classes. An abstract class can only be used as the base class for some other class, that is why it is impossible to create an object of the abstract class type.

A class which contains at least one pure virtual function in it is abstract. Therefore, classes derived from the abstract class must implement all its pure virtual functions, otherwise they will also be abstract classes.

A virtual function is declared as "pure" by using the pure-specifier syntax. Consider the example of the CAnimal class, which is only created to provide common functions – the objects of the CAnimal type are too general for practical use. Thus, CAnimal is a good example for an abstract class:

```
class CAnimal
  {
public:
                      CAnimal();     // Constructor
   virtual void       Sound() = 0;   // A pure virtual function
private:
   double             m_legs_count;  // The number of the animal's legs
  };

```

Here Sound() is a pure virtual function, because it is declared with the specifier of the pure virtual function PURE (=0).

Pure virtual functions are only the virtual functions for which the PURE specifier is set: (=NULL) or (=0). Example of abstract class declaration and use:

```
class CAnimal
  {
public:
   virtual void       Sound()=NULL;   // PURE method, should be overridden in the derived class, CAnimal is now abstract and cannot be created
  };
//--- Derived from an abstract class
class CCat : public CAnimal
 {
public:
  virtual void        Sound() { Print("Myau"); } // PURE is overridden, CCat is not abstract and can be created
 };
 
//--- Examples of wrong use
new CAnimal;         // Error of 'CAnimal' - the compiler returns the "cannot instantiate abstract class" error
CAnimal some_animal; // Error of 'CAnimal' - the compiler returns the "cannot instantiate abstract class" error
 
//--- Examples of proper use
new CCat;  // No error - the CCat class is not abstract
CCat cat;  // No error - the CCat class is not abstract

```

## Restrictions on abstract classes

If the constructor for an abstract class calls a pure virtual function (either directly or indirectly), the result is undefined.

```
//+------------------------------------------------------------------+
//| An abstract base class                                           |
//+------------------------------------------------------------------+
class CAnimal
  {
public:
   //--- A pure virtual function
   virtual void      Sound(void)=NULL;
   //--- Function
   void              CallSound(void) { Sound(); }
   //--- Constructor
   CAnimal()
    {
     //--- An explicit call of the virtual method
     Sound();
     //--- An implicit call (using a third function)
     CallSound();
     //--- A constructor and/or destructor always calls its own functions,
     //--- even if they are virtual and overridden by a called function in a derived class
     //--- If the called function is pure virtual,
     //--- its call will cause a critical runtime error: "pure virtual function call"
    }
  };

```

However, constructors and destructors for abstract classes can call other member functions.
