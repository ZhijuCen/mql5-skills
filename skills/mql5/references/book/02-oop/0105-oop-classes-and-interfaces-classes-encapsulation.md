# OOP fundamentals: Encapsulation

To understand what encapsulation is, let's go back to reality for a moment. When we purchase a household appliance, it is usually "sealed" and under warranty. We are allowed to use it in normal modes, but the manufacturer does not encourage us to open the case and start "digging inside". For example, you can use special utilities to overclock the computer processor, but this also deprives us of the warranty, because these actions can lead to equipment failure.

It is all the same with the development of classes. Nobody should be allowed to access internal implementation, so as not to disrupt the class. This is called encapsulation, that is, including everything important in a capsule. In MQL5, as in C++, there are 3 levels of access rights. By default, the class organization is private, i.e. hidden from all its users. Only the source code of the class itself has access to the content.

Class users are also programmers. Even if you're writing a class for yourself, it makes sense to take advantage of the maximum restrictions so as not to accidentally break the class (after all, people tend to make mistakes and forget the features of their own code after a while, and programs have a tendency to grow indefinitely).

The second level of access allows the "relatives" (more precisely, the heirs; we will come back to them in a couple of paragraphs) to take a look inside.

Finally, the third level of access that you can choose is public. It is intended specifically for external programming interfaces that allow objects to be used from any part of the program for their main purpose.

Each method or field has one of three access levels, which is determined by the class developer.
