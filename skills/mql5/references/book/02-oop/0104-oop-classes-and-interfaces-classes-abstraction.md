# OOP fundamentals: Abstraction

We often use generalizing concepts in everyday life to convey the essence of information without going into details. For example, to answer the question "how did you get here", a person can just say "by car". And it will be clear to everyone that we are talking about a vehicle on 4 wheels, with an engine and a body for passengers. The specific brand, the color or the year of manufacture of the car does not matter to us.

When working with the program, the user also does not really care what kind of algorithm is implemented inside, as long as the program correctly performs its task. For example, sorting a list can be done in a dozen different ways.

Thus, abstraction means providing a simple programming interface that leaves hidden all the complexities and details of the implementation.

The programming interface is a set of functions that are defined in the context of a class and that perform a set of actions according to the purpose of the objects. In addition to these interface functions, there may be auxiliary, smaller functions, but they are available only inside the class. Similar to structures, there is a special name for all functions of a class: they are called methods.

The implementation, as a rule, uses variables or arrays belonging to the object (according to the class description) to store information. They are called 'fields' (this term comes from the fact that object properties are often associated in a 1:1 relationship with input fields in the user interface, or with fields in databases, where the current state of the object can be saved so that it can be restored the next time the program is launched).

Fields and methods, although described in the class, are related to a specific object: each instance has its own allocated set of variables, they have values that are independent of the state of other objects, and the methods work with the fields of their instance.

Interface and implementation must be independent. If desired, one implementation method should be easy to replace with another without any impact on the programming interface. It is also very important to design the interface based on the requirements of a particular task, and not to customize it specifically for the implementation. The class developer must be able to view their creation from two different points of view: 1) as the author of internal algorithms and data structures; 2) as a potential picky customer who uses the class as a "black box" and its control panel is the interface. It is recommended to start developing a class from thinking through the programming interface to finding and choosing the implementation methods.
