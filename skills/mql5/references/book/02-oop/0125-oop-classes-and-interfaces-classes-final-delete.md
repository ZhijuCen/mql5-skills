# Inheritance management: final and delete

MQL5 allows you to impose some restrictions on the inheritance of classes and structures.

Keyword final

By using the final keyword added after the class name, the developer can disable inheritance from that class. For example (FinalDelete.mq5):

```
class Base
{
};
 
class Derived final : public Base
{
};
 
class Concrete : public Derived // ERROR
{
};

```

The compiler will throw the error "cannot inherit from 'Derived' as it has been declared as 'final'".

Unfortunately, there is no consensus on the benefits and scenarios for using such a restriction. The keyword lets users of the class know that its author, for one reason or another, does not recommend taking it as the base one (for example, its current implementation is draft and will change a lot, which may cause potential legacy projects to stop compiling).

Some people try to encourage the design of programs in this way, in which the inclusion of objects ([composition](/en/book/oop/classes_and_interfaces/classes_composition)) is used instead of inheritance. Excessive passion for inheritance can indeed increase the class cohesion (that is, mutual influence), since all heirs in one way or another can change parent data or methods (in particular, by redefining virtual functions). As a result, the complexity of the working logic of the program and the likelihood of unforeseen side effects increase.

An additional advantage of using final can be code optimization by the compiler: for pointers of "final" types, it can replace the dynamic dispatch of virtual functions with a static one.

Keyword delete

The delete keyword can be specified in the header of a method to make it inaccessible in the current class and its descendants. Virtual methods of parent classes cannot be deleted in this way (this would violate the "contract" of the class, that is, the heirs would cease to "be" ("is a") representatives of the same kind).

```
class Base
{
public:
   void method() { Print(__FUNCSIG__); }
};
 
class Derived : public Base
{
public:
   void method() = delete;
};
 
void OnStart()
{
   Base *b;
   Derived d;
   
   b = &d;
   b.method();
   
   // ERROR:   
   // attempting to reference deleted function 'void Derived::method()'
   //    function 'void Derived::method()' was explicitly deleted
   d.method();
}

```

An attempt to call it will result in a compilation error.

We saw a similar error in the [Object type casting](/en/book/oop/classes_and_interfaces/classes_dynamic_cast_void) section because the compiler has some intelligence to also "remove" methods under certain conditions.

It is recommended to mark as deleted the following methods for which the compiler provides implicit implementations:

- default constructor: Class(void) = delete;
- copy constructor: Class(const Class &object) = delete;
- copy/assign operator: void operator=(const Class &object) = delete.

If you require any of these, you must define them explicitly. Otherwise, it is considered good practice to abandon the implicit implementation. The thing is that the implicit implementation is quite straightforward and can give rise to problems that are difficult to localize, in particular, when casting object types.
