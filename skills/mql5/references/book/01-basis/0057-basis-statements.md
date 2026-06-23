# Statements

So far, we've learned about data types, variable declarations, and their use in expressions for calculations. However, these are only small bricks in the building with which the program can be compared. Even the simplest program consists of larger blocks that allow you to group related data processing operations and control the sequence of their execution. These blocks are called statements, and we have actually already used some of them.

In particular, the declaration of a variable (or several variables) is a statement. Assigning the expression evaluation result to a variable is also a statement. Strictly speaking, the assignment operation itself is part of the expression, so it is more correct to call such a statement a statement of expression. By the way, an expression may not contain an assignment operator (for example, if it simply calls some function that does not return a value, such as Print("Hello");).

Program execution is the progressive execution of statements: from top to bottom and from left to right (if there are several statements on one line). In the simplest case, their sequence is performed linearly, one after the other. For most programs, this is not enough, so there are various control statements. They allow you to organize loops (repeating calculations) in programs and the selection of algorithm operation options depending on the conditions.

Statements are special syntactic constructions that represent the source text written according to the rules. Statements of a particular type have their own rules, but there is something in common. Statements of all types end with a ';' except for the [compound statement](/en/book/basis/statements/statements_compound). It can do without a semicolon because its beginning and end are set by a pair of curly brackets. It is important to note that thanks to the compound statement, we can include sets of statements inside other statements, building arbitrary hierarchical structures of algorithms.

In this chapter, we will get acquainted with all types of MQL5 control statements, as well as consolidate the features of declaration and expression statements.
