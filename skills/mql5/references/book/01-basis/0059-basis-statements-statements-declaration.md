# Declaration/definition statements

The declaration of a variable, array, function, or any other named element of a program (including structures and classes, which will be discussed in Part 3) is a statement.

The declaration must contain the type and identifier of the element (see [Declaring and defining variables](/en/book/basis/variables/define_vs_declare)), as well as an optional initial value for [initialization](/en/book/basis/variables/initialization). Also, when declaring, additional modifiers can be specified that change certain characteristics of the element. In particular, we already know the [static](/en/book/basis/variables/static_variables) and [const](/en/book/basis/variables/const_variables) modifiers, and more will be added soon. Arrays require an additional specification of the dimension and number of elements (see [Description of arrays](/en/book/basis/arrays/arrays_declaration)), while functions require a list of parameters (for further details please see [Functions](/en/book/basis/functions/functions_definition)).

The variable declaration statement can be summarized as follows:

```
[modifiers] identifier type
  [= initialization expressions] ;

```

For an array, it looks like this:

```
[modifiers] identifier type [ [size_1]ᵒᵖᵗ ] [ [size_N] ]ᵒᵖᵗ(3)
  [ = { initialization_list } ]ᵒᵖᵗ ;

```

The main difference is the mandatory presence of at least one pair of square brackets (the size inside them can be indicated or not; depending on that, we get a fixed or dynamically distributed array). In total, up to 4 pairs of square brackets are allowed (4 is the maximum supported number of measurements).

In many cases, a declaration can simultaneously act as a definition, i.e. it reserves memory for the element, determines its behavior, and makes it possible to use it in the program. Specifically, the declaration of a variable or array is also a definition. From this point of view, a declaration statement can be called a definition statement all the same, but this has not become a common practice.

Our basic knowledge of functions is enough to reliably assume what their definition should look like:

```
type identifier ( [list_of_arguments] )
{
  [statements]
}

```

Type, identifier, and list of arguments make up the function header.

Please note that this is a definition since this description contains both the external attributes of the function (interface) and statements that define its internal essence (implementation). The latter is done with a block of code formed by a pair of curly brackets and immediately following the function header. As you might guess, this is an example of the compound statement we mentioned in [the previous section](/en/book/basis/statements/statements_compound). In this case, a terminological tautology is indispensable, since it is perfectly justified: the compound statement is part of the function definition statement.

A little later, we will learn why and how to separate the interface description from the implementation and thereby achieve [function declaration](/en/book/basis/functions/functions_declaration) without defining it. We will also demonstrate the difference between a [declaration and a definition using the class](/en/book/oop/classes_and_interfaces/classes_declaration_definition) as an example.

The declaration statement makes the new element available by its name in the context of the code block (see [Context, scope, and lifetime of variables](/en/book/basis/variables/scope_and_lifetime)) in which the statement is located. Recall that blocks form the local scope of objects (variables, arrays). In the first part of the book, we encountered this when describing the greeting function.

In addition to local scopes, there is always a global scope, in which you can also use declaration statements to create elements that are accessible from anywhere in the program.

If there is no static modifier in the declaration statement and it is located in some local block, then the corresponding element is created and initialized at the moment the statement is executed (strictly speaking, memory for all local variables inside the function is allocated, for the sake of efficiency, immediately upon entering the function, but they are not yet formed at that moment).

For example, the following declaration of the variable i at the beginning of the OnStart function ensures that such a variable will be created with the specified initial value (0) as soon as the function receives control (i.e., the terminal will call it because it is the main function of the script).

```
void OnStart()
{
   int i = 0;
   Print(i);
   
   // error: 'j' - undeclared identifier
   // Print(j); 
   int j = 1;
}

```

Thanks to the declaration in the first statement, the variable i is known and available in the subsequent lines of the function, in particular, in the second line with the call of the Print function, which displays the contents of the variable in the log.

The variable j described in the last line of the function will be created just before the end of the function (this, of course, is meaningless, but clear). Therefore, this variable is not known in all earlier strings of this function. An attempt to output j to the log using a commented Print call will result in an "undeclared identifier" compilation error.

Elements declared this way (inside code blocks and without the static modifier) are called automatic, because the program itself allocates memory for them when entering the block and destroys them when exiting the block (in our case, after exiting the function). Therefore, the area of memory in which this happens is called the stack ("last in, first out").

Automatic elements are created in the order in which the declaration statements are executed (first i, then j). Destruction is performed in reverse order (first j, then i).

If a variable is declared without initialization and starts to be used in subsequent statements (for example, to the right of the '=' sign) without first writing a meaningful value into it, the compiler issues a warning: "possible use of uninitialized variable".

```
void OnStart()
{
   int i, p;
   i = p; // warning: possible use of uninitialized variable 'p'
}

```

If a declaration statement has the static modifier, the corresponding element is created only once when the statement is executed for the first time, and remains in memory, regardless of exit and possible subsequent entries and exits in the same block of code. All such static members are removed only when the program is unloaded.

Despite the increased lifetime, the scope of such variables is still limited to the local context in which they are defined, and can only be accessed from later statements (located below in the code).

In contrast, declaration statements in the global context create their elements in the same order in which they appear in the source code, immediately after the program is loaded (before any standard start function is called, such as OnStart for scripts). Global objects are deleted in reverse order when the program is unloaded.

To demonstrate the aforementioned, let's create a more "cunning" example (StmtDeclaration.mq5). Recalling the skills gained in the first part, in addition to OnStart, we will write a simple function Init, which will be used in variable initialization expressions and will log a sequence of calls.

```
int Init(const int v)
{
   Print("Init: ", v);
   return v;
}

```

The Init function accepts a single parameter v of integer type int, the value of which is returned to the calling code ([return](/en/book/basis/statements/statements_return)[ statement](/en/book/basis/statements/statements_return)).

This allows using it as a wrapper to set the initial value of a variable, for example, for two global variables:

```
int k = Init(-1);
int m = Init(-2);

```

The value of the passed argument gets into the variables k and m by calling the function and returning from it. However, inside Init, we additionally output the value with Print, and thus we can track how the variables are created.

Note that we cannot use the Init function in the initialization of global variables above its definition. If we try to move the k variable declaration above the Init declaration, we get the error "'Init' is an unknown identifier". This limitation only works for the initialization of global variables, because functions are also defined globally, and the compiler builds a list of such identifiers in one go. In all other cases, the order of defining functions in the code is not important, because the compiler first registers them all in the internal list, and then mutually links their calls from blocks. In particular, you can move the entire Init function and the declaration of the global variables k and m below the OnStart function - it will not break anything.

Inside the OnStart function, we will describe several more variables using Init: local i and j, as well as static n. For simplicity, all variables are given unique values so that they can be distinguished.

```
void OnStart()
{
   Print(k);
   
   int i = Init(1);
   Print(i);
   // error: 'n' - undeclared identifier
   // Print(n);
   static int n = Init(0);
   // error: 'j' - undeclared identifier
   // Print(j);
   int j = Init(2);
   Print(j);
   Print(n);
}

```

Comments here show erroneous attempts to call the relevant variables before they are defined.

Run the script and get the following log:

```
Init: -1
Init: -2
-1
Init: 1
1
Init: 0
Init: 2
2
0

```

As we can see, the global variables were initialized before the OnStart function was called, and exactly in the order in which they were encountered in the code. Internal variables were created in the same sequence as their declaration statements were written.

If a variable is defined but not used anywhere, the compiler will issue a "variable 'name' not used" warning. This is a sign of a potential programmer error.

Looking ahead, let's say that with the help of declaration/definition statements, not only data elements (variables, arrays) or functions, but also new user-defined types (structures, classes, templates, namespaces) that are not yet known to us can be introduced into the program. Such statements can only be made at the global level, that is, outside of all functions.

It is also impossible to define a function within a function. The following code will not compile:

```
void OnStart()
{
   int Init(const int v)
   {
      Print("Init: ", v);
      return v;
   }
   int i = 0;
}

```

The compiler will generate an error: "function declarations are allowed on global, namespace, or class scope only".
