# OOP fundamentals: Composition (design)

When designing programs using OOP, there is a problem of finding the optimal (according to some given characteristics) division into classes and relations between them. The term "composition" can be ambiguous and is often used with different meanings, including one of the special cases of "composing" classes. This digression is necessary because when reading other computer literature, you can find different interpretations of the term "compositions": both in a generalized and in a narrower sense. We will try to explain this concept, specifying the meaning of the terms in each case (when it means the general "design/project development" of the software interface, and when it means "compositional aggregation").

So, the class, as we know, consists of fields (properties) and methods. Properties, in turn, can be described by custom types, that is, they can be objects of another class. There are several ways to logically connect these objects:

- Composition (full inclusion or compositional aggregation) of objects-fields into an owner object. The relationship of such objects is described by the "whole-part" relationship, and the part cannot exist outside the whole. The owner object is said to "have a" property object, and the property object is a "part of" the owner object. The owner creates and destroys its parts. Deleting the owner removes all of its parts; the owner cannot exist without parts.
- Aggregation of objects-fields by the owner object is a "softer" inclusion. Although the relationship is also described as "whole-part", the owner only contains references to parts that can be assigned, changed, and exist in isolation from the whole. Moreover, one part can be used in several "owners".
- Association, that is, a one- or two-way connection of independent objects that has an arbitrary applied meaning; one object is said to "use" another.

Another type of relationship to keep in mind is "is a", discussed earlier in the [inheritance](/en/book/oop/classes_and_interfaces/classes_oop_inheritance) section.

An example of a full inclusion is a car and its engine. Here, a car is understood as a full-fledged means of transportation. It's not like that without a motor. And a particular engine belongs to only one car at a time. Situations when there is no engine in the car yet (at the factory) or it no longer exists (in the car repair shop) are equivalent to the fact that we broke the source code of the program.

An example of aggregation is the composition of groups of students for studies of certain courses: a group for each course includes several students, and any of them can belong to other groups (if listening to several subjects). The group "has" listeners. The exit of a student from the group does not affect the educational process of the group (the rest continue to study).

Finally, to demonstrate the idea of association, consider a computer and a printer. We can say that the computer uses the printer to print. The printer can be turned on or off as needed, and the same printer can be used from different computers. All computers and printers exist independently of each other but can be shared.

As for the characteristics that are customary to guide the design of classes, the most famous include:

- DRY (Don't repeat yourself) — instead, move common parts into parent (possibly abstract) classes.
- SRP (Single Responsibility Principle) — one class should perform one task, and if this is not the case, you need to split it into smaller ones.
- OCP (Open-Closed Principle) — "write code open for extension but closed for modification". If several calculation options are hardcoded in the X class and new ones may appear, make a base (abstract) class for a separate calculation and create specific options ("extension" of the functionality) on its basis, connected to class X without modifying it.

These are just a few of the class design best practices. After mastering the basics of OOP within the scope of this book, it may be helpful to look at other specialized sources of information on the topic, as they provide ready-made solutions for object decomposition in many common situations.
