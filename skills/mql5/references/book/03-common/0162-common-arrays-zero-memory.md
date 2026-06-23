# Zeroing objects and arrays

Usually, initialization or filling of variables and arrays does not cause problems. So, for simple variables, we can simply use the operator '=' in the definition statement along with [initialization](/en/book/basis/variables/initialization), or assign the desired value at any later time.

Aggregate view initialization is available for structures (see section [Defining Structures](/en/book/oop/structs_and_unions/structs_definition)):

```
Struct struct = {value1, value2, ...};

```

But it is possible only if there are no dynamic arrays and strings in the structure. Moreover, the aggregate initialization syntax cannot be used to clean up a structure again. Instead, you must either assign values to each field individually or reserve an instance of the empty structure in the program and copy it to clearable instances.

If at the same time, we are talking about an array of structures, then the source code will quickly grow due to auxiliary but necessary instructions.

For arrays, there are the [ArrayInitialize](/en/book/common/arrays/arrays_init_fill)[ and ](/en/book/common/arrays/arrays_init_fill)[ArrayFill](/en/book/common/arrays/arrays_init_fill) functions, but they only support numeric types: an array of strings or structures cannot be filled with them.

In such cases, the ZeroMemory function can be useful. It is not a panacea, since it has significant limitations in the scope, but it is good to know it.

void ZeroMemory(void &entity)

The function can be applied to a wide range of different entities: variables of simple or object types, as well as their arrays (fixed, dynamic, or multidimensional).

Variables get the 0 value (for numbers) or its equivalent (NULL for strings and pointers).

In the case of an array, all its elements are set to zero. Do not forget that the elements can be objects, and in turn, contain objects. In other words, the ZeroMemory function performs a deep memory cleanup in a single call.

However, there are restrictions on valid objects. You can only populate with zeros the objects of structures and classes, which:

- contain only public fields (i.e., they do not contain data with access type private or protected)
- do not contain fields with the const modifier
- do not contain pointers

The first two restrictions are built into the compiler: an attempt to nullify objects with fields that do not meet the specified requirements will cause errors (see below).

The third limitation is a recommendation: external zeroing of a pointer will make it difficult to check the integrity of the data, which is likely to lead to the loss of the associated object and to a memory leak.

Strictly speaking, the requirement of publicity of fields in nullable objects violates the [encapsulation](/en/book/oop/classes_and_interfaces/classes_encapsulation) principle, which is inherent in class objects, and therefore ZeroMemory is mainly used with objects of simple structures and their arrays.

Examples of working with ZeroMemory are given in the script ZeroMemory.mq5.

The problems with the aggregate initialization list are demonstrated using the structure Simple:

```
#define LIMIT 5
   
struct Simple
{
   MqlDateTime data[]; // dynamic array disables initialization list,
   // string s; // and a string field would also forbid,
   // ClassType *ptr; // and a pointer too
   Simple()
   {
      // allocating memory, it will contain arbitrary data
      ArrayResize(data, LIMIT);
   }
};

```

In the OnStart function or in the global context, we cannot define and immediately nullify an object of such a structure:

```
void OnStart()
{
   Simple simple = {}; // error: cannot be initialized with initializer list
   ...

```

The compiler throws the error "cannot use initialization list". It is specific to fields like dynamic arrays, string variables, and pointers. In particular, if the data array were of a fixed size, no error would occur.

Therefore, instead of an initialization list, we use ZeroMemory:

```
void OnStart()
{
   Simple simple;
   ZeroMemory(simple);
   ...

```

The initial filling with zeros could also be done in the structure constructor, but it is more convenient to do subsequent cleanups outside (or provide a method for this with the same function ZeroMemory).

The following class is defined in Base.

```
class Base
{
public: // public is required for ZeroMemory
   // const for any field will cause a compilation error when calling ZeroMemory:
   // "not allowed for objects with protected members or inheritance"
   /* const */ int x;
   Simple t;   // using a nested structure: it will also be nulled
   Base()
   {
      x = rand();
   }
   virtual void print() const
   {
      PrintFormat("%d %d", &this, x);
      ArrayPrint(t.data);
   }
};

```

Since the class is further used in arrays of objects nullable with ZeroMemory, we are forced to write an access section public for its fields (which, in principle, is not typical for classes and is done to illustrate the requirements imposed by ZeroMemory). Also, note that fields cannot have the modifier const. Otherwise, we'll get a compilation error with text that unfortunately doesn't really fit the problem: "forbidden for objects with protected members or inheritance".

The class constructor fills the field x with a random number so that later you can clearly see its cleaning by the function ZeroMemory. The print method displays the contents of all fields for analysis, including the unique object number (descriptor) &this.

MQL5 does not prevent ZeroMemory from being applied to a pointer variable:

```
   Base *base = new Base();
   ZeroMemory(base); // will set the pointer to NULL but leave the object

```

However, this should not be done, because the function resets only the base variable itself, and, if it referred to an object, this object will remain "hanging" in memory, inaccessible from the program due to the loss of the pointer.

You can nullify a pointer only after the pointer instance has been freed using the delete operator. Furthermore, it is easier to reset a separate pointer from the above example, like any other simple variable (non-composite), using an assignment operator. It makes sense to use ZeroMemory for composite objects and arrays.

The function allows you to work with objects of the class hierarchy. For example, we can describe the derivative of the Dummy class derived from Base:

```
class Dummy : public Base
{
public:
   double data[]; // could also be multidimensional: ZeroMemory will work
   string s;
   Base *pointer; // public pointer (dangerous)
   
public:
   Dummy()
   {
      ArrayResize(data, LIMIT);
      
      // due to subsequent application of ZeroMemory to the object
      // we'll lose the 'pointer'
      // and get warnings when the script ends
      // about undeleted objects of type Base
      pointer = new Base();
   }
   
   ~Dummy()
   {
      // due to the use of ZeroMemory, this pointer will be lost
      // and will not be freed
      if(CheckPointer(pointer) != POINTER_INVALID) delete pointer;
   }
   
   virtual void print() const override
   {
      Base::print();
      ArrayPrint(data);
      Print(pointer);
      if(CheckPointer(pointer) != POINTER_INVALID) pointer.print();
   }
};

```

It includes fields with a dynamic array of type double, string and pointer of type Base (this is the same type from which the class is derived, but it is used here only to demonstrate the pointer problems, so as not to describe another dummy class). When the ZeroMemory function nullifies the Dummy object, an object at pointer is lost and cannot be freed in the destructor. As a result, this leads to warnings about memory leaks in the remaining objects after the script terminates.

ZeroMemory is used in OnStart to clear the Dummy objects array:

```
void OnStart()
{
   ...
   Print("Initial state");
   Dummy array[];
   ArrayResize(array, LIMIT);
   for(int i = 0; i < LIMIT; ++i)
   {
      array[i].print();
   }
   ZeroMemory(array);
   Print("ZeroMemory done");
   for(int i = 0; i < LIMIT; ++i)
   {
      array[i].print();
   }

```

The log will output something like the following (the initial state will be different because it prints the contents of the "dirty", newly allocated memory; here is a small code part):

```
Initial state
1048576 31539
     [year]     [mon]    [day] [hour] [min] [sec] [day_of_week] [day_of_year]
[0]       0     65665       32      0     0     0             0             0
[1]       0         0        0      0     0     0         65624             8
[2]       0         0        0      0     0     0             0             0
[3]       0         0        0      0     0     0             0             0
[4] 5242880 531430129 51557552      0     0 65665            32             0
0.0 0.0 0.0 0.0 0.0
...
ZeroMemory done
1048576 0
    [year] [mon] [day] [hour] [min] [sec] [day_of_week] [day_of_year]
[0]      0     0     0      0     0     0             0             0
[1]      0     0     0      0     0     0             0             0
[2]      0     0     0      0     0     0             0             0
[3]      0     0     0      0     0     0             0             0
[4]      0     0     0      0     0     0             0             0
0.0 0.0 0.0 0.0 0.0
...
5 undeleted objects left
5 objects of type Base left
3200 bytes of leaked memory

```

To compare the state of objects before and after cleaning, use descriptors.

So, a single call to ZeroMemory is able to reset the state of an arbitrary branched data structure (arrays, structures, arrays of structures with nested structure fields and arrays).

Finally, let's see how ZeroMemory can solve the problem of string array initialization. The ArrayInitialize and ArrayFill functions do not work with strings.

```
   string text[LIMIT] = {};
   // an algorithm populates and uses 'text'
   // ...
   // then you need to re-use the array
   // calling functions gives errors:
   // ArrayInitialize(text, NULL);
   //      `-> no one of the overloads can be applied to the function call
   // ArrayFill(text, 0, 10, NULL);
   //      `->  'string' type cannot be used in ArrayFill function
   ZeroMemory(text);               // ok

```

In the commented instructions, the compiler would generate errors, stating that the type string is not supported in these functions.

The way out of this problem is the ZeroMemory function.
