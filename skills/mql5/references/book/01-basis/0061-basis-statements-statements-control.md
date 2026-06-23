# Overview of control statements

Control statements are designed to organize the non-linear execution of other statements, including declarations, expressions, and nested control statements. They can be divided into 3 types:

- repetition statements, or loops
- conditional statements for choosing one of several branches of alternative actions
- jump statements that change, if necessary, the standard behavior of the first two types of statements

Repeat and select statements consist of a header (each with a different syntax) followed by a controlled statement. If a managed part needs to specify multiple statements, it uses a compound statement. This feature is not available for jump statements. They only move the internal pointer, based on which the program determines which statement is currently to be executed, according to special rules, which we will discuss in the following sections.

In the simplest case, without control statements, the statements are executed sequentially, one after the other, as they are written in the code block (in particular, in the body of the main function OnStart for scripts). If an expression with a call to another function is encountered in a code block, the program, according to the same linear principle, begins to execute statements inside the called function, and when they are all executed, it will return to the calling code block, and execution will continue on the next statement after the function call. Control statements can significantly change this logic of work.

You can use selection inside loops or vice versa, and the nesting level is unlimited. However, too much nesting makes the program difficult to understand for the programmer. Therefore, it is recommended to allocate (transfer) code blocks into functions (one or several): inside each function, it makes sense to maintain a nesting level of no more than 2-3.

The following repetition statements are supported in MQL5:

- for loop
- while loop
- do loop

All loops allow one or more statements to be executed a given number of times or until some boolean condition is met. Executing the contents of a loop once is called an iteration. As a rule, arrays are processed in loops or periodic repeating actions are performed (usually in [scripts](/en/book/applications/script_service/scripts) or [services](/en/book/applications/script_service/services)).

Conditional statements include:

- selection with if
- selection with switch

The former allows you to specify one or more conditions, depending on the truth or falsity of which the options assigned to them (one or more statements) will be executed. The latter evaluates an expression of an integer type and selects one of several alternatives based on its value.

Finally, jump statements are:

- break
- continue
- return

Later we will consider each of them in detail.

Unlike C++, MQL5 does not have a go to statement.
