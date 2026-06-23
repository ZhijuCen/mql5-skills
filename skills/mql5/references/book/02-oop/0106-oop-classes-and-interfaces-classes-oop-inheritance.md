# OOP fundamentals: Inheritance

When building large and complex projects, people seek ways to make the process more efficient. One of the popular ways is leveraging existing developments. For example, it is much easier to develop a building plan not from scratch but based on the previous blueprints.

Code reuse in programming is also very popular. We already know one such technique: isolating a piece of code into a function and then calling it from different places where the corresponding functionality is required. But OOP provides a more powerful mechanism: when developing a new class, it can inherit from another, acquiring all the internal structure and external interface, requiring only minimum adjustment to suit the purpose. Thus, starting from the parent class, you can quickly "grow" a derived class with additional or refined abilities. Also, any subsequent changes to the parent class (such as enhancements or bug fixes) will automatically affect all child classes.

When a class is the parent of another, it is referred to as the base class. In turn, the class that is inherited from the base class is called derived.

Of course, the chain of inheritance (or rather, the family tree) can be continued: each class can have several heirs, those, in turn, have their heirs, and so on. The only thing that inheritance rules do not allow is cycles in kinship relationships, for example, a grandson cannot be the parent of its grandfather.

The relationship between any class and its descendant of any generation is described by the word "is a", that is, the descendant is able to act as an ancestor, but not vice versa. This is because the derived object actually contains the data model of the ancestor and supplements it with new fields and behavior.

By inheriting classes from each other, we get the opportunity to process related objects in a unified way, as some of their functions are common.

For example, a hypothetical drawing program can be used to implement several types of shapes, including circles, squares, triangles, and so on. Each object has coordinates on the screen (for simplicity, we will assume that a pair of X and Y values of the shape center is specified). In addition, each shape is rendered using its own background color, border color, and border thickness.

This means that we can implement functions for setting the coordinates and setting the drawing style only once in the parent class describing the abstract shape, and these functions will be automatically inherited by all the descendants.

Moreover, in order to simplify the source code, it is desirable to somehow unify not only the settings but also the drawing of different shapes. This phrase contains some kind of contradiction: since the shapes are different, and each must be displayed in its own way, what kind of unification are we talking about? We're talking about a unified software interface. Indeed, according to the concept of abstraction, it is necessary to separate the external interface from the internal implementation. And the display of specific shapes is essentially an implementation detail.

A unified interface and different implementations for shape types smoothly lead us to the next concept — polymorphism.
