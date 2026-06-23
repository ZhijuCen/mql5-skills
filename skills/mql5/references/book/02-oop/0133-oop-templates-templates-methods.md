# Method templates

Not only an object type as a whole can be a template, but its method separately — simple or static — also can be a template. The exception is virtual methods: they cannot be made templates. It follows that template methods cannot be declared inside [interfaces](/en/book/oop/classes_and_interfaces/classes_abstract_interfaces). However, interfaces themselves can be made templates, and virtual methods can be present in class templates.

When a method template is contained within a class/structure template, the parameters of both templates must be different. If there are multiple template methods, their parameters are not related in any way and may have the same name.

A method template is declared similar to a [function template](/en/book/oop/templates/templates_functions), but only in the context of a class, structure, or union (which may or may not be templates).

```
[ template < typename T ⌠, typename Ti ...] > ]
class class_name
{
   ...
   template < typename U [, typename Ui ...] >
  type method_name(parameters_with_types_T_and_U)
   {
   }
};

```

Parameters, the return value, and the method body can use types T (general for a class) and U (specific for a method).

An instance of a method for a specific combination of parameters is generated only when it is called in the program code.

In the previous section, we described the template class AutoPtr for storing and releasing a single pointer. When there are many pointers of the same type, it is convenient to put them in a container object. Let's create a simple template with similar functionality — the class SimpleArray (SimpleArray.mqh). In order not to duplicate the functionality for controlling the release of dynamic memory, we will put in the class contract that it is intended for storing values and objects, but not pointers. To store the pointers, we will place them in AutoPtr objects, and those in the container.

This has another positive effect: because the object AutoPtr is small, it is easy to copy (without overspending resources on it), which often happens when data is exchanged between functions. The objects of those application classes that AutoPtr points to can be large, and it is not even necessary to implement their own copy constructor in them.

Of course, it's cheaper to return pointers from functions, but then you need to reinvent the means of memory release control. Therefore, it is easier to use a ready-made solution in the form of AutoPtr.

For objects inside the container, we will create the data array of the templated type T.

```
template<typename T>
class SimpleArray
{
protected:
   T data[];
   ...

```

Since one of the main operations for a container is to add an element, let's provide a helper function to expand the array.

```
   int expand()
   {
      const int n = ArraySize(data);
      ArrayResize(data, n + 1);
      return n;
   }

```

We will directly add elements through the overloaded operator '<<'. It uses the generic template parameter T.

```
public:
   SimpleArray *operator<<(const T &r)
   {
      data[expand()] = (T)r;
      return &this;
   }

```

This option takes a value by reference, i.e. a variable or an object. You should pay attention to this for now, and why this is important will become clear in a couple of moments.

Reading elements is done by overloading the operator '[]' (it has the highest precedence and therefore does not require the use of parentheses in expressions).

```
   T operator[](int i) const
   {
      return data[i];
   }

```

First, let's make sure that the class works on the example of the structure.

```
struct Properties
{
   int x;
   string s;
};

```

To do this, we will describe a container for the structure in the function OnStart and place one object (TemplatesSimpleArray.mq5) into it.

```
void OnStart()
{
   SimpleArray<Properties> arrayStructs;
   Properties prop = {12345, "abc"};
   arrayStructs << prop;
   Print(arrayStructs[0].x, " ", arrayStructs[0].s);
   ...
}

```

Debug logging allows you to verify that the structure is in a container.

Now let's try to store some numbers in the container.

```
   SimpleArray<double> arrayNumbers;
   arrayNumbers << 1.0 << 2.0 << 3.0;

```

Unfortunately, we will get "parameter passed as reference, variable expected" errors, which occur exactly in the overloaded operator '<<'.

We need an overload with parameter passing by value. However, we can't just write a similar method that doesn't have const and '&':

```
   SimpleArray *operator<<(T r)
   {
      data[expand()] = (T)r;
      return &this;
   }

```

If you do this, the new variant will lead to an uncompilable template for object types: after all, objects need to be passed only by reference. Even if the function is not used for objects, it is still present in the class. Therefore, we will define the new method as a template with its own parameter.

```
template<typename T>
class SimpleArray
{
   ...
   template<typename U>
   SimpleArray *operator<<(U u)
   {
      data[expand()] = (T)u;
      return &this;
   }

```

It will appear in the class only if something by value is passed to the operator '<<', which means it is definitely not an object. True, we cannot guarantee that T and U are the same, so an explicit cast (T)u is performed. For built-in types (if the two types do not match), in some combinations, conversion with loss of precision is possible, but the code will compile for sure. The only exception is the prohibition on converting a string to a boolean type, but it is unlikely that the container will be used for the array bool, so this restriction is not significant. Those who wish can solve this problem.

With the new template method, the container SimpleArray<double> works as expected and does not conflict with SimpleArray<Properties> because the two template instances have differences in the generated source code.

Finally, let's check the container with objects AutoPtr. To do this, let's prepare a simple class Dummy that will "supply" objects for pointers inside AutoPtr.

```
class Dummy
{
   int x;
public:
   Dummy(int i) : x(i) { }
   int value() const
   {
      return x;
   }
};

```

Inside the functionOnStart, let's create a container SimpleArray<AutoPtr<Dummy>> and fill it.

```
void OnStart()
{
   SimpleArray<AutoPtr<Dummy>> arrayObjects;
   AutoPtr<Dummy> ptr = new Dummy(20);
   arrayObjects << ptr;
   arrayObjects << AutoPtr<Dummy>(new Dummy(30));
   Print(arrayObjects[0][].value());
   Print(arrayObjects[1][].value());
}

```

Recall that in AutoPtr the operator '[]' is used to return a stored pointer, so arrayObjects[0][] means: return the 0th element of the array data into SimpleArray, i.e. the object AutoPtr, and then the second pair of square brackets is applied to the volume, resulting in a pointer Dummy*. Next, we can work with all the properties of this object: in this case, we retrieve the current value of the x field.

Because Dummy does not have a copy constructor, you cannot use a container to store these objects directly without AutoPtr.

```
   // ERROR:
   // object of 'Dummy' cannot be returned,
   // copy constructor 'Dummy::Dummy(const Dummy &)' not found
   SimpleArray<Dummy> bad;

```

But a resourceful user can guess how to get around this.

```
   SimpleArray<Dummy*> bad;
   bad << new Dummy(0);

```

This code will compile and run. However, this "solution" contains a problem: SimpleArray does not know how to control pointers, and therefore, when the program exits, a memory leak is detected.

```
1 undeleted objects left
1 object of type Dummy left
24 bytes of leaked memory

```

We, as the developers of SimpleArray, have a duty to close this loophole. To do this, let's add another template method to the class with an overload of the operator '<<' – this time for pointers. Since it is a template, it is also only included in the resulting source code "on demand": when the programmer tries to use this overload, that is, write a pointer to the container. Otherwise, the method is ignored.

```
template<typename T>
class SimpleArray
{
   ...
   template<typename P>
   SimpleArray *operator<<(P *p)
   {
      data[expand()] = (T)*p;
      if(CheckPointer(p) == POINTER_DYNAMIC) delete p;
      return &this;
   }

```

This specialization throws a compilation error ("object pointer expected") when instantiating a template with a pointer type. Thus, we inform the user that this mode is not supported.

```
   SimpleArray<Dummy*> bad; // ERROR is generated in SimpleArray.mqh

```

In addition, it performs another protective action. If the client class still has a copy constructor, then saving dynamically allocated objects in the container will no longer lead to a memory leak: a copy of the object at the passed pointer P *p remains in the container, and the original is deleted. When the container is destroyed at the end of the OnStart function, its internal array data will automatically call the destructors for its elements.

```
void OnStart()
{
   ...
   SimpleArray<Dummy> good;
   good << new Dummy(0);
} // SimpleArray "cleans" its elements
 // no forgotten objects in memory

```

Method templates and "simple" methods can be defined outside of the main class block (or class template), similar to what we saw in the [Splitting Declaration and Definition of Class](/en/book/oop/classes_and_interfaces/classes_declaration_definition) section. At the same time, they are all preceded by the template header (TemplatesExtended.mq5):

```
template<typename T>
class ClassType
{
   ClassType() // private constructor
   {
      s = &this;
   }
   static ClassType *s; // object pointer (if it was created)
public:
   static ClassType *create() // creation (on first call only)
   {
      static ClassType single; //single pattern for every T
      return single;
   }
 
   static ClassType *check() // checking pointer without creating
   {
      return s;
   }
   
   template<typename U>
   void method(const U &u);
};
   
template<typename T>
template<typename U>
void ClassType::method(const U &u)
{
   Print(__FUNCSIG__, " ", typename(T), " ", typename(U));
}
   
template<typename T>
static ClassType<T> *ClassType::s = NULL;

```

It also shows the initialization of a templated static variable, denoting the singleton design pattern.

In the function OnStart, create an instance of the template and test it:

```
void OnStart()
{
   ClassType<string> *object = ClassType<string>::create();
   double d = 5.0;
   object.method(d);
   // OUTPUT:
   // void ClassType<string>::method<double>(const double&) string double
   
   Print(ClassType<string>::check()); // 1048576 (an example of an instance id)
    Print(ClassType<long>::check());   // 0 (there is no instance for T=long)
}

```
