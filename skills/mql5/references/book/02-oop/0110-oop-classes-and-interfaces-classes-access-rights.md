# Access rights

A special syntax is provided for editing access to class members (we already met it in the chapter on structures). Anywhere in the block, before the description of class members, you can insert a modifier: one of the three keywords – private, protected, public – and a colon sign.

All members following the modifier, until another modifier is encountered, or up to the end of the class, will receive the corresponding visibility constraint.

For example, the following entry is identical to the previous description of the class Shape, because the mode private is assumed for classes without modifiers:

```
class Shape
{
private:
   int x, y;              // center coordinates
   color backgroundColor; // fill color
   ...
};

```

If we wanted to open access to all fields, we would change the modifier to public

```
class Shape
{
public:
   int x, y;              // center coordinates
   ...
};

```

But that would violate the principle of encapsulation, and we won't do that. Instead, we insert the modifier protected: it allows access to members from derived classes while leaving them hidden from the outside world. We are planning to extend the class Shape to several other shape classes that will need access to the parent's variables.

```
class Shape
{
protected:
   int x, y;              // center coordinates
   color backgroundColor; // fill color
   
public:
   string toString() const
   {
      return (string)x + " " + (string)y;
   }
   
   void draw() { /* shape drawing interface stub */ }
};

```

Along the way, we made both functions public.

Modifiers can be interleaved in the class description in an arbitrary way and repeated many times. However, in order to improve the readability of the code, it is recommended to make one section of public, protected, and private members, and withstand the same order in all classes of the project.

Note that we added the keyword const to the end of the header of the toString function. It means that the function does not change the state of the object fields. Although not required, it helps prevent accidental corruption of variables and also lets users of the class and the compiler know that calling the function will not result in any side effects.

In the toString function, as in any class method, the fields are accessible by their names. Later, we'll see how to declare [methods as static](/en/book/oop/classes_and_interfaces/classes_static): they are related entirely to the class, not to object instances, and therefore fields cannot be accessed.

Now we can call the method toString from the object variable s:

```
void OnStart()
{
   Shape s;
   Print(s.toString());
}

```

Here we see the use of the dot character '.' as a special dereference operator: it provides access to the members of the object — fields and methods. To the left of it should be an object, and to the right — the identifier of one of the available properties.

The method toString is public, and therefore accessible from an external to the class function OnStart. If we tried in OnStart to "reach out" to the fields s.x or s.y through dereference, we would get a compilation error "cannot access protected member declared in class 'Shape'".

For C++ professionals, we note that MQL5 does not support so-called "friends" (for the rest, let's explain that in C++ it is possible, if necessary, to make a kind of "whitelist" of third-party classes and methods that have extended rights, although they are not "relatives").

When we run the program, we will see that it outputs a couple of numbers. However, the coordinate values will be random. Even if you are lucky enough to see nulls, it does not guarantee that they will appear the next time you run the script. As a rule, if the list of executing MQL programs does not change in the terminal, repeated launches of any script result in the allocation of the same memory area to it, which may give the deceptive impression that the state of the object is stable. In fact, the fields of an object, as in the case of local variables, are not initialized with anything by default (see section [Initialization](/en/book/basis/variables/initialization)).

To initialize them, special class functions, constructors, are used.
