# External variables

The material in this section is simultaneously complex and optional. It requires the knowledge of the concepts that are based on the analogy to C++ and those considered hereinbelow. At the same time, the effect of the language structure described can be achieved in another manner, while its flexibility is a potential source of errors.

MQL5 allows describing variables as external ones. This is made using the extern keyword and is only permitted in the [global context](/en/book/basis/variables/scope_and_lifetime).

For an external variable, syntax basically repeats a normal description but it additionally has the 'extern' keyword while initialization is prohibited:

```
extern type identifier;

```

Describing a variable as external means that its description is delayed and must occur later in the source code, usually in another file (connecting files using the [#include](/en/book/basis/preprocessor/preprocessor_include)[ directive](/en/book/basis/preprocessor/preprocessor_include) will be considered in the chapter dealing with the [preprocessor](/en/book/basis/preprocessor)). Several different source files can have a description of the same external variable, that is, those having identical types and identifiers. All such descriptions refer to the same variable.

It is assumed that this variable will be completely described in one of the files. If the variable is not defined anywhere in the code without the extern keyword, the "unresolved extern variable" compilation error is returned (similar to a linker error in C++ in such cases).

Describing an external variable allows using it efficiently in the source code of a particular file. In other words, it enables compiling a given module, although the variable is not created in this module.

Using extern in MQL5 is not so insistent as in C++ and in most cases, may be replaced by enabling a header file with general descriptions of the variables to be declared as extern. It is sufficient to perform these definitions conventionally. The compiler ensures adding each attached file to the source code only once. Considering that in MQL5 a program always consists of one compilable unit mq5, there is no C++ problem here, with the potential error of the multiple definitions of the same variable due to enabling the header in different units.

Even an additional mq5 (not mqh) file is attached in the #include directive, it does not equally compete with the main unit, for which compilation is launched; instead, it is considered as one of the headers.

Unlike C++, MQL5 does not allow specifying an initial value for an external variable (initialization in C++ leads to ignoring the word extern). If you try to set an initial value, you will get a compilation error "extern variable initialization is not allowed".

Generally, describing a variable as external can be considered a kind of "soft" description: It ensures the appearance of the variable and excludes the overriding error that would occur if the variable is described in several files without the extern modifier.

However, this can be a source of errors. If in different header files, by coincidence, identical variables are described for different purposes, then no keyword extern allows identifying a collision, while with extern, the variables will become one, and the program operation logic will most likely be broken.

As external, both variables and functions can be described (they will be considered [below](/en/book/basis/functions)). For functions, describing them with the attribute as external is a rudiment (i.e., it is compiled, but does not make any changes). The following two declarations of a function are equivalent:

```
extern return_type name([parameters]);
      return_type name([parameters]);

```

In this sense, the presence/absence of extern can only be used to stylistically distinguish between a forward description of a function from the current unit (no extern) or from an external one (extern is present).

You can use extern in both the mq5 unit to be compiled and header files to be attached.

Let's consider some options for using extern: They are entered in different files, i.e., main script ExternMain.mq5 and 3 attachable files: ExternHeader1.mqh, ExternHeader2.mqh, and ExternCommon.mqh.

In the main file, only ExternHeader1.mqh and ExternHeader2.mqh are attached, while we will need ExternCommon.mqh a bit later.

```
// source code from mqh files will be substituted implicitly
// in the main mq5 file, instead of these directives
#include "ExternHeader1.mqh"
#include "ExternHeader2.mqh"

```

In header files, two conditionally useful functions are defined: In the first one, function inc for the x variable increment, while in the second, function dec for the x variable decrement. It is variable x that is described in both files as external:

```
// ExternHeader1.mqh
extern int x;
void inc()
{
   x++;
}
// -----------------
// ExternHeader2.mqh
extern int x;
void dec()
{
   x--;
}

```

Due to this description, each of the mqh files is compiled in a regular way. When they are included in an mq5 file together, the entire program is compiled, too.

If the variable were defined in each file without the word extern, the re-defining error would occur in compiling the program as a whole. If we had transferred the definition of x from header files into the main unit, header files would have stopped being compiled (it is not a problem for somebody, perhaps; however, in larger programs, developers like checking the compilation ability of immediate corrections without compiling the entire project).

In the main script, we define a variable (in this case, with an initial value of 2, while if we do not specify the value, the default 0 will be used) and call the conditionally useful functions, as well as print the x value.

```
int x = 2;
   
void OnStart()
{
   inc();  // uses x
   dec();  // uses x
   Print(x); // 2
   ...
}

```

In file ExternHeader1.mqh, there is the description of variable short z (without extern). A similar description is commented upon in the main script. If we make this string active, we will get the error mentioned before ("variable already defined"). This is done to illustrate the potential problem.

In ExternHeader1.mqh, extern long y is described, too. At the same time, in file ExternHeader2.mqh, the homonym external variable has another type: extern short y. If the latter description were not "moved" into a comment preemptively, the types incompatibility error ("variable 'y' already defined with different type") would occur here. Summary: Either types must coincide or variables must not be external. If both options are not good, it means that there is a mistype in the name of one of the variables.

Moreover, it should be noted that variable y is not explicitly initialized. However, the main script calls it successfully and prints 0 in the log:

```
long y;
   
void OnStart()
{
   ...
   Print(y); // 0
}

```

Finally, there is a possibility provided in the script to try an alternative of the external twin variables, exemplified by the already known variable x. Instead of describing extern int x, each of the files ExternHeader1.mqh and ExternHeader2.mqh can include another common header, ExternCommon.mqh, in which there is the description of int x (without extern). It becomes the only description of x in the project.

This alternative mode of assembling the program is enabled when activating [macro](/en/book/basis/preprocessor/preprocessor_define_simple) USE_INCLUDE_WORKAROUND: It is in the comment at the beginning of the script:

```
#define USE_INCLUDE_WORKAROUND // this string was in the comment
#include "ExternHeader1.mqh"
#include "ExternHeader2.mqh"

```

In this configuration, particular include files will still be compilable, as well as the entire project. In a real project, without using this method, the common mqh file would be included in ExternHeader1.mqh and ExternHeader2.mqh unconditionally (no USE_INCLUDE_WORKAROUND conditions). In this example, switching between the two threads of instructions is based on USE_INCLUDE_WORKAROUND is only needed to demonstrate both modes. For example, the simplified version of ExternHeader2.mqh should appear as follows:

```
// ExternHeader2.mqh
#include "ExternCommon.mqh" // int x; now here
 
void dec()
{
   x--;
}

```

We can check in the MetaEditor log that file ExternCommon.mqh loaded only once, although it is referenced in both ExternHeader1.mqh and ExternHeader2.mqh.

```
'ExternMain.mq5'
'ExternHeader1.mqh'
'ExternCommon.mqh'
'ExternHeader2.mqh'
code generated

```

If the x variable is "registered" in ExternCommon.mqh, we shall not re-define it (without extern) in the main unit since this would cause a compilation error, but we can simply assign to it the desired value at the beginning of the algorithm.
