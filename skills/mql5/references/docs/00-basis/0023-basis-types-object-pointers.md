# Object Pointers

MQL5 enables the dynamic creation of complex type objects. This is done by using [the ‘new’ operator](/en/docs/basis/operators/newoperator)which returns a descriptor of the created object. The descriptor size is 8 bytes. Syntactically, object descriptors in MQL5 are similar to C++ pointers.

Example:

```
MyObject* hobject= new MyObject();

```

Unlike C++, the ‘hobject’ variable from the example above is not a pointer to memory, but is an object descriptor. Furthermore, in MQL5, all objects in function parameters must be passed by reference. The examples below show the passing of objects as function parameters:

```
class Foo
  {
public:
   string            m_name;
   int               m_id;
   static int        s_counter;
   //--- constructors and destructors
                     Foo(void){Setup("noname");};
                     Foo(string name){Setup(name);};
                    ~Foo(void){};
   //--- initialize the Foo object
   void              Setup(string name)
     {
      m_name=name;
      s_counter++;
      m_id=s_counter;
     }
  };
int Foo::s_counter=0;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare the object as a variable, with automatic creation
   Foo foo1;
//--- variant of passing an object by reference
   PrintObject(foo1);
 
//--- declare a pointer to an object and create it using the 'new' operator
   Foo *foo2=new Foo("foo2");
//--- variant of passing a pointer to an object by reference
   PrintObject(foo2); // the pointer to the object is converted by the compiler automatically
 
//--- declare an array of Foo objects
   Foo foo_objects[5];
//--- variant of passing an array of objects
   PrintObjectsArray(foo_objects); // a separate function for passing an array of objects
 
//--- declare an array of pointers to objects of type Foo
   Foo *foo_pointers[5];
   for(int i=0;i<5;i++)
      foo_pointers[i]=new Foo("foo_pointer");
//--- variant of passing an array of pointers
   PrintPointersArray(foo_pointers); // a separate function for passing an array of pointers
 
//--- before finishing, be sure to delete the objects created as pointers
   delete(foo2);
//--- remove the array of pointers
   int size=ArraySize(foo_pointers);
   for(int i=0;i<5;i++)
      delete(foo_pointers[i]);
//---   
  }
//+------------------------------------------------------------------+
//|  Objects are always passed by reference                          |
//+------------------------------------------------------------------+
void PrintObject(Foo &object)
  {
   Print(__FUNCTION__,": ",object.m_id," Object name=",object.m_name);
  }
//+------------------------------------------------------------------+
//| Pass an array of objects                                         |
//+------------------------------------------------------------------+
void PrintObjectsArray(Foo &objects[])
  {
   int size=ArraySize(objects);
   for(int i=0;i<size;i++)
      PrintObject(objects[i]);
  }
//+------------------------------------------------------------------+
//| Pass an array of object pointers                                 |
//+------------------------------------------------------------------+
void PrintPointersArray(Foo* &objects[])
  {
   int size=ArraySize(objects);
   for(int i=0;i<size;i++)
      PrintObject(objects[i]);
  }
//+------------------------------------------------------------------+

```

### Check the pointer before use

An attempt to access an invalid pointer causes the [critical shutdown](/en/docs/runtime/errors) of the program. The [CheckPointer](/en/docs/common/checkpointer) function is utilized to check a pointer before use. The pointer can be invalid in the following cases:

- the pointer is equal to [NULL](/en/docs/basis/types/void);
- the object was destroyed using the [delete](/en/docs/basis/operators/deleteoperator) operator.

This function can be used to validate of a pointer. A non-zero value indicates that data can be accessed at this pointer.

```
class CMyObject
 {
protected:
  double             m_value;
public:
                     CMyObject(void);
                     CMyObject(double value) {m_value=value;};
                    ~CMyObject(void){};
  //---
  double             Value(void) {return(m_value);}
 };
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
 {
//--- create a non-initialized object
  CMyObject *pointer;
  if(CheckPointer(pointer)==POINTER_INVALID)
    Print("1. pointer is ", EnumToString(CheckPointer(pointer)));
  else
    Print("1. pointer.Value()=", pointer.Value());
 
//--- initialize the pointer
  pointer=new CMyObject(M_PI);
  if(CheckPointer(pointer)==POINTER_INVALID)
    Print("2. pointer is ", EnumToString(CheckPointer(pointer)));
  else
    Print("2. pointer.Value()=", pointer.Value());
 
//--- delete the object
  delete(pointer);
  if(CheckPointer(pointer)==POINTER_INVALID)
    Print("3. pointer is ", EnumToString(CheckPointer(pointer)));
  else
    Print("3. pointer.Value()=", pointer.Value());
 }
/*
   1. pointer is POINTER_INVALID
   2. pointer.Value()=3.141592653589793
   3. pointer is POINTER_INVALID
*/

```

To quickly validate the pointer, you can also use operator "!" ([LNOT](/en/docs/basis/operations/bool)) which checks it via an implicit call of the [CheckPointer](/en/docs/common/checkpointer) function. This allows a more concise and clear code writing. Below are the checks from the previous example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
 {
//--- create a non-initialized object
  CMyObject *pointer;
  if(!pointer)
    Print("1. pointer is ", EnumToString(CheckPointer(pointer)));
  else
    Print("1. pointer.Value()=", pointer.Value());
 
//--- initialize the pointer
  pointer=new CMyObject(M_PI);
  if(!pointer)
    Print("2. pointer is ", EnumToString(CheckPointer(pointer)));
  else
    Print("2. pointer.Value()=", pointer.Value());
 
//--- delete the object
  delete(pointer);
  if(!pointer)
    Print("3. pointer is ", EnumToString(CheckPointer(pointer)));
  else
    Print("3. pointer.Value()=", pointer.Value());
 }
/*
   1. pointer is POINTER_INVALID
   2. pointer.Value()=3.141592653589793
   3. pointer is POINTER_INVALID
*/

```

Operator "==" is used for a quick check for NULL. For example: ptr==NULL or ptr!=NULL.

See also

[Variables](/en/docs/basis/variables), [Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
