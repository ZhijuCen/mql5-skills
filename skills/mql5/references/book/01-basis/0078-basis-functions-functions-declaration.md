# Function declaration

Function declaration describes a prototype without specifying a function body. Instead of a block with a body, a semicolon is put.

The declaration is necessary for the compiler so that it can check in subsequent code fragments how correctly the function is called by name, passing arguments to it and getting the result.

The entire function definition (including the body) is also a declaration, so there is no need to declare a function in addition to the definition.

For example, the declaration of the Fibo function above could look like this.

```
int Fibo(const int n);

```

Separate function declarations and definitions are used when building a program from several files with source text: then the declaration is made in the header file with the extension mqh (see the section about the [#include preprocessor directive ](/en/book/basis/preprocessor/preprocessor_include)), which is included in files where the function is used, and the function definition is implemented in only one of the files. Matching of the function signature in the declaration and definition provides error protection. In other words, a single declaration guarantees the consistency of changes made to the entire source code

If we declare a function and call it somewhere in the code, but do not provide a fully appropriate definition for it, the compiler will throw an error: "function 'Name' must have a body". This often happens when there are typos or inaccuracies either in the declaration or in the definition, as well as in the process of changing the source codes, when some of the corrections have already been made, and the other part has most likely been forgotten.

If the function is declared and not used anywhere, the compiler does not require its definition either - such an element is simply "cut out" from the binary program.

In the [Declaration/definition statements](/en/book/basis/statements/statements_declaration) section, we considered an example of the Init function (script StmtDeclaration.mq5), which was used to initialize variables. There, in particular, the problem was demonstrated that the global variable k cannot be defined before the Init function, since the initial value k is obtained by calling Init. The compiler through the error "'Init' is an unknown identifier".

Now we know that such a problem can be solved with a declaration. In the FuncDeclaration.mq5 script, we added the following forward declaration of the Init function before the k variable, and left the  Init definition after k.

```
// preliminary declaration
int Init(const int v);
// before adding preliminary declaration above
// here was an error: 'Init' is an unknown identifier
int k = Init(-1);
int Init(const int v)
{
   Print("Init: ", v);
   return v;
}

```

Now the script compiles normally. Technically, in this case, we could simply move the function above the variable without a preliminary declaration. We did this to explain the concept. However, there are cases of mutual dependence of language elements on each other (for example, classes), when it is impossible to go without a preliminary declaration within the same file.
