# Cancelling macro substitution (#undef)

Substitutions registered with #define can be undone if they are no longer needed after a particular piece of code. For these purposes, the #undef directive is used.

```
#undef macro_identifier

```

In particular, it is useful if you need to define the same macro in different ways in different parts of the code. If the identifier specified in #define has already been registered somewhere in earlier lines of code (by another #define directive), then the old definition is replaced with the new one, and the preprocessor generates the "macro redefinition" warning. The use of #undef avoids the warning while explicitly indicating the programmer's intention not to use a particular macro further down the code.

#undef cannot undefine [predefined macros](/en/book/basis/preprocessor/preprocessor_predefined).
