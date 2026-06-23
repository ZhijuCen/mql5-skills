# Packing structures in memory and interacting with DLLs

To store one instance of the structure, a contiguous area is allocated in memory, sufficient to fit all the elements.

Unlike in C++, here structure elements follow one after another in memory and are not aligned on the boundary of 2, 4, 8 or 16 bytes, depending on the size of the elements themselves (alignment algorithms differ for different compilers and operating modes). Alignment of elements, the size of which is less than the specified block, is performed by adding unused dummy variables to the composition of the structure (the program does not have direct access to them). Alignment is used to optimize memory performance.

MQL5 allows you to change the alignment rules if necessary, mainly when integrating MQL programs with third-party DLLs that describe specific types of structures. For those, it is necessary to prepare an equivalent description in MQL5 (see the section on [importing libraries](/en/book/advanced/libraries/libraries_import)). It is important to note that structures intended for integration should only have fields of a limited set of types in their definition. So, they cannot use strings, dynamic arrays, as well as class objects, and [pointers](/en/book/oop/classes_and_interfaces/classes_pointers) to class objects.

Alignment is controlled by the keyword pack added to the header of the structure. There are two options:

```
struct pack(size) identifier
struct identifier pack(size)

```

In both cases, the size is an integer 1, 2, 4, 8, 16. Or you can use sizeof(built-in_type) operator as the size, for example, sizeof(double).

The option pack(1), i.e. byte alignment, is identical to default behavior without pack modifier.

The special operator offsetof() allows you to find out the offset in bytes of a specific structure element from its beginning. It has 2 parameters: structure object and element identifier. For example,

```
Print(offsetof(Result, status)); // 36

```

Before the status field in the Result structure, there are 4 double values and one int value: 36 in total.

When designing your own structures, it is recommended that you place the largest elements first, and then the rest - in order of decreasing their size.
