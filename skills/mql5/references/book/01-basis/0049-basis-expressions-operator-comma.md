# Comma

Operator comma that is explicitly denoted as ',' is placed between two expressions computed independently from left to right. In other words, this operator does not perform any actions itself but just allows specifying the sequence of two or more expressions within a statement.

Expressions placed right-hand in the sequence can use the results of computing the left-hand expressions, since they have already been processed.

The operator result is the result of the rightmost expression. The operator has the lowest priority.

Currently, using the operator in MQL5 is limited by the header of the [for statement](/en/book/basis/statements/statements_for).

Example:

```
for(i=0,j=99; i<100; i++,j--) 
   Print(array[i][j]);

```

Let's repeat the key aspects of the comma operator in MQL5:

Order of evaluation:

- Expressions are processed from left to right. Thus, the expressions on the right can use the results of the expressions on the left since they have already been processed.

Result and priority:

- The result of the comma operator is the value of the rightmost expression. It's important to note that the comma operator has the lowest priority, meaning that other operators in the expression may have higher priorities.
