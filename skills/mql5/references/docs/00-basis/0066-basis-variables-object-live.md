# Creating and Deleting Objects

After a MQL5 program is loaded for execution, memory is allocated to each variable according to its type. According to the access level, all variables are divided into two types - [global variables](/en/docs/basis/variables/global) and [local variables](/en/docs/basis/variables/local). According to the memory class, they can be [input parameters](/en/docs/basis/variables/inputvariables) of a MQL5 program, [static](/en/docs/basis/variables/static) and automatic. If necessary, each variable is [initialized](/en/docs/basis/variables/initialization) by a corresponding value. After being used a variable is unintialized and memory used by it is returned to the MQL5 executable system.

## Initialization and Deinitialization of Global Variables

Global variables are initialized automatically right after a MQL5 program is loaded and before any of function is called. During initialization initial values are assigned to variables of [simple](/en/docs/basis/types#base_types) types and a constructor (if there is any) is called for objects. [Input variables](/en/docs/basis/variables/inputvariables) are always declared at a global level, and are initialized by values set by a user in the dialog during the program start.

Despite the fact that [static](/en/docs/basis/variables/static) variables are usually declared at a local level, the memory for these variables is pre-allocated, and initialization is performed right after a program is loaded, the same as for [global](/en/docs/basis/variables/global) variables.

The initialization order corresponds to the variable declaration order in the program. Deinitialization is performed in the reverse order. This rule is true only for the variables that were not created by the new operator. Such variables are created and initialized automatically right after loading, and are deinitialized before the program unloading.

## Initialization and Deinitialization of Local Variables

If a variable declared on a local level is not a static one, memory is allocated automatically for such a variable. Local variables, as well as global ones, are initialized automatically at the moment when the program execution meets their declaration. Thus the initialization order corresponds to the order of declaration.

Local variables are deinitialized at the end of the program block, in which they were declared, and in the order opposite to their declaration. A program block is a [compound operator](/en/docs/basis/operators/compound) that can be a part of selection operator [switch](/en/docs/basis/operators/switch), loop operator ([for](/en/docs/basis/operators/for), [while](/en/docs/basis/operators/while), [do-while](/en/docs/basis/operators/dowhile)), [a function body](/en/docs/basis/function#function_body) or a part of the [if-else operator](/en/docs/basis/operators/if).

Local variables are initialized only at the moment when the program execution meets the variable declaration. If during the program execution the block, in which the variable is declared, was not executed, such a variable is not initialized.

## Initialization and Deinitialization of Objects Placed

A special case is that with [object pointers](/en/docs/basis/types/object_pointers), because declaration of a pointer does not entail initialization of a corresponding objects. Dynamically placed objects are initialized only at the moment when the class sample is created by the [new operator](/en/docs/basis/operators/newoperator). Initialization of objects presupposes call of a constructor of a corresponding class. If there is no corresponding constructor in the class, its members of a [simple type](/en/docs/basis/types#base_types) will not be automatically initialized; members of types [string](/en/docs/basis/types/stringconst), [dynamic array](/en/docs/basis/types/dynamic_array) and [complex object](/en/docs/basis/types#complex_types) will be automatically initialized.

Pointers can be declared on a local or global level; and they can be initialized by the empty value of [NULL](/en/docs/basis/types/void) or by the value of the pointer of the same or [inherited](/en/docs/basis/oop/inheritance) type. If the new operator is called for a pointer declared on a local level, the delete operator for this pointer must be performed before exiting the level. Otherwise the pointer will be lost and the explicit deletion of the object will fail.

All objects created by the expression of object_pointer=new Class_name, must be then deleted by the delete(object_pointer) operator. If for some reasons such a variable is not deleted by the [delete operator](/en/docs/basis/operators/deleteoperator) when the program is completed, the corresponding entry will appear in the "Experts" journal. One can declare several variables and assign a pointer of one object to all of them.

If a dynamically created object has a constructor, this constructor will be called at the moment of the new operator execution. If an object has a destructor, it will be called during the execution of the delete operator.

Thus dynamically placed objects are created only at the moment when the corresponding new operator is invoked, and are assuredly deleted either by the delete operator or automatically by the executing system of MQL5 during the program unloading. The order of declaration of pointers of dynamically created object doesn't influence the order of their initialization. The order of initialization and deinitialization is fully controlled by the programmer.

## Dynamic memory allocation in MQL5

When working with dynamic arrays, released memory is immediately returned back to the operating system.

When working with dynamic class objects using the [new operator](/en/docs/basis/operators/newoperator), first memory is requested from the class memory pool the memory manager is working with. If there is not enough memory in the pool, memory is requested from the operating system. When deleting the dynamic object using the [delete operator](/en/docs/basis/operators/deleteoperator), released memory is immediately returned back to the class memory pool.

Memory manager releases memory back to the operating system immediately after exiting the following event handling functions: [OnInit()](/en/docs/runtime/event_fire#init), [OnDeinit()](/en/docs/runtime/event_fire#deinit), [OnStart()](/en/docs/runtime/event_fire#start), [OnTick()](/en/docs/runtime/event_fire#newtick), [OnCalculate()](/en/docs/runtime/event_fire#calculate), [OnTimer()](/en/docs/runtime/event_fire#timer), [OnTrade()](/en/docs/runtime/event_fire#trade), [OnTester()](/en/docs/runtime/event_fire#tester), [OnTesterInit()](/en/docs/runtime/event_fire#testerinit), [OnTesterPass()](/en/docs/runtime/event_fire#testerpass), [OnTesterDeinit()](/en/docs/runtime/event_fire#testerdeinit), [OnChartEvent()](/en/docs/runtime/event_fire#chartevent), [OnBookEvent()](/en/docs/runtime/event_fire#bookevent).

## Brief Characteristics of Variables

The main information about the order of creation, deletion, about calls of constructors and destructors is given in the below table.

|  | Global automatic variable | Local automatic variable | Dynamically created object |
| --- | --- | --- | --- |
| Initialization | right after a mql5 program is loaded | when the code line where it is declared is reached during execution | at the execution of the  new  operator |
| Initialization order | in the order of declaration | in the order of declaration | irrespective of the order of declaration |
| Deinitialization | before a mql5 program is unloaded | when execution exits the declaration block | when the  delete  operator is executed or before a mql5 program is unloaded |
| Deinitialization order | in the order opposite to the initialization order | in the order opposite to the initialization order | irrespective of the initialization order |
| Constructor call | at mql5 program loading | at initialization | at the execution of the  new  operator |
| Destructor call | at mql5 program unloading | when exiting the block where the variable was initialized | at the execution of the  delete  operator |
| Error logs | log message in the "Experts" journal about the attempt to delete an automatically created object | log message in the "Experts" journal about the attempt to delete an automatically created object | log message in the "Experts" journal about undeleted dynamically created objects at the unload of a mql5 program |

See also

[Data Types](/en/docs/basis/types), [Encapsulation and Extensibility of Types](/en/docs/basis/oop/incapsulation),[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope)
