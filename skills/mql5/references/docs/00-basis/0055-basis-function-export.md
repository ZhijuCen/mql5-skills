# Exporting Functions

A function declared in a mql5 program with the export postmodifier can be used in another mql5 program. Such a function is called exportable, and it can be called from other programs after compilation.

```
int Function() export
  {
  }

```

This modifier orders the compiler to add the function into the table of EX5 functions exported by this ex5 file. Only function with such a modifier are accessible ("visible") from other mql5 programs.

The [library](/en/docs/basis/preprosessor/compilation) property tells the compiler that the EX5-file will be a library, and the compiler will show it in the header of EX5.

All functions that are planned as exportable ones must be marked with the export modifier.

See also

[Overload](/en/docs/basis/oop/overload), [Virtual Functions](/en/docs/basis/oop/virtual), [Polymorphism](/en/docs/basis/oop/polymorphism)
