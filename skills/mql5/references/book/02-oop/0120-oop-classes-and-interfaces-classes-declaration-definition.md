# Splitting class declaration and definition

In large software projects, it is convenient to separate classes into a brief description (declaration) and a definition, which includes the main implementation details. In some cases, such a separation becomes necessary if the classes somehow refer to each other, that is, none can be fully defined without prior declarations.

We saw an example of a forward declaration in the section [Indicators](/en/book/oop/classes_and_interfaces/classes_pointers) (see file ThisCallback.mq5), where classes Manager and Element contain reciprocal pointers. There, the class was pre-declared in a short form: in the form of a header with the keyword class and a name:

```
class Manager;

```

However, this is the shortest declaration possible. It registers only the name and makes it possible to postpone the description of the programming interface until some time, but this description must be encountered somewhere later in the code.

More often, the declaration includes a complete description of the interface: it specifies all the variables and method headers of the class but without their bodies (code blocks).

Method definitions are written separately: with headers that use fully qualified names that include the name of the class (or multiple classes and namespaces if the method context is highly nested). The names of all classes and the name of the method are concatenated using the context selection operator '::'.

```
type class_name [:: nested_class_name...] :: method_name([parameters...])
{
}

```

In theory, you can define part of the methods directly in the class description block (usually they do this with small functions), and some can be taken out separately (as a rule, large functions). But a method must have only one definition (that is, you cannot define a method in a class block, and then again separately) and one declaration (a definition in a class block is also a declaration).

The list of parameters, return type and const modifiers (if any) must match exactly in the method declaration and definition.

Let's see how we can separate the description and definition of classes from the script ThisCallback.mq5 (an example from the section [Pointers](/en/book/oop/classes_and_interfaces/classes_pointers)): let's create its analog with the name ThisCallback2.mq5.

The predeclaration Manager will still come at the beginning. Further, both classes Element and Manager are declared without implementation: instead of a block of code with a method body, there is a semicolon.

```
class Manager; // preliminary announcement
  
class Element
{
   Manager *owner; // pointer
public:
   Element(Manager &t);
   void doMath();
   string getMyName() const;
};
  
class Manager
{
   Element *elements[1]; // array of pointers (replace with dynamic)
public:
   ~Manager();
   Element *addElement();
   void progressNotify(Element *e, const float percent);
};

```

The second part of the source code contains implementations of all methods (the implementations themselves are unchanged).

```
Element::Element(Manager &t) : owner(&t)
{
}
 
void Element::doMath()
{
   ...
}
 
string Element::getMyName() const
{
   return typename(this);
}
 
Manager::~Manager()
{
   ...
}
 
Element *Manager::addElement()
{
   ...
}
 
void Manager::progressNotify(Element *e, const float percent)
{
   ...
}

```

Structures also support separate method declarations and definitions.

Note that the constructor initialization list (after the name and ':') is a part of the definition and therefore must precede the function body (in other words, the initialization list is not allowed in a constructor declaration where only the header is present).

Separate writing of the declaration and definition allows the development of [libraries](/en/book/advanced/libraries), the source code of which must be closed. In this case, the declarations are placed in a separate header file with the mqh extension, while the definitions are placed in a file of the same name with the mq5 extension. The program is compiled and distributed as an ex5 file with a header file describing the external interface.

In this case, the question may arise why part of the internal implementation, in particular the organization of data (variables), is visible in the external interface. Strictly speaking, this signals an insufficient level of abstraction in the class hierarchy. All classes that provide an external interface should not expose any implementation details.

In other words, if we set ourselves the goal of exporting the above classes from a certain library, then we would need to separate their methods into base classes that would provide a description of the API (without data fields), and Manager and Element inherit from them. At the same time, in the methods of base classes, we cannot use any data from derived classes and, by and large, they cannot have implementations at all. How is it possible?

To do this, there is a technology of abstract methods, abstract classes and interfaces.
