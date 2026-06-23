# ArgSort

Indirect sort of a matrix or vector.

```
vector vector::Sort(
  func_name  compare_func=NULL,  // comparison function
  T          context             // parameter for the custom sort function
   );
 
matrix matrix::Sort(
  func_name  compare_func=NULL   // comparison function
  T          context             // parameter for the custom sort function
   );
 
matrix matrix::Sort(
  const int  axis,               // axis for sorting
  func_name  compare_func=NULL   // comparison function
  T          context             // parameter for the custom sort function
   );

```

Parameters

axis

[in]  The axing along which to sort: 0 is horizontal, 1 is vertical.

func_name

[in]  Comparator. You can specify one of the values of the [ENUM_SORT_MODE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_sort_mode) enumeration or your own comparison function. If no function is specified, ascending sort is used.  

   

A custom comparison function can be of two types:

- int comparator(T x1,T x2)
- int comparator(T x1,T x2,TContext context)

Here T is the type of matrix or vector, and TContex is the type of the 'context' variable which is passed as an additional parameter to the Sort method.

context

[in] Additional optional parameter that can be passed to a custom sort function.

Return Value

Vector or matrix with the indexes of sorted elements. For example, the result [4,2,0,1,3] indicates that there should be an element with index 4 in the zero position, an element with index 2 in the first position, and so on.
