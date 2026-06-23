# OOP fundamentals: Polymorphism

The term polymorphism means variability or diversity. This is the inverse of abstraction combined with the inheritance mechanism. When we have a common programming interface, it can be implemented by different classes which are linked by relations of inheritance. Then calling interface methods will cause the task to be performed in different ways.

For example, imagine a family of abstract vehicles that includes a couple of certain types: a car and a helicopter. The command to move from point A to point B will be executed by them equally well, but the car will make its way on the ground, and the helicopter in the air.

Let's continue the example with the drawing program. We can say that the diversity in it is laid down at the level of graphic shapes. The user is free to draw any combination of circles, squares, and triangles. Each of these objects must be able to display itself on the screen using its own coordinates and its own style, but the most important thing is to do it in a way that produces an appropriate form.

The program will most likely have an array (or another container) that stores all the shapes created by the user, and displaying the entire drawing on the screen should consist in sequentially drawing each shape. If we reduce drawing instructions for shapes into a separate method (let's call it draw), then each class will have its own implementation. However, the headers of these functions will be completely identical, since they perform the same task, and take the initial data from the objects.

Therefore, we have the opportunity to unify the source code, since the same call to draw inside the loop over shapes exhibits polymorphism: the displayed shape will depend on the type of object.
