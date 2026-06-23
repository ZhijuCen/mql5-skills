# Overview of macro substitution directives

Macro substitution directives include two forms of the #define directive:

- simple, usually to define a constant
- defining a macro as a pseudo-function with parameters

In addition, there is a #undef directive to undo any of the previous #define definitions. If #undef is not used, each defined macro is valid until the end of source compilation.

Macros are registered and then used in code by name, following the rules of identifiers. By convention, macro names are written in capital letters. Macro names can overlap the names of variables, functions, and other elements of the source code. Purposeful use of this fact allows the flexibility to change and generate source code on the fly. However, an unintentional coincidence of a macro name with a program element will result in errors.

The principle of operation of both forms of macro substitutions is the same. Using the #define directive, an identifier is introduced, which is associated with a certain piece of text — a definition. If the preprocessor finds a given identifier later in the source code, it replaces it with the text associated with it. We emphasize that the macro name can be used in compiled code only after registration (this is similar to the variable declaration principles, but only at the compilation stage).

Replacing a macro name with its definition is called expansion. The analysis of the source code occurs progressively and by one line in a pass, but the expansion in each line can be performed an arbitrary number of times, as in a loop, as long as macro names are found in the result. You cannot include the same name in a macro definition: when substituting, such a macro will result in an "unknown identifier" error.

In Part 3 of the book, we'll learn about [templates](/en/book/oop/templates), which also allow you to generate (or, in fact, replicate) source code, but with different rules. If there are both, macro substitution directives and templates in the source code, the macros are expanded first, and then the code is generated from the templates.

Macro names are highlighted in red in MetaEditor.
