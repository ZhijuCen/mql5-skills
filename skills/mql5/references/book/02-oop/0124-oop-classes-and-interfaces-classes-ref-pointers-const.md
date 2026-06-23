# Pointers, references, and const

After learning about built-in and object types, and the concepts of [reference](/en/book/basis/functions/functions_ref_value) and [pointer](/en/book/oop/classes_and_interfaces/classes_pointers), it probably makes sense to do a comparison of all available type modifications.

References in MQL5 are used only when describing parameters of functions and methods. Moreover, object type parameters must be passed by reference.

```
void function(ClassOrStruct &object) { }          // OK
void function(ClassOrStruct object) { }           // wrong
void function(double &value) { }                  // OK
void function(double value) { }                   // OK

```

Here ClassOrStruct is the name of the class or structure.

It is allowed to pass only variables (LValue) as an argument for a reference type parameter, but not constants or temporary values obtained as a result of expression evaluation.

You cannot create a variable of a reference type or return a reference from a function.

```
ClassOrStruct &function(void) { return Class(); } // wrong
ClassOrStruct &object;                            // wrong
double &value;                                    // wrong

```

Pointers in MQL5 are available only for class objects. Pointers to variables of built-in types or structures are not supported.

You can declare a variable or function parameter of type a pointer to an object, and also return a pointer to an object from the function.

```
ClassOrStruct *pointer;                                   // OK
void function(ClassOrStruct *object) { }                  // OK
ClassOrStruct *function() { return new ClassOrStruct(); } // OK

```

However, you cannot return a pointer to a local automatic object, because the latter will be freed when the function exits, and the pointer will become invalid.

If the function returned a pointer to an object dynamically allocated within the function with new, then the calling code must "remember" to free the pointer with delete.

A pointer, unlike a reference, can be NULL. Pointer parameters can have a default value, but references can't ("reference cannot be initialized" error).

```
void function(ClassOrStruct *object = NULL) { }          // OK
void function(ClassOrStruct &object = NULL) { }          // wrong

```

Links and pointers can be combined in a parameter description. So a function can take a reference to a pointer: and then changes to the pointer in the function will become available in the calling code. In particular, the factory function, which is responsible for creating objects, can be implemented in this way.

```
void createObject(ClassName *&ref)
{
   ref = new ClassName();
   // further customization of ref
   ...
}

```

True, to return a single pointer from a function, it is usually customary to use the return statement, so this example is somewhat artificial. However, in those cases when it is necessary to pass an array of pointers outside, a reference to it in the parameter becomes the preferred option. For example, in some classes of the standard library for working with container classes of the map type with [key, value] pairs (MQL5/Include/Generic/SortedMap.mqh, MQL5/Include/Generic/HashMap.mqh) there are methods CopyTo for getting arrays with elements CKeyValuePair.

```
int CopyTo(CKeyValuePair<TKey,TValue> *&dst_array[], const int dst_start = 0);

```

The parameter type dst_array may seem unfamiliar: it's a class template. We will learn about templates in the [next chapter](/en/book/oop/templates). Here, for now, the only important thing for us is that this is a reference to an array of pointers.

The const modifier imposes special behavior for all types. In relation to built-in types, it was discussed in the section on [Constant variables](/en/book/basis/variables/const_variables). Object types have their own characteristics.

If a variable or function parameter is declared as a pointer or a reference to an object (a reference is only in the case of a parameter), then the presence of the modifier const on them limits the set of methods and properties that can be accessed to only those that also have the modifier const. In other words, only constant properties are accessible through constant references and pointers.

When you try to call a non-const method or change a non-const field, the compiler will generate an error: "call non-const method for constant object" or "constant cannot be modified".

A non-const pointer parameter can take any argument (constant or non-constant).

It should be borne in mind that two modifiers const can be set in the pointer description: one will refer to the object, and the second to the pointer:

- Class *pointer is a pointer to an object; the object and the pointer work without limitations;
- const Class *pointer is a pointer to a const object; for the object, only constant methods and reading properties are available, but the pointer can be changed (assigned to it the address of another object);
- const Class * const pointer is a const pointer to a const object; for the object, only const methods and reading properties are available; the pointer cannot be changed;
- Class * const pointer is a const pointer to an object; the pointer cannot be changed, but the properties of the object can be changed.

Consider the following class Counter (CounterConstPtr.mq5) as an example.

```
class Counter
{
public:
   int counter;
   
   Counter(const int n = 0) : counter(n) { }
   
   void increment()
   {
      ++counter;
   }
   
   Counter *clone() const
   {
      return new Counter(counter);
   }
};

```

It artificially made the public variable counter. The class also has two methods, one of which is constant (clone), and the second is not (increment). Recall that a constant method does not have the right to change the fields of an object.

The following function with the Counter *ptr type parameter can call all methods of the class and change its fields.

```
void functionVolatile(Counter *ptr)
{
   // OK: everything is available
   ptr.increment();
   ptr.counter += 2;
   //remove the clone immediately so that there is no memory leak
   // the clone is only needed to demonstrate calling a constant method 
   delete ptr.clone(); 
   ptr = NULL;
}

```

The following function with the parameter const Counter *ptr will throw a couple of errors.

```
void functionConst(const Counter *ptr)
{
   // ERRORS:
   ptr.increment(); // calling non-const method for constant object
   ptr.counter = 1; // constant cannot be modified
   
   // OK: only const methods are available, fields can be read
   Print(ptr.counter); // reading a const object
   Counter *clone = ptr.clone(); // calling a const method
   ptr = clone;     // changing a non-const pointer ptr
   delete ptr;      // cleaning memory
}

```

Finally, the following function with the parameter const Counter * const ptr does even less.

```
void functionConstConst(const Counter * const ptr)
{
   // OK: only const methods are available, the pointer ptr cannot be changed
   Print(ptr.counter); // reading a const object
   delete ptr.clone(); // calling a const method
   
   Counter local(0);
   // ERRORS:
   ptr.increment(); // calling non-const method for constant object
   ptr.counter = 1; // constant cannot be modified
   ptr = &local;    // constant cannot be modified
}

```

In the function OnStart, where we have declared two Counter objects (one is constant and the other is not), you can call these functions with some exceptions:

```
void OnStart()
{
   Counter counter;
   const Counter constCounter;
   
   counter.increment();
   
   // ERROR:
   // constCounter.increment(); // call non-const method for constant object
   Counter *ptr = (Counter *)&constCounter; // trick: type casting without const
   ptr.increment();
   
   functionVolatile(&counter);
   
   // ERROR: cannot convert from a const pointer...
   // functionVolatile(&constCounter); // to a non-const pointer
   
   functionVolatile((Counter *)&constCounter); // type casting without const
   
   functionConst(&counter);
   functionConst(&constCounter);
   
   functionConstConst(&counter);
   functionConstConst(&constCounter);
}

```

First, note that variables also generate an error when trying to call a const method increment on a non-const object.

Secondly, constCounter cannot be passed to the functionVolatile function — we get the error "cannot convert from const pointer to nonconst pointer".

However, both errors can be circumvented by explicit type casting without the const modifier. Although this is not recommended.
