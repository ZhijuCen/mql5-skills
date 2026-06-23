# Compound statements (blocks of code)

A compound statement is a generic container for other statements enclosed in curly brackets '{' and '}'. Such a block of code can be used to define the body of a function, after the header of other control statements if they require more than one controlled statement, or simply as a nested block on its own within the body of a function or other statement. This allows you to create a local, limited scope for variables. We already talked about this in the section [Context, scope, and lifetime of variables](/en/book/basis/variables/scope_and_lifetime).

In a generalized form, a compound statement can be described as follows:

```
{
[statements]
}

```

In such a schematic description, any fragment enclosed in semicircular brackets and with the superscripted opt indicates that it is optional. In this case, there may not be any nested statements inside the block.

In the following sections, we will see how compound statements are used in combination with other kinds of statements and what they can contain.

There is one nuance that is worth emphasizing: after the description of the compound statement, the semicolon ';' is not required. This distinguishes it from all other statements.
