# Classes and interfaces

Classes are the main building block in the program development based on the OOP approach. In a global sense, the term class refers to a collection of something (things, people, formulas, etc.) that have some common characteristics. In the context of OOP, this logic is preserved: one class generates objects that have the same set of properties and behavior.

In the previous chapters of this book, we familiarized ourselves with the built-in MQL5 types such as double, int or string. The compiler knows how to store values of these types and what operations can be performed on them. However, these types may not be very convenient to use when describing any application area. For example, a trader has to work with such entities as a trading strategy, a signal filter, a currency basket, and a portfolio of open positions. Each of them consists of a whole set of related properties, subject to specific processing and consistency rules.

A program to automate actions with these objects could consist only of built-in types and simple functions, but then you would have to come up with tricky ways to store and link properties. This is where the OOP technology comes to the rescue, providing ready-made, unified, and intuitive mechanisms for this.

OOP proposes to write all the instructions for storing properties, filling them correctly, and performing permitted operations on objects of a particular user-defined type in a single container with source code. It combines variables and functions in a certain way. Containers are divided into classes, structures, and associations if you list them in descending order of capabilities and relevance.

We have already had an encounter with structures and associations in the [previous chapter](/en/book/oop/structs_and_unions). This knowledge will be useful for classes as well, but classes provide more tools from the OOP arsenal.

By analogy with a structure, a class is a description of a user-defined type with an arbitrary internal storage method and rules for working with it. Based on it, the program can create instances of this class, the objects that should be considered composite variables.

All user-defined types share some of the basic concepts that you might call OOP theory, but they are especially relevant for classes. These include:

- abstraction
- encapsulation
- inheritance
- polymorphism
- composition (design)

Despite the tricky names, they indicate quite simple and familiar norms of the real world, transferred to the world of programming. We'll start our dive into OOP by looking at these concepts. As for the syntax for describing classes and how to create objects — we will discuss it later.
