# Global Variables

Global variables are created by placing their declarations outside function descriptions. Global variables are defined at the same level as functions, i.e., they are not local in any block.

Example:

```
int GlobalFlag=10;   // Global variable
int OnStart()
  {
   ...
  }

```

The scope of global variables is the entire program. Global variables are accessible from all functions defined in the program. They are initialized to zero unless another initial value is explicitly defined. A global variable can be initialized only by a constant or constant expression that corresponds to its type.

Global variables are initialized only once after the program is loaded into the client terminal memory and before the first handling of the [Init](/en/docs/runtime/event_fire#init) event. For global variables representing class objects, during their initialization the corresponding constructors are called. In scripts global variables are initialized before handling the [Start](/en/docs/runtime/event_fire#start) event.

Note: Variables declared at global level must not be mixed up with the client terminal global variables that can be accessed using the [GlobalVariable...()](/en/docs/globals) functions.

See also

[Data Types](/en/docs/basis/types), [Encapsulation and Extensibility of Types](/en/docs/basis/oop/incapsulation),[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
