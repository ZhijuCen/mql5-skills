# Empty statement

The empty statement is the simplest in the language. It consists of only one character, the semicolon ';'

An empty statement is used in the program in those places where the syntax requires the presence of a statement, but the logic of the algorithm instructs to do nothing.

For example, the following while loop is used to find a space in a string. The whole essence of the algorithm is performed directly in the loop header, so its body must be empty. We could write an empty block of curly brackets, but an empty statement would also work here. (StmtNull.mq5).

```
int i = 0;
ushort c;
string s = "Hello, " + Symbol();
while((c = s[i++]) != ' ' && c != 0); // intentional ';' (!)
if(c == ' ')
{
   Print("Space found at: ", i);
}

```

Note that if the semicolon at the end of the while header is omitted (perhaps by accident), then the if statement will be treated as the body of the loop. As a result, there will be no output to the log by the Print function. In fact, the program will not work correctly, although without noticeable errors.

The opposite situation is also possible: an extra semicolon after the loop header (where it should not have been) will "detach" the loop body from the header, i.e. only an empty statement will be executed in the loop.

In this regard, optional semicolons should be checked in the code, and wherever they are placed intentionally, leave a comment with explanations.

By the way, from a formal point of view, the empty statement is also used in the [for](/en/book/basis/statements/statements_for) statement when we omit the initialization expression. In fact, there is always initialization:

```
for ( [initialization] ; [end loop condition]; [post-expression] )
  loop body

```

The first character ';' is part of an initialization statement, which can be an expression or an empty statement: both contain the character ';' at the end, with the latter containing nothing but ';'. Thus, optionality (emptiness) is achieved.
